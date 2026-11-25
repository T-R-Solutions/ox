#!/usr/bin/env bash
# AC-13 de SDD-FLUXO-20261124 (r2): o AGENTS.md que o Codex carrega pede subagentes nos casos da
# triagem, e o link aponta para um título existente do workflow. `codex debug prompt-input`
# renderiza a entrada do modelo sem executá-lo. Rode da raiz do Ox.
set -euo pipefail
command -v codex >/dev/null || { echo "codex ausente do PATH"; exit 2; }
out=$(mktemp)
trap 'rm -f "$out"' EXIT
codex debug prompt-input >"$out"
python3 -I - "$out" <<'PY'
import json
import re
import sys
from pathlib import Path

texts: list[str] = []


def walk(node):
    if isinstance(node, dict):
        for value in node.values():
            walk(value)
    elif isinstance(node, list):
        for value in node:
            walk(value)
    elif isinstance(node, str):
        texts.append(node)


walk(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")))
loaded = next((t for t in texts if "# Instruções operacionais — Ox" in t), "")
flat = " ".join(loaded.split())
checks = {
    "AGENTS.md carregado": bool(loaded),
    "pedido explícito de subagentes": "Use subagentes nos casos definidos pela" in flat,
    "link para a triagem": "[triagem do Ox](sdd/workflow.md#triagem)" in flat,
    "título Triagem no workflow": bool(re.search(r"^### Triagem\s*$", Path("sdd/workflow.md").read_text(encoding="utf-8"), re.M)),
}
for name, ok in checks.items():
    print(f"{'ok' if ok else 'FALHA'}  {name}")
failures = sum(not ok for ok in checks.values())
print(f"{failures} falha(s)")
sys.exit(1 if failures else 0)
PY
