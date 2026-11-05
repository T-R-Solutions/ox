import pathlib,subprocess,time,json
b=pathlib.Path(__file__).resolve().parent
deadline=time.monotonic()+600
while not (b/'support-batch.json').exists() and time.monotonic()<deadline:time.sleep(1)
if not (b/'support-batch.json').exists():raise RuntimeError('native support incomplete')
results=[]
for scale,w,h in [(1,900,700),(1,640,480),(1.5,900,700),(1.5,640,480),(2,900,700),(2,640,480)]:
 cmd=['/usr/bin/python3',str(b/'x11-isolated.py'),f'x11-support-{scale}-{w}','full',str(scale),str(w),str(h)]
 p=subprocess.run(cmd);results.append({'command':cmd,'exit':p.returncode})
(b/'x11-support-batch.json').write_text(json.dumps(results,indent=2)+'\n')
