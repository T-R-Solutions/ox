from pathlib import Path
import subprocess,json,time,sys,os,hashlib
b=Path(__file__).resolve().parent;r=b.parents[2];phase=sys.argv[1];rows=[]
commands=[('structure',['python3','sdd/tools/validate.py','--root','.','--structure-only']),('freshness',['python3','sdd/tools/validate.py','--root','.','--require-fresh']),('governance',['python3','tools/governance/scripts/run-checks.py']),('whitespace',['git','diff','--check'])]
if phase=='closure':
 commands=[(name,(['python3','tools/governance/scripts/check-ox.py'] if name=='governance' else cmd)) for name,cmd in commands]
 commands.append(('maintenance',['python3','tools/governance/scripts/verify-maintenance.py']))
if phase=='closure':commands.append(('acceptance',['python3',str(b/'acceptance.py')]))
for name,cmd in commands:
 start=time.monotonic();p=b/(phase+'-'+name+'.log')
 with p.open('x') as log:result=subprocess.run(cmd,cwd=r,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),stdout=log,stderr=log)
 rows.append({'name':name,'command':cmd,'exit':result.returncode,'log':str(p.relative_to(r)),'seconds':time.monotonic()-start,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()});(b/('checks-'+phase+'.json')).write_text(json.dumps(rows,indent=2)+'\n');print(phase,name,result.returncode,flush=True)
(b/'checks.json').write_text(json.dumps({'phase':phase,'checks':rows,'scope':'governance and integrity, not independent graphical effectiveness'},indent=2)+'\n')
