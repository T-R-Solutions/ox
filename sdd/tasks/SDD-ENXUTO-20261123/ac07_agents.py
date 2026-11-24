"""AC-07 de SDD-ENXUTO-20261123: 6 perfis, 7 TOML carregados, âncoras existentes no workflow."""
import glob
import re
import tomllib

wf = open("sdd/workflow.md", encoding="utf-8").read()
anchors = {re.sub(r"[^\w\- ]", "", h.strip().lower()).replace(" ", "-") for h in re.findall(r"^#{1,6} (.+)$", wf, re.M)}
profiles = sorted(glob.glob(".codex/agents/*.toml"))
files = profiles + [".codex/config.toml"]
missing = []
for f in files:
    with open(f, "rb") as fh:
        text = tomllib.load(fh).get("developer_instructions", "")
    missing += [(f, a) for a in re.findall(r"#([a-z0-9\-]+)", text) if a not in anchors]
print(f"perfis={len(profiles)} carregados={len(files)} ancoras_ausentes={len(missing)} {missing}")
raise SystemExit(0 if (len(profiles), len(files), missing) == (6, 7, []) else 1)
