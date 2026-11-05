"""Run ordinary local checks after graphical measurements have finished."""
from pathlib import Path
import subprocess,json,time,datetime
B=Path(__file__).resolve().parent;R=B.parents[2]
# The caller starts this only after the serial graphics batch completes.
assert (B/'optimized-batch.json').is_file()
checks=[]
commands=[('reproduction',['python3',str(B/'prepare-optimized.py')],R),('fmt',['cargo','fmt','--all','--','--check'],R/'application'),('check',['cargo','check','--workspace','--locked','--offline'],R/'application'),('test',['cargo','test','--workspace','--locked','--offline'],R/'application'),('clippy',['cargo','clippy','--workspace','--all-targets','--locked','--offline','--','-D','warnings'],R/'application'),('backend',['/usr/bin/time','-v','cargo','run','-p','ox-ui','--example','f0_measure','--locked','--offline','--',str(R/'application/target/debug'),str(B/'optimized-backend-workspace')],R/'application')]
for name,cmd,cwd in commands:
 path=B/f'optimized-product-{name}.log';assert not path.exists(),path
 start=time.monotonic()
 with path.open('w') as log:p=subprocess.run(cmd,cwd=cwd,stdout=log,stderr=log)
 checks.append({'name':name,'command':cmd,'cwd':str(cwd),'exit':p.returncode,'seconds':time.monotonic()-start,'log':path.name});print(name,p.returncode,flush=True)
(B/'optimized-product-checks.json').write_text(json.dumps({'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':checks},indent=2)+'\n')
assert all(x['exit']==0 for x in checks)
