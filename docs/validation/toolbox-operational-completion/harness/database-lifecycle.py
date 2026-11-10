from pathlib import Path
import sys,json,subprocess,os,shutil,hashlib
R=Path.cwd();base=R/'.local/build/toolbox-completion';candidate=base/'candidate';sys.path.insert(0,str(candidate))
from toolbox.storage import Store,atomic_json
from toolbox.databases import publish_database,inspect_database,public_data_metadata
store=Store(candidate/'.local/state',candidate/'tools');out=R/'docs/validation/toolbox-operational-completion/database-lifecycle';out.mkdir(exist_ok=False);rows=[]
for name,version in [('osv-scanner','2.7.0'),('trivy','0.76.2')]:
 pointer=store.volume(name)/'databases'/version/'current.json';prior=pointer.read_bytes();identity=json.loads(prior)['database'];db=inspect_database(store,name,version,identity)
 record=json.loads((candidate/'tools'/name/'volume/central/active.json').read_text());record['id']=record['image']
 for mode in ['missing','corrupt','inconsistent','expired']:
  dest=out/(name+'-'+mode);dest.mkdir();stage=store.preparation_dir(name)
  try:
   if mode=='missing':atomic_json(pointer,{'database':'0'*64})
   elif mode=='corrupt':
    atomic_json(pointer,{'database':'f'*64})
    fake=store.database(name,version,'f'*64);fake.mkdir();(fake/'corrupt').write_text('controlled corrupted snapshot')
    atomic_json(fake.parent/('f'*64+'.json'),{'tool':name,'version':version,'id':'f'*64})
   else:
    # CoW keeps immutable originals unchanged and gives each negative fixture private bytes.
    subprocess.run(['cp','-a','--reflink=auto',db['path'],str(stage/'data')],check=True)
    if name=='osv-scanner':
     receipt=stage/'data/toolbox-osv-sources.json';sources=json.loads(receipt.read_text())
     if mode=='expired':
      for source in sources:source['data_timestamp']='2000-01-01T00:00:00Z'
     else:sources[0]['sha256']='0'*64
     receipt.write_text(json.dumps(sources))
    else:
     metadata=stage/'data/db/metadata.json';native=json.loads(metadata.read_text());native['UpdatedAt']='2000-01-01T00:00:00Z' if mode=='expired' else '2099-01-01T00:00:00Z';metadata.write_text(json.dumps(native))
    published=publish_database(store,name,{'version':version},record,stage,{'purpose':'controlled negative fixture '+mode});(dest/'publication.json').write_text(json.dumps(published,indent=2))
   argv=['scan','source','--offline','--format','json','--all-packages','--lockfile','package-lock.json'] if name=='osv-scanner' else ['fs','--scanners','vuln','--offline-scan','--skip-db-update','--skip-java-db-update','--format','json','--exit-code','1','/project']
   command=[str(R/'scripts/toolbox.sh'),'exec','--tool',name,'--project-root',str(base/'fixtures'),'--results',str(dest),'--timeout','120','--diagnostic-file',str(dest/'execution.json'),'--',*argv]
   run=subprocess.run(command,capture_output=True,env=dict(os.environ,TOOLBOX_BIN=str(candidate/'bin/toolbox')))
   (dest/'stdout').write_bytes(run.stdout);(dest/'stderr').write_bytes(run.stderr)
   diagnostic=json.loads((dest/'execution.json').read_text())
   if mode=='expired':
    verdict=subprocess.run(['bash','-c','source scripts/lib/backends.sh; validate_database_age "$1" "$2"','age',str(dest/'execution.json'),'osv' if name=='osv-scanner' else 'trivy'],capture_output=True);passed=verdict.returncode!=0
   else:passed=diagnostic['outcome']=='infrastructure' and run.returncode!=0
   rows.append({'tool':name,'case':mode,'command':command,'exit':run.returncode,'outcome':diagnostic['outcome'],'passed':passed})
  finally:
   pointer.write_bytes(prior)
   recovered=inspect_database(store,name,version,json.loads(pointer.read_text())['database']);assert recovered['database']==identity
  (out/'results.json').write_text(json.dumps(rows,indent=2));print(name,mode,passed,flush=True)
