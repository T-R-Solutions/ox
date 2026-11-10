from pathlib import Path
import json,subprocess,sys,hashlib,shutil
R=Path.cwd();base=R/'.local/build/toolbox-completion';candidate=base/'candidate';central=Path('/home/rodrigo/Projetos/dev_audit/shared-toolbox');out=R/'docs/validation/toolbox-operational-completion/promotion';out.mkdir(exist_ok=False)
# No approval by exit-only: require all previously observed independent oracles.
for rel in ['real/results.json','real-expanded-r4/results.json','database-lifecycle/results.json','grype-database-lifecycle-r2/results.json','report-rejections/results.json','report-rejections-more/results.json','updated-database-qualification/results.json']:
 rows=json.loads((out.parent/rel).read_text());assert rows and all(row['passed'] for row in rows),rel
assert json.loads((out.parent/'lifecycle/results.json').read_text())['passed']
c=json.loads((out.parent/'concurrent/results.json').read_text());assert c['source_unchanged'] and all(x['passed'] for x in c['operations'])
# Snapshot exact public selection before any central mutation.
def call(label,args):
 r=subprocess.run([str(central/'bin/toolbox'),*args],capture_output=True)
 (out/(label+'.stdout')).write_bytes(r.stdout);(out/(label+'.stderr')).write_bytes(r.stderr)
 if r.returncode:raise RuntimeError(label+' failed: '+str(r.returncode))
 return json.loads(r.stdout)
old=call('catalog-before',['central','list']);assert old=={},'Concurrent central activation; review before promotion'
owned={}
sys.path.insert(0,str(central))
from toolbox.storage import Store
from toolbox.databases import inspect_database,publish_database
store=Store(central/'.local/state',central/'tools');rows=[]
try:
 for tool,version in [('osv-scanner','2.7.0'),('trivy','0.76.2'),('grype','0.119.0')]:
  root=candidate/'tools'/tool/'volume/databases'/version;identity=json.loads((root/'current.json').read_text())['database'];pointer=store.volume(tool)/'databases'/version/'current.json';(out/(tool+'-database-before.json')).write_bytes(pointer.read_bytes())
  stage=store.preparation_dir(tool);shutil.copytree(root/identity,stage/'data')
  active=json.loads((candidate/'tools'/tool/'volume/central/active.json').read_text());record=json.loads((candidate/'tools'/tool/'volume/central/revisions'/(active['revision']+'.json')).read_text())
  selected=publish_database(store,tool,{'version':version},record,stage,{'qualified_by':'toolbox-operational-completion','source_snapshot':identity});assert selected['database']==identity
  (out/(tool+'-database-after.json')).write_text(json.dumps(selected,indent=2))
 for tool in ['ruff','bandit','gitleaks','shellcheck','opengrep','syft','trivy','grype','osv-scanner','yara-x']:
  current=json.loads((candidate/'tools'/tool/'volume/central/active.json').read_text());record_path=candidate/'tools'/tool/'volume/central/revisions'/(current['revision']+'.json');record=json.loads(record_path.read_text())
  registered=call(tool+'-register',['central','register','--tool',tool,'--record',str(record_path)])
  owned[tool]=registered['revision'];(out/'owned-revisions.json').write_text(json.dumps(owned,indent=2))
  active=call(tool+'-activate',['central','activate','--tool',tool,'--revision',registered['revision']])
  assert active['image']==record['id'] and active['version']==record['version']
  rows.append({'tool':tool,**active,'qualified_candidate_revision':current['revision'],'qualified_image_record_sha256':hashlib.sha256(record_path.read_bytes()).hexdigest()});(out/'results.json').write_text(json.dumps(rows,indent=2));print(tool,active['version'],flush=True)
 catalog=call('catalog-after',['central','list']);assert len(catalog)==10
except BaseException:
 subprocess.run([sys.executable,str(base/'recover-central.py')],check=True)
 raise
