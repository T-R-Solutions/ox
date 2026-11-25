#!/usr/bin/env bash
# AC-12 de SDD-FLUXO-20261124: o Codex carrega .codex/config.toml e os perfis de .codex/agents.
# `codex debug prompt-input` renderiza a entrada do modelo sem executá-lo. Rode da raiz do Ox.
set -euo pipefail
command -v codex >/dev/null || { echo "codex ausente do PATH"; exit 2; }
out=$(mktemp)
trap 'rm -f "$out"' EXIT
codex debug prompt-input >"$out"
python3 -I - "$out" <<'PY'
import json
import sys
import tomllib
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
blob = "\n".join(texts)
errors = 0
config = tomllib.loads(Path(".codex/config.toml").read_text(encoding="utf-8"))
root_ok = any(t.strip() == config["developer_instructions"].strip() for t in texts)
print(f"{'ok' if root_ok else 'FALHA'}  instrução da raiz igual a .codex/config.toml")
errors += not root_ok
agents_ok = "# Instruções operacionais — Ox" in blob
print(f"{'ok' if agents_ok else 'FALHA'}  AGENTS.md carregado")
errors += not agents_ok
profiles = sorted(Path(".codex/agents").glob("*.toml"))
for path in profiles:
    agent = tomllib.loads(path.read_text(encoding="utf-8"))
    expected = (f"{agent['name']}: {{\n{agent['description']}\n- This role's model is set to "
                f"`{agent['model']}` and its reasoning effort is set to `{agent['model_reasoning_effort']}`.")
    ok = expected in blob
    print(f"{'ok' if ok else 'FALHA'}  {agent['name']}: {agent['model']} / {agent['model_reasoning_effort']}")
    errors += not ok
print(f"{len(profiles)} perfil(is); {errors} falha(s)")
sys.exit(1 if errors else 0)
PY
