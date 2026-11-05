import subprocess,pathlib,json,sys
b=pathlib.Path(__file__).resolve().parent;results=[]
if len(sys.argv)>1 and sys.argv[1]=='--history-candidate':
 subprocess.run(['/usr/bin/python3',str(b/'history-session.py'),'raster-profile-candidate-2-900','--flow','--cell','2','900','700'],check=True)
 sys.exit(0)
for scale,w,h in [(1,900,700),(1,640,480),(1.5,900,700),(1.5,640,480),(2,900,700),(2,640,480)]:
 for backend in ['native','x11']:
  if backend=='native':cmd=['/usr/bin/python3',str(b/'native-resource-session.py'),f'native-resource-{scale}-{w}','--flow','--cell',str(scale),str(w),str(h)]
  else:cmd=['/usr/bin/python3',str(b/'x11-isolated.py'),f'x11-resource-{scale}-{w}','local_task_rendered_flow',str(scale),str(w),str(h)]
  p=subprocess.run(cmd);results.append({'command':cmd,'exit':p.returncode})
(b/'resource-batch.json').write_text(json.dumps(results,indent=2)+'\n')
