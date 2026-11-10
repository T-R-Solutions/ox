from pathlib import Path
import json,sys
R=Path('/home/rodrigo/Projetos/ox');out=R/'docs/validation/toolbox-operational-completion/promotion';central=Path('/home/rodrigo/Projetos/dev_audit/shared-toolbox');sys.path.insert(0,str(central))
from toolbox.storage import Store,atomic_json
from toolbox.native import central_lock
store=Store(central/'.local/state',central/'tools');owned=json.loads((out/'owned-revisions.json').read_text()) if (out/'owned-revisions.json').exists() else {}
for tool,revision in owned.items():
 pointer=store.volume(tool)/'central/active.json'
 with central_lock(store,tool,'activation'):
  if pointer.exists():
   active=json.loads(pointer.read_text())
   if active['revision']!=revision:raise RuntimeError('Concurrent central selection; recovery needs review: '+tool)
   atomic_json(out/(tool+'-recovered-active.json'),active);pointer.unlink()
for tool,version in [('osv-scanner','2.7.0'),('trivy','0.76.2'),('grype','0.119.0')]:
 before=out/(tool+'-database-before.json');after=out/(tool+'-database-after.json')
 if before.exists() and after.exists():
  pointer=store.volume(tool)/'databases'/version/'current.json'
  if json.loads(pointer.read_text())['database']!=json.loads(after.read_text())['database']:raise RuntimeError('Concurrent DB selection; recovery needs review: '+tool)
  atomic_json(pointer,json.loads(before.read_text()))
atomic_json(out/'recovered.json',{'recovered':True,'previous_active_catalog':{}})
