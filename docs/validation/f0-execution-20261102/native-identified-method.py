from pathlib import Path
import subprocess,os,json,time,hashlib
root=Path('/home/rodrigo/Projetos/ox');out=root/'docs/validation/f0-execution-20261102/wayland-identified';out.mkdir();workspace=Path('/tmp/oxf0native2');workspace.mkdir(exist_ok=True)
env=dict(os.environ,WAYLAND_DEBUG='1',OX_VALIDATION_SESSION='F0-20261102-B');env.pop('DISPLAY',None)
with (out/'wayland.log').open('w') as log:
 p=subprocess.Popen([str(root/'application/target/debug/ox')],cwd='/tmp',env=env,stdout=log,stderr=subprocess.STDOUT)
 record={'pid':p.pid,'DISPLAY':'unset','WAYLAND_DISPLAY':env.get('WAYLAND_DISPLAY'),'binary_sha256':hashlib.sha256((root/'application/target/debug/ox').read_bytes()).hexdigest(),'workspace':str(workspace),'start':time.time(),'method':'native Wayland, human interaction required; protocol log is not input proof'}
 (out/'running.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record),flush=True)
 try:record['exit']=p.wait(timeout=1200)
 except subprocess.TimeoutExpired:
  p.terminate()
  try:record['exit']=p.wait(timeout=10)
  except subprocess.TimeoutExpired:p.kill();record['exit']=p.wait()
  record['timeout']=True
 record['end']=time.time();(out/'result.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record),flush=True)
