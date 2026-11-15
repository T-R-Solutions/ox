"""Optional upstream skill-creator check; requires already available PyYAML."""

import importlib.util
import json
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location(
    "quick", root / "tools/governance/scripts/skill-quick-validate.py"
)
quick = importlib.util.module_from_spec(spec)
spec.loader.exec_module(quick)
failed = False
for name in json.loads((root / "config/governance/profile.json").read_text())["new"]:
    ok, message = quick.validate_skill(root / ".codex/skills" / name)
    print(name + ": " + message)
    failed |= not ok
sys.exit(failed)
