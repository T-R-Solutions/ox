"""Generated-container identity is external; recursive payload limits stay fixed."""

import hashlib
import importlib.util
import json
import os
import struct
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
SPEC = importlib.util.spec_from_file_location("package_inventory_subject", SCRIPTS / "package-ox.py")
P = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(P)


class PackageInventoryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="ox-package-inventory-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "source"
        self.root.mkdir()
        for name in P.distribution_files(self.root):
            name.parent.mkdir(parents=True, exist_ok=True)
            name.write_bytes(b"fixture\n")
        self.payload = self.root / "docs/sample.bin"
        self.payload.parent.mkdir(exist_ok=True)
        self.payload.write_bytes(b"payload\n")
        (self.root / "scripts/automate.sh").chmod(0o755)
        self.package = self.root.parent / "package.zip"

    def build(self):
        self.inventory = P.source_inventory(self.root)
        return P.create_archive(self.root, self.package, self.inventory)

    def inspect(self):
        P.inspect_generated_archive(self.root, self.package, self.inventory, {})

    def test_canonical_roundtrip_uses_external_inventory_and_regular_members(self):
        manifest, scope = self.build()
        self.inspect()
        destination = self.root.parent / "extracted"
        with zipfile.ZipFile(self.package) as archive:
            self.assertEqual(len(archive.namelist()), len(set(archive.namelist())))
            self.assertEqual(set(archive.namelist()), set(manifest) | {"package-manifest.json", "package-scope.json"})
            for info in archive.infolist():
                mode = 0o755 if info.filename == "scripts/automate.sh" else 0o644
                self.assertEqual(info.external_attr >> 16, 0o100000 | mode)
        P.extract_archive(self.package, destination, self.inventory)
        actual = {
            p.relative_to(destination).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in destination.rglob("*") if p.is_file()
            and p.name not in {"package-manifest.json", "package-scope.json"}
        }
        self.assertEqual(actual, manifest)
        self.assertEqual(json.loads((destination / "package-scope.json").read_text()), scope)
        self.assertFalse(scope["product_included"])
        self.assertIn("task_finalizada.md", actual)
        self.assertEqual((destination / "scripts/automate.sh").stat().st_mode & 0o7777, 0o755)
        self.assertEqual((destination / "docs/sample.bin").stat().st_mode & 0o7777, 0o644)
        self.assertTrue(os.access(destination / "scripts/automate.sh", os.X_OK))

    def test_source_mode_drift_and_privileged_bits_are_rejected(self):
        self.build()
        self.payload.chmod(0o755)
        with self.assertRaisesRegex(ValueError, "inventory changed"):
            self.inspect()
        self.payload.chmod(0o4644)
        with self.assertRaisesRegex(ValueError, "privileged"):
            P.source_inventory(self.root)

    def test_product_boundary_is_exact_and_preserves_task_log(self):
        excluded = ("sdd/features/product-ide-shell/spec.md", "docs/validation/ide-shell-20261118/evidence.json", "docs/design/ide-shell.md")
        retained = ("docs/design/ide-shell.md.unrelated", "docs/validation/ide-shell-20261118-other/evidence.json", "sdd/features/product-ide-shell-other/spec.md")
        for name in excluded + retained:
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("fixture\n")
        paths = {p.relative_to(self.root).as_posix() for p in P.distribution_files(self.root)}
        self.assertTrue(set(excluded).isdisjoint(paths))
        self.assertTrue(set(retained).issubset(paths))
        self.assertIn("task_finalizada.md", paths)

    def test_archive_mode_corruption_and_nonempty_extraction_fail(self):
        self.build()
        original = bytearray(self.package.read_bytes())
        with zipfile.ZipFile(self.package) as archive:
            target = archive.getinfo("scripts/automate.sh")
        cursor = original.find(b"PK\x01\x02")
        while original[cursor:cursor + 4] == b"PK\x01\x02":
            offset = struct.unpack_from("<I", original, cursor + 42)[0]
            if offset == target.header_offset:
                struct.pack_into("<I", original, cursor + 38, 0o100644 << 16)
                break
            cursor += 46 + sum(struct.unpack_from("<HHH", original, cursor + 28))
        else:
            self.fail("Executable central entry not found")
        self.package.write_bytes(original)
        with self.assertRaises(ValueError):
            self.inspect()
        with self.assertRaisesRegex(ValueError, "size/mode"):
            P.extract_archive(self.package, self.root.parent / "corrupt-extraction", self.inventory)
        with self.assertRaisesRegex(ValueError, "empty directory"):
            P.extract_archive(self.package, self.root, self.inventory)

    def test_aggregate_over_128_mib_accepts_individually_bounded_payloads(self):
        for index in range(2):
            path = self.root / f"docs/large-{index}.bin"
            with path.open("wb") as stream:
                for _ in range(68):
                    stream.write(b"x" * (1024 * 1024))
        self.build()
        self.assertGreater(sum(row["size"] for row in self.inventory.values()), P.MAX_EXPANDED)
        self.inspect()

    def test_individual_payload_budget_is_not_relaxed(self):
        with self.payload.open("wb") as stream:
            stream.truncate(P.MAX_EXPANDED + 1)
        with self.assertRaisesRegex(ValueError, "inspection limit"):
            self.build()

    def test_nested_archive_expansion_budget_is_not_relaxed(self):
        self.payload.unlink()
        nested = self.root / "docs/nested.zip"
        with zipfile.ZipFile(nested, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            with archive.open("expanded.bin", "w") as stream:
                for _ in range(129):
                    stream.write(b"x" * (1024 * 1024))
        self.build()
        with self.assertRaisesRegex(ValueError, "inspection limit"):
            self.inspect()

    def test_changed_source_and_inventory_fail_closed(self):
        self.build()
        original = self.payload.read_bytes()
        self.payload.write_bytes(b"changed\n")
        with self.assertRaisesRegex(ValueError, "inventory changed"):
            self.inspect()
        self.payload.write_bytes(original)
        (self.root / "docs/added.bin").write_bytes(b"new")
        with self.assertRaisesRegex(ValueError, "inventory changed"):
            self.inspect()

    def test_symlink_and_unsafe_inventory_are_rejected(self):
        self.payload.unlink()
        self.payload.symlink_to(self.root / "README.md")
        with self.assertRaisesRegex(ValueError, "Symlink"):
            self.build()
        self.payload.unlink()
        self.payload.write_bytes(b"payload\n")
        self.build()
        for name in ("../escape", "/absolute", "C:/absolute", "C:relative", "docs/.git/config", "docs\\escape", "package-scope.json"):
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, "Unsafe package path|Reserved package path"):
                P._safe_source(self.root, name)

    def test_container_prefix_suffix_metadata_missing_duplicate_and_extra_rejected(self):
        self.build()
        original = self.package.read_bytes()
        for content in (b"PREFIX" + original, original + b"SUFFIX", original[:-1]):
            self.package.write_bytes(content)
            with self.subTest(kind="framing"), self.assertRaises(ValueError):
                self.inspect()
        self.package.write_bytes(original)
        with zipfile.ZipFile(self.package) as archive:
            entries = [(info.filename, archive.read(info)) for info in archive.infolist()]
        for kind in ("missing", "duplicate", "extra", "scope"):
            rows = list(entries)
            if kind == "missing":
                rows.pop()
            elif kind == "duplicate":
                rows.append(rows[0])
            elif kind == "extra":
                rows.append(("unexpected", b"data"))
            else:
                rows = [(name, b"{}\n" if name == "package-scope.json" else data) for name, data in rows]
            with zipfile.ZipFile(self.package, "w", compression=zipfile.ZIP_DEFLATED) as archive:
                for name, data in rows:
                    archive.writestr(name, data)
            with self.subTest(kind=kind), self.assertRaises(ValueError):
                self.inspect()

    def test_deflate_unused_suffix_rejected_even_when_zipfile_accepts_plaintext(self):
        self.build()
        data = bytearray(self.package.read_bytes())
        with zipfile.ZipFile(self.package) as archive:
            first = archive.infolist()[0]
            expected = {info.filename: archive.read(info) for info in archive.infolist()}
        local = first.header_offset
        name_length, extra_length = struct.unpack_from("<HH", data, local + 26)
        insert = local + 30 + name_length + extra_length + first.compress_size
        suffix = b"HIDDEN-AFTER-DEFLATE-EOF"
        eocd = data.rfind(b"PK\x05\x06")
        central = struct.unpack_from("<I", data, eocd + 16)[0]
        cursor = central
        while data[cursor:cursor + 4] == b"PK\x01\x02":
            header_offset = struct.unpack_from("<I", data, cursor + 42)[0]
            if header_offset == local:
                struct.pack_into("<I", data, cursor + 20, first.compress_size + len(suffix))
            elif header_offset >= insert:
                struct.pack_into("<I", data, cursor + 42, header_offset + len(suffix))
            lengths = struct.unpack_from("<HHH", data, cursor + 28)
            cursor += 46 + sum(lengths)
        self.assertEqual(data[insert:insert + 4], b"PK\x07\x08")
        struct.pack_into("<I", data, insert + 8, first.compress_size + len(suffix))
        struct.pack_into("<I", data, eocd + 16, central + len(suffix))
        data[insert:insert] = suffix
        self.package.write_bytes(data)
        with zipfile.ZipFile(self.package) as archive:
            self.assertIsNone(archive.testzip())
            self.assertEqual({info.filename: archive.read(info) for info in archive.infolist()}, expected)
        with self.assertRaises(ValueError):
            self.inspect()


if __name__ == "__main__":
    unittest.main()
