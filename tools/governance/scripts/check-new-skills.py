"""Optional upstream skill-creator check of every .codex/skills/<name>/SKILL.md.

Requires already available PyYAML. The skill map lives in sdd/workflow.md#skills.
"""

import importlib.util
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location(
    "quick", root / "tools/governance/scripts/skill-quick-validate.py"
)
quick = importlib.util.module_from_spec(spec)
spec.loader.exec_module(quick)
failed = False
for skill in sorted(p.parent for p in (root / ".codex/skills").glob("*/SKILL.md")):
    ok, message = quick.validate_skill(skill)
    print(skill.name + ": " + message)
    failed |= not ok
sys.exit(failed)
