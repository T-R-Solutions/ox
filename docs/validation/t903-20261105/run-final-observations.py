from pathlib import Path
import subprocess,json,time
b=Path(__file__).resolve().parent;r=b.parents[2];app=r/'application'
while not (b/'full-history-batch.json').exists() or len(json.loads((b/'full-history-batch.json').read_text()))<12:time.sleep(1)
checks=[]
for name,cmd in [('fifo-x11-repaired',['/usr/bin/python3',str(b/'fifo-journey.py'),'fifo-x11-repaired','x11']),('backend-direct',['/usr/bin/time','-v',str(app/'target/debug/examples/f0_measure'),str(app/'target/debug'),str(b/'backend-direct-workspace')])]:
 with (b/(name+'.log')).open('w') as log:p=subprocess.run(cmd,stdout=log,stderr=log)
 checks.append({'name':name,'command':cmd,'exit':p.returncode});(b/'final-observations.json').write_text(json.dumps(checks,indent=2)+'\n');print(name,p.returncode,flush=True)
