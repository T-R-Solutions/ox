"""Create a new local package, inspect it and smoke-test a clean extraction."""

import hashlib
import json
import os
import stat
import subprocess
import sys
import tempfile
import zipfile
import zlib
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath, PureWindowsPath

from governance_support import (
    MAX_EXPANDED,
    PACKAGE_NAME,
    distribution_files,
    governance_scope,
    inspect_bytes,
    inspect_tree,
    scope_errors,
    sha,
)

ROOT = Path(__file__).resolve().parents[3]


def source_inventory(root):
    """Capture the external build inputs; the archive never supplies this trust."""
    inventory = {}
    for path in distribution_files(root):
        name = path.relative_to(root).as_posix()
        _safe_source(root, name)
        status = path.stat()
        size = status.st_size
        if size > MAX_EXPANDED:
            raise ValueError("Archive inspection limit exceeded: " + name)
        inventory[name] = {"sha256": sha(path), "size": size, "mode": _mode(status)}
    return inventory


def _mode(status):
    if not stat.S_ISREG(status.st_mode) or status.st_mode & 0o7000:
        raise ValueError("Package source must be regular without privileged mode bits")
    return 0o755 if status.st_mode & 0o111 else 0o644


def _safe_name(name):
    path = PurePosixPath(name)
    if (
        not name
        or "\\" in name
        or path.as_posix() != name
        or path.is_absolute()
        or PureWindowsPath(name).drive
        or any(part in {"..", ".git"} for part in path.parts)
    ):
        raise ValueError("Unsafe package path: " + name)
    return path


def _safe_source(root, name):
    path = _safe_name(name)
    if name in {".ox-governance-copy.json", "package-manifest.json", "package-scope.json"}:
        raise ValueError("Reserved package path: " + name)
    source = root / name
    if root.is_symlink() or any(
        (root / Path(*path.parts[:index])).is_symlink()
        for index in range(1, len(path.parts) + 1)
    ):
        raise ValueError("Symlink in package source: " + name)
    if not source.resolve().is_relative_to(root.resolve()) or not source.is_file():
        raise ValueError("Missing or escaping package source: " + name)
    return source


def _payload(root, name, row):
    source = _safe_source(root, name)
    if (
        set(row) != {"sha256", "size", "mode"}
        or type(row["size"]) is not int
        or not 0 <= row["size"] <= MAX_EXPANDED
        or type(row["mode"]) is not int
        or row["mode"] not in (0o644, 0o755)
    ):
        raise ValueError("Invalid bounded package input: " + name)
    with source.open("rb") as stream:
        if _mode(os.fstat(stream.fileno())) != row["mode"]:
            raise ValueError("Package source mode changed: " + name)
        data = stream.read(row["size"] + 1)
    if len(data) != row["size"] or hashlib.sha256(data).hexdigest() != row["sha256"]:
        raise ValueError("Package source changed: " + name)
    return data


class _ForwardWriter:
    """Deliberately non-seekable: ZIP headers/descriptors have one canonical form."""

    def __init__(self, stream):
        self.stream = stream
        self.position = 0
        self.discard = False

    def tell(self):
        return self.position

    def write(self, data):
        if self.discard:
            return len(data)
        written = self.stream.write(data)
        if written != len(data):
            raise OSError("Short package write")
        self.position += written
        return written

    def flush(self):
        self.stream.flush()


class _CompareWriter:
    """Compare the canonical serialization without trusting a ZIP parser or index."""

    def __init__(self, stream):
        self.stream = stream
        self.position = 0

    def write(self, data):
        if self.stream.read(len(data)) != data:
            raise ValueError(f"Noncanonical or corrupt package bytes at {self.position}")
        self.position += len(data)
        return len(data)

    def flush(self):
        pass


def _metadata(inventory):
    from instruction_revision import COPY_CONTEXT, COPY_CONTEXT_BYTES

    manifest = {name: row["sha256"] for name, row in sorted(inventory.items())}
    manifest[COPY_CONTEXT] = hashlib.sha256(COPY_CONTEXT_BYTES).hexdigest()
    scope = governance_scope()
    if scope_errors(scope):
        raise ValueError("Invalid governance package scope")
    generated = {
        COPY_CONTEXT: COPY_CONTEXT_BYTES,
        "package-manifest.json": (json.dumps(manifest, indent=2) + "\n").encode(),
        "package-scope.json": (json.dumps(scope, indent=2) + "\n").encode(),
    }
    return manifest, scope, generated


def _serialize(root, stream, inventory, fingerprints=None):
    from instruction_revision import governance_copy

    governance_copy(root)
    manifest, scope, generated = _metadata(inventory)
    if set(inventory) & set(generated):
        raise ValueError("Package source collides with generated metadata")
    writer = _ForwardWriter(stream)
    with zipfile.ZipFile(writer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        try:
            for name in sorted(set(inventory) | set(generated)):
                data = generated[name] if name in generated else _payload(root, name, inventory[name])
                if fingerprints is not None:
                    errors = inspect_bytes(name, data, fingerprints)
                    if errors:
                        raise ValueError("\n".join(errors))
                info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
                info.create_system = 3
                mode = 0o644 if name in generated else inventory[name]["mode"]
                info.external_attr = (stat.S_IFREG | mode) << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                info.file_size = len(data)
                with archive.open(info, "w") as member:
                    for offset in range(0, len(data), 65536):
                        member.write(data[offset : offset + 65536])
        except BaseException:
            # Closing a failed ZIP emits a partial central directory. Discard that
            # cleanup output so it cannot hide the original inspection/write error.
            writer.discard = True
            raise
    return manifest, scope


def create_archive(root, package, inventory=None):
    """Build a canonical local ZIP from externally captured and rechecked inputs."""
    inventory = source_inventory(root) if inventory is None else inventory
    if hasattr(package, "write"):
        return _serialize(root, package, inventory)
    with Path(package).open("xb") as stream:
        return _serialize(root, stream, inventory)


def inspect_generated_archive(root, package, inventory, fingerprints):
    """Validate every container byte against trusted inputs, with per-payload limits.

    This is only for this process's canonical local build, not arbitrary archives.
    The original recursive inspector still bounds each included payload to 128 MiB.
    Re-serialization rejects hidden compressed suffixes and opaque container fields
    as well as changed names/content/metadata; no extraction precedes this check.
    """
    if source_inventory(root) != inventory:
        raise ValueError("Package input inventory changed before inspection")
    with Path(package).open("rb") as stream:
        _serialize(root, _CompareWriter(stream), inventory, fingerprints)
        if stream.read(1):
            raise ValueError("Trailing package bytes")
    if source_inventory(root) != inventory:
        raise ValueError("Package input inventory changed during inspection")


def archive_sha(package):
    with Path(package).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def extract_archive(package, destination, inventory):
    """Independently parse the inspected ZIP and recover only expected regular files."""
    _, _, generated = _metadata(inventory)
    expected = {
        **inventory,
        **{name: {"sha256": hashlib.sha256(data).hexdigest(), "size": len(data), "mode": 0o644}
           for name, data in generated.items()},
    }
    if destination.is_symlink() or (destination.exists() and any(destination.iterdir())):
        raise ValueError("Package extraction requires a new empty directory")
    destination.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(package) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)) or set(names) != set(expected):
            raise ValueError("Extracted inventory differs from external package inputs")
        for name, row in expected.items():
            _safe_name(name)
            info = archive.getinfo(name)
            if info.file_size != row["size"] or info.external_attr >> 16 != (stat.S_IFREG | row["mode"]):
                raise ValueError("Extracted member size/mode differs: " + name)
            with archive.open(info) as member:
                data = member.read(row["size"] + 1)
            if len(data) != row["size"] or hashlib.sha256(data).hexdigest() != row["sha256"]:
                raise ValueError("Extracted member content differs: " + name)
            target = destination / name
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("xb") as stream:
                stream.write(data)
            target.chmod(row["mode"])
            if target.stat().st_mode & 0o7777 != row["mode"]:
                raise ValueError("Extracted member mode was not restored: " + name)


def main():
    output = ROOT / "dist" / datetime.now(UTC).strftime("%Y%m%dT%H%M%S.%fZ")
    output.mkdir(parents=True, exist_ok=False)
    inventory = source_inventory(ROOT)
    (output / "source-inputs.json").write_text(json.dumps(inventory, indent=2) + "\n")
    (output / "build-runtime.json").write_text(
        json.dumps({"python": sys.version, "zlib": zlib.ZLIB_RUNTIME_VERSION}, indent=2) + "\n"
    )
    errors = inspect_tree(ROOT)
    if errors:
        (output / "inspection-errors.json").write_text(
            json.dumps(errors, indent=2) + "\n"
        )
        print("\n".join(errors))
        return 1
    package = output / PACKAGE_NAME
    manifest, scope = create_archive(ROOT, package, inventory)
    fingerprints = json.loads(
        (
            ROOT
            / "docs/validation/governance-externalization/external-fingerprints.json"
        ).read_text()
    )
    try:
        package_identity = archive_sha(package)
        inspect_generated_archive(ROOT, package, inventory, fingerprints)
        if archive_sha(package) != package_identity:
            raise ValueError("Package changed during canonical inspection")
    except (OSError, ValueError) as exc:
        errors = [str(exc)]
        (output / "inspection-errors.json").write_text(
            json.dumps(errors, indent=2) + "\n"
        )
        print("\n".join(errors))
        return 1
    commands = [
        ["sdd/tools/validate.py", "--root", "."],
        ["sdd/tools/validate.py", "--root", ".", "--structure-only"],
        ["tools/governance/scripts/check-ox.py"],
        ["-m", "unittest", "discover", "-s", "tools/governance/tests", "-v"],
        ["tools/governance/scripts/run-checks.py"],
    ]
    results = []
    with tempfile.TemporaryDirectory(prefix="ox-package-") as temporary:
        extracted = Path(temporary) / "ox"
        extracted.mkdir()
        # Container bytes were matched to trusted inputs before this independent parse.
        extract_archive(package, extracted, inventory)
        actual = {
            p.relative_to(extracted).as_posix(): sha(p)
            for p in extracted.rglob("*")
            if p.is_file()
            and p.relative_to(extracted).as_posix()
            not in {"package-manifest.json", "package-scope.json"}
        }
        if actual != manifest:
            raise ValueError("Extracted inventory differs from package manifest")
        extracted_scope = json.loads((extracted / "package-scope.json").read_text())
        if extracted_scope != scope or scope_errors(extracted_scope):
            raise ValueError("Extracted package scope differs from governance receipt")
        for index, args in enumerate(commands, 1):
            command = [
                sys.executable,
                "tools/governance/scripts/isolated-run.py",
                str(ROOT),
                *args,
            ]
            process = subprocess.run(
                command,
                cwd=extracted,
                env=dict(
                    os.environ,
                    PYTHONDONTWRITEBYTECODE="1",
                    OX_ISOLATION_ORIGIN=str(ROOT),
                ),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )
            log = output / f"{index:02}.log"
            log.write_text(process.stdout)
            results.append(
                {
                    "command": "PYTHONDONTWRITEBYTECODE=1 python3 " + " ".join(args),
                    "exit_code": process.returncode,
                    "log": log.name,
                    "sha256": sha(log),
                }
            )
            print(f"{index}/5 exit={process.returncode}: " + " ".join(args), flush=True)
        # Preserve the runner's new evidence from the disposable extraction.
        observed = output / "extracted-runs"
        observed.mkdir()
        for run in (extracted / "docs/validation/runs").iterdir():
            if not (ROOT / "docs/validation/runs" / run.name).exists():
                import shutil

                shutil.copytree(run, observed / run.name)
    unchanged = source_inventory(ROOT) == inventory
    archive_unchanged = archive_sha(package) == package_identity
    result = {
        **scope,
        "package": package.name,
        "sha256": archive_sha(package),
        "file_count": len(manifest) + 2,
        "archive_inspection": "PASS: canonical bytes from external source inventory; per-payload recursive limits",
        "manifest_and_extraction": "PASS",
        "source_unchanged_during_build": unchanged,
        "archive_unchanged_during_extraction_and_checks": archive_unchanged,
        "source_input_bytes": sum(row["size"] for row in inventory.values()),
        "recursive_payload_limit_bytes": MAX_EXPANDED,
        "results": results,
        "isolation": "Python audit hook rejects original parent and external document reads; not an OS sandbox",
    }
    (output / "results.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    )
    print("Governance package evidence (no application):", output.relative_to(ROOT))
    return int(not unchanged or not archive_unchanged or any(row["exit_code"] for row in results))


if __name__ == "__main__":
    sys.exit(main())
