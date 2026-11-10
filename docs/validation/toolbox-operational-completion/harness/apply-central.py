from pathlib import Path
import json,hashlib
root=Path('/home/rodrigo/Projetos/ox');base=root/'.local/build/toolbox-completion';central=Path('/home/rodrigo/Projetos/dev_audit/shared-toolbox');checks=json.loads((base/'central-preconditions.json').read_text())
for rel,expected in checks.items():
 p=central/rel;actual=hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None
 if actual!=expected:raise RuntimeError('Concurrent modification: '+rel)
for rel in checks:
 p=central/rel;p.write_bytes((base/'candidate'/rel).read_bytes())
print('Applied bounded public data provenance contract; no images activated or databases selected')
