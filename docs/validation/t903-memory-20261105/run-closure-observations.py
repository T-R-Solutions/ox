from pathlib import Path
import subprocess,json
b=Path(__file__).resolve().parent;r=b.parents[2];rows=[]
for script in ['run-accepted.py','accepted-postflight.py','accepted-extra.py']:
 with (b/(script+'.log')).open('x') as log:p=subprocess.run(['/usr/bin/python3',str(b/script)],cwd=r,stdout=log,stderr=log)
 rows.append({'script':script,'exit':p.returncode});(b/'closure-observation-runs.json').write_text(json.dumps(rows,indent=2)+'\n');print(script,p.returncode,flush=True)
 if p.returncode:break
