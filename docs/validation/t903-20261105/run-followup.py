from pathlib import Path
import subprocess,json,time,os
b=Path(__file__).resolve().parent;r=b.parents[2]
while not (b/'batch.json').exists() or len(json.loads((b/'batch.json').read_text()))<12:time.sleep(1)
checks=[]
def run(name,cmd,cwd=r,env=None):
 start=time.monotonic()
 with (b/(name+'.log')).open('w') as log:p=subprocess.run(cmd,cwd=cwd,env=env,stdout=log,stderr=log)
 checks.append({'name':name,'command':cmd,'cwd':str(cwd),'exit':p.returncode,'seconds':time.monotonic()-start});(b/'followup.json').write_text(json.dumps(checks,indent=2)+'\n');print(name,p.returncode,flush=True)
for backend in ['native','x11']:run('fifo-'+backend,['/usr/bin/python3',str(b/'fifo-journey.py'),'fifo-'+backend,backend])
run('native-held',['/usr/bin/python3',str(b/'native-held.py'),'native-held-current'])
app=r/'application'
run('product-build',['cargo','build','--workspace','--locked','--offline'],app)
run('backend',['/usr/bin/time','-v','cargo','run','-p','ox-ui','--example','f0_measure','--locked','--offline','--',str(app/'target/debug'),str(b/'backend-workspace')],app)
for i in range(3):run('history-'+str(i),['/usr/bin/time','-v','cargo','run','-p','ox-verification','--example','history_measure','--locked','--offline','--',str(b/f'large-history-{i}'),str(app/'target/debug/task-oracle')],app)
run('focused-tests',['cargo','test','-p','ox-ui','-p','ox-verification','--locked','--offline'],app)
run('fmt',['cargo','fmt','--all','--','--check'],app)
run('clippy',['cargo','clippy','-p','ox-ui','-p','ox-verification','--all-targets','--locked','--offline','--','-D','warnings'],app)
run('matrix-analysis',['/usr/bin/python3',str(b/'check-optimized.py')])
