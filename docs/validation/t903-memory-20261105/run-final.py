from pathlib import Path
import subprocess,json,time,os,hashlib
b=Path(__file__).resolve().parent;r=b.parents[2];runs=[]
def run(name,cmd,cwd=r,env=None):
 start=time.monotonic()
 with (b/(name+'.log')).open('x') as log:p=subprocess.run(cmd,cwd=cwd,env=env,stdout=log,stderr=log)
 runs.append({'name':name,'command':cmd,'cwd':str(cwd),'exit':p.returncode,'seconds':time.monotonic()-start});(b/'final-runs.json').write_text(json.dumps(runs,indent=2)+'\n');print(name,p.returncode,flush=True)
# Serial measurements: no overlapping builds or profilers.
for scale,w,h in [(2,900,700),(1,900,700),(1,640,480),(1.5,900,700),(1.5,640,480),(2,640,480)]:
 for backend in ['native','x11']:
  run(f'final-history-{backend}-{scale}-{w}',['/usr/bin/python3',str(b/'history-journey.py'),f'final-history-{backend}-{scale}-{w}',backend,str(scale),str(w),str(h)])
  run(f'final-flow-{backend}-{scale}-{w}',['/usr/bin/python3',str(b/f'optimized-{backend}.py'),f'final-flow-{backend}-{scale}-{w}']+(['--flow','--cell'] if backend=='native' else ['optfull'])+[str(scale),str(w),str(h)])
for backend in ['native','x11']:run('final-fifo-'+backend,['/usr/bin/python3',str(b/'fifo-journey.py'),'final-fifo-'+backend,backend])
run('final-held',['/usr/bin/python3',str(b/'native-held.py'),'final-held'])
run('build',['cargo','build','--workspace','--locked','--offline'],r/'application')
run('backend',['/usr/bin/time','-v',str(r/'application/target/debug/examples/f0_measure'),str(r/'application/target/debug'),str(b/'backend-workspace')])
for i in range(3):run('large-'+str(i),['/usr/bin/time','-v',str(r/'application/target/debug/examples/history_measure'),str(b/f'large-history-{i}'),str(r/'application/target/debug/task-oracle')])
run('original-native',['/usr/bin/python3',str(b/'native-session.py'),'final-original','--flow'])
