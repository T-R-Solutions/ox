from pathlib import Path
import json,subprocess,time
b=Path(__file__).resolve().parent
while not (b/'current-runs.json').exists() or not any(x['name']=='current-matrix-analysis' for x in json.loads((b/'current-runs.json').read_text())):time.sleep(1)
results=[]
for scale,w,h in [(1,900,700),(1,640,480),(1.5,900,700),(1.5,640,480),(2,900,700),(2,640,480)]:
 p=b/f'current-optimized-native-{scale}-{w}/result.json';d=json.loads(p.read_text())
 if 'error' in d:
  cmd=['/usr/bin/python3',str(b/'optimized-native.py'),f'current-replay-native-{scale}-{w}','--flow','--cell',str(scale),str(w),str(h)]
  with (b/'replays.log').open('a') as log:r=subprocess.run(cmd,stdout=log,stderr=log)
  results.append({'command':cmd,'exit':r.returncode})
(b/'replays.json').write_text(json.dumps(results,indent=2)+'\n')
with (b/'current-final-analysis.log').open('w') as log:p=subprocess.run(['/usr/bin/python3',str(b/'check-current.py')],stdout=log,stderr=log)
print('final matrix analysis',p.returncode,flush=True)
