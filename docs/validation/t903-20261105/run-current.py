from pathlib import Path
import subprocess,json,os,shutil
b=Path(__file__).resolve().parent;r=b.parents[2];app=r/'application';checks=[]
def run(name,cmd,cwd=r,env=None):
 with (b/(name+'.log')).open('w') as log:p=subprocess.run(cmd,cwd=cwd,env=env,stdout=log,stderr=log)
 checks.append({'name':name,'command':cmd,'cwd':str(cwd),'exit':p.returncode});(b/'current-runs.json').write_text(json.dumps(checks,indent=2)+'\n');print(name,p.returncode,flush=True)
run('current-build',['cargo','build','--workspace','--locked','--offline'],app)
run('current-diagnostic-build',['cargo','build','--workspace','--offline'],Path('/tmp/ox-t903-app'),dict(os.environ,CARGO_TARGET_DIR='/tmp/ox-t903-target'))
run('current-matrix',['/usr/bin/python3',str(b/'run-current-matrix.py')])
for scale,w,h in [(1,900,700),(1,640,480),(1.5,900,700),(1.5,640,480),(2,900,700),(2,640,480)]:
 for backend in ['native','x11']:run(f'current-history-{backend}-{scale}-{w}',['/usr/bin/python3',str(b/'history-journey.py'),f'current-history-{backend}-{scale}-{w}',backend,str(scale),str(w),str(h)])
for backend in ['native','x11']:run('current-fifo-'+backend,['/usr/bin/python3',str(b/'fifo-journey.py'),'current-fifo-'+backend,backend])
run('current-held',['/usr/bin/python3',str(b/'native-held.py'),'current-held'])
run('current-original',['/usr/bin/python3',str(b/'native-session.py'),'current-original','--flow'])
for name,cmd in [('test',['cargo','test','--workspace','--locked','--offline']),('fmt',['cargo','fmt','--all','--','--check']),('clippy',['cargo','clippy','--workspace','--all-targets','--locked','--offline','--','-D','warnings'])]:run('current-'+name,cmd,app)
run('current-matrix-analysis',['/usr/bin/python3',str(b/'check-current.py')])
