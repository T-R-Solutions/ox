from pathlib import Path
import subprocess,json,time,os,hashlib
b=Path(__file__).resolve().parent;r=b.parents[2];runs=[]
def run(name,cmd,cwd=r,env=None):
 start=time.monotonic()
 with (b/(name+'.log')).open('x') as log:p=subprocess.run(cmd,cwd=cwd,env=env,stdout=log,stderr=log)
 runs.append({'name':name,'command':cmd,'cwd':str(cwd),'exit':p.returncode,'seconds':time.monotonic()-start});(b/'accepted-runs.json').write_text(json.dumps(runs,indent=2)+'\n');print(name,p.returncode,flush=True)
# Serial measurements: no overlapping builds or profilers.
for scale,w,h in [(2,900,700),(1,900,700),(1,640,480),(1.5,900,700),(1.5,640,480),(2,640,480)]:
 for backend in ['native','x11']:
  run(f'accepted-history-{backend}-{scale}-{w}',['/usr/bin/python3',str(b/'history-journey.py'),f'accepted-history-{backend}-{scale}-{w}',backend,str(scale),str(w),str(h)])
  run(f'accepted-flow-{backend}-{scale}-{w}',['/usr/bin/python3',str(b/f'optimized-{backend}.py'),f'accepted-flow-{backend}-{scale}-{w}']+(['--flow','--cell'] if backend=='native' else ['optfull'])+[str(scale),str(w),str(h)])
for backend in ['native','x11']:run('accepted-fifo-'+backend,['/usr/bin/python3',str(b/'fifo-journey.py'),'accepted-fifo-'+backend,backend])
run('accepted-held',['/usr/bin/python3',str(b/'native-held.py'),'accepted-held'])
run('accepted-build-product',['cargo','build','--workspace','--locked','--offline'],r/'application')
run('accepted-original-native',['/usr/bin/python3',str(b/'native-session.py'),'accepted-original','--flow'])
