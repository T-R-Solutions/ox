"""Create a new packet identity, refusing to overwrite any prior freeze."""
import hashlib
import json
from pathlib import Path
R=Path(__file__).resolve().parents[3]
B=Path(__file__).resolve().parent
names=set()
for base in [B, R/'docs/validation/persistence-preflight-20261105', R/'.local/build/persistence-experiment-preflight-20261105', R/'tools/governance', R/'sdd/features/product-local-persistence']:
    for p in base.rglob('*'):
        if p.is_file() and '__pycache__' not in p.parts and p.name not in {'freeze.json','freeze.sha256','freeze-verification.log'}:
            names.add(p.relative_to(R).as_posix())
names.update(['README.md','AGENTS.md','sdd/project.md','sdd/workflow.md','sdd/evidence.md','docs/constitution.md','docs/architecture/context.md','docs/structure/files.json','docs/decisions/licensing.md','docs/decisions/local-persistence-experiment-20261105.md','docs/decisions/local-persistence-proposal.md','docs/decisions/readme-skill-integration.md','docs/decisions/readme-preservation.md','docs/decisions/documentation-visuals.md','.codex/skills/software-design/SKILL.md','.codex/skills/database-engineering/SKILL.md'])
# Original README chain remains an independently checked historical mechanism.
for base in ['docs/validation/readme-preservation-20261104','docs/validation/documentation-visuals-20261104']:
    names.update(p.relative_to(R).as_posix() for p in (R/base).rglob('*') if p.is_file())
integration = next(r for r in json.loads((R/'docs/structure/files.json').read_text())['revisions'] if r['id']=='readme-skill-integration-001')
for row in integration['records']:
    names.add(row['destination'])
    if row.get('previous'): names.add(row['previous'])
for source in ['observed-inputs.json','fixture-hashes.json']:
    names.update(row['path'] for row in json.loads((R/'docs/validation/persistence-preflight-20261105'/source).read_text()))
rows=[]
for n in sorted(names):
    p=R/n
    assert not p.is_symlink(), n
    rows.append({'path':n,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size,'role':'local reproduction resource' if n.startswith('.local/') else 'review input, evidence or preserved context'})
d={'schema_version':1,'scope':'T011 pre-execution review only; blocked preparation, no maintainer approval','limitations':['Includes local-only resources; Git-only copy incomplete','Content identity is not authenticity, legal clearance, runtime validation or authorization','Historical evidence remains historical; global freshness failures are retained'],'files':rows}
raw=(json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode()
with (B/'freeze.json').open('xb') as f:f.write(raw)
with (B/'freeze.sha256').open('x') as f:f.write(hashlib.sha256(raw).hexdigest()+'  freeze.json\n')
print(hashlib.sha256(raw).hexdigest(),len(rows))
