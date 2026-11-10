from pathlib import Path
import time,json,subprocess,shutil
b=Path(__file__).resolve().parent;r=b.parents[2]
while not (b/'environment.json').exists():time.sleep(1)
runs=[]
def run(name,args):
 with (b/(name+'.log')).open('x') as log:p=subprocess.run(['/usr/bin/python3',str(b/args[0]),*args[1:]],stdout=log,stderr=log,cwd=r)
 runs.append({'name':name,'args':args,'exit':p.returncode});(b/'extra-runs.json').write_text(json.dumps(runs,indent=2)+'\n');print(name,p.returncode,flush=True)
run('visible-history-x11-2-900',['history-journey.py','visible-history-x11-2-900','x11','2','900','700'])
run('held-x11',['held-x11.py','final-held-x11'])
for backend in ['native','x11']:run('close-'+backend,['execution-close.py','final-close-'+backend,backend])
if (b/'final-history-checks.json').exists():shutil.copyfile(b/'final-history-checks.json',b/'pre-extra-history-checks.json')
run('history-analysis-visible',['check-history.py'])
