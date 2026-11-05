import pathlib,subprocess,time,json
b=pathlib.Path(__file__).resolve().parent
deadline=time.monotonic()+900
while not (b/'x11-metrics-2-640/result.json').exists() and time.monotonic()<deadline:time.sleep(1)
if not (b/'x11-metrics-2-640/result.json').exists():raise RuntimeError('measurements incomplete; no concurrent functional workload')
results=[]
for scale,w,h in [(1,900,700),(1,640,480),(1.5,900,700),(1.5,640,480),(2,900,700),(2,640,480)]:
 cmd=['/usr/bin/python3',str(b/'native-session.py'),f'native-support-{scale}-{w}','--flow','--cell',str(scale),str(w),str(h)]
 p=subprocess.run(cmd);results.append({'command':cmd,'exit':p.returncode})
(b/'support-batch.json').write_text(json.dumps(results,indent=2)+'\n')
