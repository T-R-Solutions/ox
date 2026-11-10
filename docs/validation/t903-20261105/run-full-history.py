from pathlib import Path
import subprocess,time,json
b=Path(__file__).resolve().parent
while not (b/'followup.json').exists() or not any(x['name']=='matrix-analysis' for x in json.loads((b/'followup.json').read_text())):time.sleep(1)
results=[]
for scale,w,h in [(1,900,700),(1,640,480),(1.5,900,700),(1.5,640,480),(2,900,700),(2,640,480)]:
 for backend in ['native','x11']:
  cmd=['/usr/bin/python3',str(b/'history-journey.py'),f'history-{backend}-{scale}-{w}',backend,str(scale),str(w),str(h)]
  with (b/'full-history.log').open('a') as log:p=subprocess.run(cmd,stdout=log,stderr=log)
  results.append({'command':cmd,'exit':p.returncode});(b/'full-history-batch.json').write_text(json.dumps(results,indent=2)+'\n');print(backend,scale,w,flush=True)
