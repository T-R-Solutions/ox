#!/usr/bin/env python3
"""AC-07 de SDD-AJUSTES-20261124: pins de reviews.static iguais aos bytes atuais.

Somente leitura; rode da raiz do Ox. Arquivo pinado ausente conta como divergência.
"""
import hashlib
import json
import sys
from pathlib import Path

config = json.loads(Path("scripts/config/automation.json").read_text(encoding="utf-8"))
static = config["reviews"]["static"]
pins = {**static["sources"], **static["policy_files"]}
diverge = 0
for path, pinned in sorted(pins.items()):
    target = Path(path)
    current = hashlib.sha256(target.read_bytes()).hexdigest() if target.is_file() else "ausente"
    if current != pinned:
        diverge += 1
        print(f"DIVERGE {path}: pin={pinned[:12]} atual={current[:12]}")
reason = static.get("reason", "")
if "SDD-AJUSTES-20261124" not in reason:
    diverge += 1
    print("DIVERGE reason: revisão SDD-AJUSTES-20261124 não registrada")
print(f"{len(pins)} pin(s); {diverge} divergência(s)")
sys.exit(1 if diverge else 0)
