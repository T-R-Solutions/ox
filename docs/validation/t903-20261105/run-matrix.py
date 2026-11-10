from pathlib import Path
import subprocess,json
b=Path(__file__).resolve().parent
results=[]
for scale,w,h in [(1,900,700),(1,640,480),(1.5,900,700),(1.5,640,480),(2,900,700),(2,640,480)]:
 for backend in ['native','x11']:
  cmd=['/usr/bin/python3',str(b/f'optimized-{backend}.py'),f'optimized-{backend}-{scale}-{w}']+(['--flow','--cell'] if backend=='native' else ['optfull'])+[str(scale),str(w),str(h)]
  with (b/'batch.log').open('a') as log:p=subprocess.run(cmd,stdout=log,stderr=log)
  results.append({'command':cmd,'exit':p.returncode});(b/'batch.json').write_text(json.dumps(results,indent=2)+'\n')
  print(backend,scale,w,p.returncode,flush=True)
