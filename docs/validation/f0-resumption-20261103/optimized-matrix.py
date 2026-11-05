import subprocess,pathlib,json
b=pathlib.Path(__file__).resolve().parent;results=[]
for scale,w,h in [(1,900,700),(1,640,480),(1.5,900,700),(1.5,640,480),(2,900,700),(2,640,480)]:
 for backend in ['native','x11']:
  if backend=='native':cmd=['/usr/bin/python3',str(b/'optimized-native.py'),f'optimized-native-{scale}-{w}','--flow','--cell',str(scale),str(w),str(h)]
  else:cmd=['/usr/bin/python3',str(b/'optimized-x11.py'),f'optimized-x11-{scale}-{w}','optfull',str(scale),str(w),str(h)]
  p=subprocess.run(cmd);results.append({'command':cmd,'exit':p.returncode})
(b/'optimized-batch.json').write_text(json.dumps(results,indent=2)+'\n')
