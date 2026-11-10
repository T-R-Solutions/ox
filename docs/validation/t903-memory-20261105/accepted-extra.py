from pathlib import Path
import time,json,subprocess,shutil
b=Path(__file__).resolve().parent;r=b.parents[2]
while not (b/'accepted-environment.json').exists():time.sleep(1)
runs=[]
def run(name,args):
 with (b/(name+'.log')).open('x') as log:p=subprocess.run(['/usr/bin/python3',str(b/args[0]),*args[1:]],stdout=log,stderr=log,cwd=r)
 runs.append({'name':name,'args':args,'exit':p.returncode});(b/'accepted-extra-runs.json').write_text(json.dumps(runs,indent=2)+'\n');print(name,p.returncode,flush=True)
run('accepted-held-x11',['held-x11.py','accepted-held-x11'])
for backend in ['native','x11']:run('accepted-close-'+backend,['execution-close.py','accepted-close-'+backend,backend])

# Inspect application and private session PIDs after all journeys, without signalling
# any preexisting/unknown process. Each journey already observed its own exit.
audit=[]
for p in b.glob('accepted-*/result.json'):
 d=json.loads(p.read_text());pid=d.get('pid')
 if pid:audit.append({'run':p.parent.name,'pid':pid,'present_after_batch':Path(f'/proc/{pid}').exists()})
for p in b.glob('accepted-*/environment.json'):
 d=json.loads(p.read_text())
 for key in ['compositor_pid','bus_pid']:
  if key in d:audit.append({'run':p.parent.name,'role':key,'pid':d[key],'present_after_batch':Path(f'/proc/{d[key]}').exists()})
(b/'process-audit.json').write_text(json.dumps({'observations':audit,'pid_reuse_limit':'Late existence alone cannot identify PID reuse; per-journey exit/readiness observations remain primary.'},indent=2)+'\n')
