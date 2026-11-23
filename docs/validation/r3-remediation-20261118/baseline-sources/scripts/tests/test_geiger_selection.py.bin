"""Explicit native selection must not fall back to an unrelated PATH plugin."""

import json
import shutil
import tempfile
import unittest
from pathlib import Path

import support as S


class GeigerSelection(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="ox Geiger selection ; space ")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        shutil.copytree(S.ROOT / "scripts", self.root / "scripts")
        self.catalog_path = self.root / "scripts/config/automation.json"
        self.catalog = json.loads(self.catalog_path.read_text())
        self.relative = self.catalog["checks"]["geiger"]["executable"]["path"]
        self.binary = self.root / self.relative
        self.binary.parent.mkdir(parents=True)
        self.binary.write_text("#!/bin/sh\nexit 71\n")
        self.binary.chmod(0o700)
        self.catalog["checks"]["geiger"]["executable"]["sha256"] = S.digest(self.binary)
        self.path_bin = self.root / "unrelated PATH"
        self.path_bin.mkdir()
        for name in ("cargo-geiger", "cargo-machete"):
            plugin = self.path_bin / name
            plugin.write_text("#!/bin/sh\nexit 99\n")
            plugin.chmod(0o700)
        self.save()

    def save(self):
        self.catalog_path.write_text(json.dumps(self.catalog))

    def select(self, name="geiger", plan=False):
        program = '''ROOT=$OX_TEST_ROOT
SCRIPTS_DIR=$ROOT/scripts
check_properties "$1"
source "$2/lib/backends.sh"
PATH="$3:/usr/bin:/bin"
unset OX_CARGO_BIN OX_TOOLBOX_BIN OX_SCANNER_BACKEND
name=$1
if [[ $4 == plan ]]; then
    plan=true; legacy=false; backend_plan; json_args "${CMD[@]}"
elif select_backend; then
    jq -n --arg path "$TOOL_BIN" '{path:$path}'
else
    jq -n --arg reason "$BACKEND_REASON" '{reason:$reason}'
fi
'''
        return json.loads(S.shell(
            program, name, S.ROOT / "scripts", self.path_bin,
            "plan" if plan else "run", root=self.root,
        ))

    def test_explicit_selection_precedes_path_and_other_plugin_keeps_path(self):
        self.assertEqual(self.select(), {"path": str(self.binary)})
        self.assertEqual(self.select("machete"), {"path": str(self.path_bin / "cargo-machete")})

    def test_missing_binary_blocks_instead_of_path_fallback(self):
        self.binary.unlink()
        self.assertIn("missing", self.select()["reason"])

    def test_changed_binary_blocks_instead_of_path_fallback(self):
        self.binary.write_text("#!/bin/sh\nexit 0\n")
        self.assertIn("digest mismatch", self.select()["reason"])

    def test_nonexecutable_and_directory_are_rejected(self):
        self.binary.chmod(0o600)
        self.assertIn("not executable", self.select()["reason"])
        self.binary.unlink()
        self.binary.mkdir()
        self.assertIn("not executable", self.select()["reason"])

    def test_file_and_parent_symlinks_are_rejected(self):
        real = self.root / "real-plugin"
        self.binary.rename(real)
        self.binary.symlink_to(real)
        self.assertIn("unsafe", self.select()["reason"])
        self.binary.unlink()
        real.rename(self.binary)
        (self.root / "alias").symlink_to(self.binary.parent, target_is_directory=True)
        self.catalog["checks"]["geiger"]["executable"]["path"] = "alias/cargo-geiger"
        self.save()
        self.assertIn("unsafe", self.select()["reason"])

    def test_pure_plan_declares_selection_without_needing_installed_binary(self):
        self.binary.unlink()
        argv = self.select(plan=True)
        self.assertEqual(argv[0], str(self.binary))
        self.assertIn("--locked", argv)
        self.assertIn("--offline", argv)

    def test_invalid_catalog_selection_is_rejected(self):
        valid = self.catalog["checks"]["geiger"]["executable"].copy()
        for selection in (
            None, [], {}, {**valid, "extra": True}, {**valid, "sha256": "bad"},
            {**valid, "path": str(self.root / "plugin")}, {**valid, "path": "../plugin"},
            {**valid, "path": "./plugin"}, {**valid, "path": "a//plugin"},
            {**valid, "path": "a/../plugin"}, {**valid, "path": "a\nplugin"},
        ):
            with self.subTest(selection=selection):
                self.catalog["checks"]["geiger"]["executable"] = selection
                self.save()
                with S.rejected(self, returncode=2, message="Invalid automation catalog schema"):
                    self.select()

    def test_toolbox_selection_cannot_declare_native_executable(self):
        self.catalog["checks"]["ruff"]["executable"] = self.catalog["checks"]["geiger"]["executable"]
        self.save()
        with S.rejected(self, returncode=2, message="Invalid automation catalog schema"):
            self.select("ruff")

    def test_runner_rejects_binary_changed_after_selection(self):
        common = self.root / "scripts/lib/common.sh"
        # Deterministic fixture: the first hash returns the selected bytes while
        # replacing the file. The runner's later captured identity must match pin.
        with common.open("a") as stream:
            stream.write('''
hash_file() {
    local digest
    digest=$(sha256sum <"$1") || return 1
    if [[ $1 == "$ROOT/"*cargo-geiger && ! -e $ROOT/replaced ]]; then
        printf '#!/bin/sh\\nexit 72\\n' >"$1"
        touch "$ROOT/replaced"
    fi
    printf '%s' "${digest:0:64}"
}
''')
        active = self.root / "active"
        active.mkdir()
        (active / ".owner").write_text("ox-local-v2\n")
        output = active / "geiger"
        output.mkdir()
        S.shell('''export OX_ACTIVE_RUN=$1
if bash "$2/scripts/checks/run.sh" --root "$2" --check geiger --output "$1/geiger"; then
    exit 1
fi
''', active, self.root)
        result = json.loads((output / "assessment.json").read_text())
        self.assertEqual(result["state"], "blocked")
        self.assertEqual(result["reason"], "Configured native executable changed after selection")
        self.assertIsNone(result["tool_exit_code"])
        self.assertTrue((self.root / "replaced").is_file())
