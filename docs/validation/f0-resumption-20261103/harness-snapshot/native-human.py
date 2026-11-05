import pathlib,os,subprocess,time,json,hashlib
root=pathlib.Path(__file__).resolve().parents[3];out=root/'docs/validation/f0-resumption-20261103/primary-native-1';out.mkdir()
workspace=pathlib.Path('/tmp/oxf0resume3');workspace.mkdir();(workspace/'sentinel').write_text('preserve F0 resumption\n')
binary=pathlib.Path('/tmp/ox-f0-frame-target/debug/ox');env=dict(os.environ,WAYLAND_DEBUG='1',OX_VALIDATION_SESSION='F0-RETOMADA-03',OX_VALIDATION_WORKSPACE=str(workspace));env.pop('DISPLAY',None)
for name in ['desktop.rs','Cargo.toml']:
 src=pathlib.Path('/tmp/ox-f0-frame-app')/('crates/ox-ui/src/desktop.rs' if name=='desktop.rs' else name);(out/(name+'.bin')).write_bytes(src.read_bytes())
with (out/'wayland.log').open('w') as log:
 app=subprocess.Popen([str(binary)],cwd='/tmp',env=env,stdout=log,stderr=log)
 rec={'pid':app.pid,'workspace':str(workspace),'binary_sha256':hashlib.sha256(binary.read_bytes()).hexdigest(),'WAYLAND_DISPLAY':env.get('WAYLAND_DISPLAY'),'DISPLAY':None,'start':time.time(),'instrumentation':'update-message log, isolated iced client draw timer, prefilled workspace; not performance acceptance'}
 (out/'running.json').write_text(json.dumps(rec,indent=2)+'\n');print(json.dumps(rec),flush=True)
 seen={};end=time.monotonic()+1200
 while app.poll() is None and time.monotonic()<end:
  childfile=pathlib.Path(f'/proc/{app.pid}/task/{app.pid}/children')
  for task in pathlib.Path(f'/proc/{app.pid}/task').glob('*/children'):
   try:ids=task.read_text().split()
   except FileNotFoundError:continue
   for pid in ids:
    if pid not in seen:
     try:seen[pid]={'first_seen':time.time(),'command':pathlib.Path(f'/proc/{pid}/cmdline').read_bytes().replace(b'\0',b' ').decode()}
     except FileNotFoundError:pass
  for pid,item in seen.items():
   if 'absent_at' not in item and not pathlib.Path('/proc/'+pid).exists():item['absent_at']=time.time()
  (out/'children.json').write_text(json.dumps(seen,indent=2)+'\n')
  time.sleep(.02)
 rec['natural_exit']=app.poll()
 if app.poll() is None:app.terminate();rec['timeout']=True
 try:rec['exit']=app.wait(timeout=5)
 except subprocess.TimeoutExpired:app.kill();rec['exit']=app.wait()
 rec['end']=time.time();(out/'result.json').write_text(json.dumps(rec,indent=2)+'\n')
 files=[]
 for p in workspace.rglob('*'):
  if p.is_file():
   data=p.read_bytes();dest=out/'workspace'/p.relative_to(workspace);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data);files.append({'path':str(p),'sha256':hashlib.sha256(data).hexdigest(),'size':len(data)})
 (out/'artifacts.json').write_text(json.dumps(files,indent=2)+'\n');print(json.dumps(rec),flush=True)
