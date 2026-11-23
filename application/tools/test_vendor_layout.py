#!/usr/bin/env python3
"""Compile the actual optional renderer and run every vendored library unit test.

This development test reuses scripts/tests/support.py's process adapter explicitly.
It never changes dependency resolution or downloads a missing toolchain/crate.
Reports are new directories; raw failures and exact compiler inputs are retained.
It does not run upstream benches/examples or establish GPU runtime behavior.
"""

import argparse
import hashlib
import importlib.util
import json
import os
import re
import shutil
import sys
import tomllib
from datetime import UTC, datetime
from pathlib import Path

APPLICATION = Path(__file__).resolve().parents[1]
CHECKOUT = APPLICATION.parent
ADAPTER = CHECKOUT / "scripts/tests/support.py"
VENDOR = APPLICATION / "vendor/cryoglyph-0.1.0"
REQUIRED_TESTS = {
    "ox_layout_tests::gpu_layout_offsets_and_sizes_remain_exact",
    "ox_layout_tests::glyph_encoding_preserves_native_integer_and_float_bits",
    "ox_layout_tests::glyph_slice_handles_empty_and_multiple_records_without_copying",
    "ox_layout_tests::uniform_encoding_preserves_resolution_and_explicit_padding",
}


def digest(path):
    with path.open("rb") as source:
        return hashlib.file_digest(source, "sha256").hexdigest()


def inputs():
    paths = [ADAPTER, Path(__file__).resolve()]
    paths.extend(APPLICATION / name for name in ("Cargo.toml", "Cargo.lock"))
    paths.append(APPLICATION / "rust-toolchain.toml")
    for directory in ("crates", "vendor", ".cargo"):
        paths.extend(path for path in (APPLICATION / directory).rglob("*")
                     if path.is_file() and "__pycache__" not in path.parts)
    return {str(path.relative_to(CHECKOUT)): digest(path) if path.is_file() else None
            for path in sorted(set(paths))}


def load_adapter():
    spec = importlib.util.spec_from_file_location("ox_test_process_support", ADAPTER)
    if spec is None or spec.loader is None:
        raise ValueError("Cannot load the checkout's test-only process adapter")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Verification:
    def __init__(self, output, target):
        self.output = output
        self.target = target
        self.adapter = load_adapter()
        self.report = {"commands": [], "limitations": [
            "No GPU runtime, upstream benchmark or example execution is claimed.",
            "Direct rustc tests use Cargo-built dependencies selected by exact package ID.",
            "Static scanning of the caller is not transitive analysis of the process adapter.",
        ]}
        self.env = os.environ.copy()
        self.env.update(CARGO_NET_OFFLINE="true", CARGO_BUILD_JOBS="2",
                        CARGO_TARGET_DIR=str(target),
                        CARGO_HOME=os.environ.get("CARGO_HOME", str(CHECKOUT / ".cache/ox/cargo-home")))

    def command(self, name, argv, expected=0):
        record = {"name": name, "argv": list(map(str, argv)), "cwd": str(APPLICATION),
                  "started_at": datetime.now(UTC).isoformat()}
        self.report["commands"].append(record)
        stdout = self.output / f"{name}.stdout.log"
        stderr = self.output / f"{name}.stderr.log"
        with stdout.open("xb") as out, stderr.open("xb") as err:
            result = self.adapter.run(record["argv"], cwd=APPLICATION, env=self.env,
                                      stdout=out, stderr=err, timeout=None, check=False)
        record.update(exit_code=result.returncode, finished_at=datetime.now(UTC).isoformat(),
                      stdout_sha256=digest(stdout), stderr_sha256=digest(stderr))
        if expected is not None and result.returncode != expected:
            raise ValueError(f"{name}: exit {result.returncode}, expected {expected}; see raw logs")
        return stdout.read_text(), stderr.read_text(), result.returncode

    def execute(self):
        channel = tomllib.loads((APPLICATION / "rust-toolchain.toml").read_text())["toolchain"]["channel"]
        rustup = shutil.which("rustup")
        if not rustup:
            raise ValueError("rustup must be installed; this verifier does not acquire toolchains")
        executables = {}
        for name in ("cargo", "rustc"):
            stdout, _, _ = self.command(f"locate-{name}", [rustup, "which", "--toolchain", channel, name])
            executable = Path(stdout.strip()).resolve(strict=True)
            if not executable.is_file():
                raise ValueError(f"Invalid installed {name} path")
            executables[name] = str(executable)
            self.report[name] = {"path": str(executable), "sha256": digest(executable)}
        self.env.update(RUSTC=executables["rustc"], RUSTUP_TOOLCHAIN=channel)
        self.command("rustc-version", [executables["rustc"], "-vV"])
        cargo = executables["cargo"]
        metadata_text, _, _ = self.command("metadata", [cargo, "metadata", "--format-version=1",
            "--manifest-path", "crates/ox-ui/Cargo.toml", "--features", "iced/wgpu-bare", "--locked", "--offline"])
        metadata = json.loads(metadata_text)
        packages = [package for package in metadata["packages"]
                    if Path(package["manifest_path"]).resolve() == VENDOR / "Cargo.toml"]
        if len(packages) != 1:
            raise ValueError("Expected exactly one actual vendored cryoglyph package")
        package = packages[0]
        node = next(item for item in metadata["resolve"]["nodes"] if item["id"] == package["id"])
        dependencies = {dependency["name"]: dependency["pkg"] for dependency in node["deps"]}
        build_text, _, _ = self.command("build", [cargo, "build", "-p", "ox-ui", "--features",
            "iced/wgpu-bare", "--locked", "--offline", "--message-format=json"])
        artifacts = [json.loads(line) for line in build_text.splitlines() if line.startswith("{")]
        externs = {}
        for name in ("bytemuck", "cosmic_text", "etagere", "lru", "rustc_hash", "wgpu"):
            package_id = dependencies[name]
            candidates = {Path(filename).resolve() for artifact in artifacts
                          if artifact.get("reason") == "compiler-artifact"
                          and artifact["package_id"] == package_id
                          for filename in artifact["filenames"] if filename.endswith(".rlib")}
            if len(candidates) != 1:
                raise ValueError(f"Ambiguous or missing artifact for {name}: {package_id}")
            path = candidates.pop()
            if not path.is_relative_to(self.target):
                raise ValueError(f"Artifact outside the selected target directory: {path}")
            externs[name] = {"path": str(path), "sha256": digest(path), "package_id": package_id}
        self.report["externs"] = externs
        dependency_directory = {str(Path(value["path"]).parent) for value in externs.values()}
        if len(dependency_directory) != 1:
            raise ValueError("Inconsistent Cargo dependency artifact directories")
        artifact_directory = self.target / "ox-vendor-layout" / hashlib.sha256(str(self.output).encode()).hexdigest()
        artifact_directory.mkdir(parents=True, exist_ok=False)
        binary = artifact_directory / "cryoglyph-layout-tests"
        compiler = [executables["rustc"], "--edition=" + package["edition"], "--crate-name", "cryoglyph",
                    "--test", str(VENDOR / "src/lib.rs"), "-C", "debuginfo=0", "-D", "warnings",
                    "-L", "dependency=" + dependency_directory.pop()]
        for name, value in sorted(externs.items()):
            compiler.extend(["--extern", name + "=" + value["path"]])
        self.command("compile-tests", compiler + ["-o", str(binary)])
        self.report["test_binary"] = {"path": str(binary), "sha256": digest(binary)}
        stdout, _, _ = self.command("unit-tests", [str(binary), "--test-threads=1"])
        passed = set(re.findall(r"^test (\S+) \.\.\. ok$", stdout, re.MULTILINE))
        summary = re.search(r"test result: ok\. (\d+) passed; 0 failed; 0 ignored; 0 measured; 0 filtered out;", stdout)
        if not REQUIRED_TESTS <= passed or summary is None or int(summary.group(1)) != len(passed):
            raise ValueError("Missing, ignored, filtered or unsuccessful mandatory library unit tests")
        self.report["passed_tests"] = sorted(passed)
        for name, fields, diagnostic in (
            ("padding", "a: u8, b: u32", "derive(Pod) was applied to a type with padding"),
            ("boolean", "a: bool", "the trait bound `bool: Pod` is not satisfied"),
        ):
            source = self.output / f"negative-{name}.rs"
            source.write_text("#[repr(C)]\n#[derive(Clone, Copy, bytemuck::Pod, bytemuck::Zeroable)]\n"
                              f"struct Invalid {{ {fields} }}\nfn main() {{}}\n")
            _, stderr, code = self.command("negative-" + name, [executables["rustc"], "--edition=2024",
                "--crate-name", "invalid_" + name, str(source), "-L",
                "dependency=" + str(Path(externs["bytemuck"]["path"]).parent), "--extern",
                "bytemuck=" + externs["bytemuck"]["path"], "-o", str(artifact_directory / name)], expected=None)
            if code != 1 or diagnostic not in stderr:
                raise ValueError(f"Negative {name} compile did not reject the invalid Pod layout as expected")
            self.report["commands"][-1]["expected_rejection_confirmed"] = True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path, help="New report directory outside application/")
    args = parser.parse_args()
    output = args.output.resolve()
    target = Path(os.environ.get("CARGO_TARGET_DIR", APPLICATION / "target/vendor-layout")).resolve()
    if output.is_relative_to(APPLICATION) or target.is_relative_to(output) or output.is_relative_to(target):
        parser.error("Report must be outside application/ and separate from build artifacts")
    output.mkdir(parents=True, exist_ok=False, mode=0o700)
    verification = Verification(output, target)
    before = inputs()
    code = 1
    try:
        verification.execute()
        code = 0
    except (OSError, ValueError, KeyError, StopIteration) as error:
        verification.report["error"] = str(error)
    except KeyboardInterrupt:
        verification.report["error"] = "Interrupted; not accepted"
        code = 130
    finally:
        after = inputs()
        verification.report.update(inputs_before=before, inputs_after=after, inputs_unchanged=before == after)
        binaries = {record["path"]: record["sha256"]
                    for key in ("cargo", "rustc", "test_binary")
                    if (record := verification.report.get(key))}
        binaries.update({record["path"]: record["sha256"]
                         for record in verification.report.get("externs", {}).values()})
        binaries_after = {name: digest(Path(name)) if Path(name).is_file() else None
                          for name in binaries}
        verification.report.update(binaries_before=binaries, binaries_after=binaries_after,
                                   binaries_unchanged=binaries == binaries_after)
        if before != after or binaries != binaries_after:
            verification.report["error"] = "Observed source or binary inputs changed during verification"
            code = 1
        verification.report.update(exit_code=code, status="passed" if code == 0 else "incomplete")
        (output / "result.json").write_text(json.dumps(verification.report, indent=2) + "\n")
    print(f"Vendor layout verification: {verification.report['status']}; report: {output}")
    return code


if __name__ == "__main__":
    sys.exit(main())
