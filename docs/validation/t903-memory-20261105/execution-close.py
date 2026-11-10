from pathlib import Path
import importlib.util,sys,os,subprocess,time,json,hashlib,select,traceback
b=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('session',b/'native-session.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
out=b/sys.argv[1];backend=sys.argv[2];session=None;r={'backend_requested':backend}
try:
 session=m.Session(out);env=dict(session.env);w=out/'workspace';w.mkdir();(w/'sentinel').write_bytes(b'preserve FIFO journey')
 if backend=='x11':
  rd,wr=os.pipe();log=(out/'xwayland.log').open('w');server=subprocess.Popen(['Xwayland','-displayfd',str(wr),'-geometry','1200x900','-nolisten','tcp','-shm','-noreset'],pass_fds=(wr,),env=env,stdout=log,stderr=log);session.children.append(server);os.close(wr);assert select.select([rd],[],[],10)[0];env['DISPLAY']=':'+os.read(rd,32).decode().strip();env.pop('WAYLAND_DISPLAY');r['display']=env['DISPLAY']
 env.update(OX_VALIDATION_WORKSPACE=str(w),OX_VALIDATION_SESSION=out.name,WAYLAND_DEBUG='1')
 binary=Path('/tmp/ox-t903-target/debug/ox');log=(out/'client.log').open('w');app=subprocess.Popen([str(binary)],env=env,stdout=log,stderr=log);session.children.append(app);r.update(pid=app.pid,binary_sha256=hashlib.sha256(binary.read_bytes()).hexdigest())
 def text():return (out/'client.log').read_text()
 session.wait(lambda:'OX_CLIENT_FRAME_MS' in text(),'initial draw');time.sleep(.5);session.key(0xffe1)
 if backend=='x11':
  (out/'x11-focus.txt').write_text(subprocess.check_output(['/usr/bin/python3',str(b/'focus-x11.py'),env['DISPLAY']],text=True))
  (out/'x11-window-tree.txt').write_text(subprocess.check_output(['xprop','-display',env['DISPLAY'],'-root'],text=True))
 else:assert 'xdg_toplevel' in text(), 'native protocol absent'
 def tab(n):
  for _ in range(n):session.key(0xff09)
 def enter():session.key(0xff0d);time.sleep(.25)

 tab(4);enter();session.wait(lambda:'Done(' in text(),'workspace ready')
 tab(4);enter()
 def children():
  found=[]
  for p in Path(f'/proc/{app.pid}/task').glob('*/children'):
   try:found.extend(p.read_text().split())
   except FileNotFoundError:pass
  return [pid for pid in found if Path('/proc/'+pid+'/cmdline').exists() and b'local-task' in Path('/proc/'+pid+'/cmdline').read_bytes()]
 session.wait(lambda:bool(children()),'owned task ready');owned=children();r['owned_pids']=owned
 r['threads_running']=[{'tid':p.name,'comm':(p/'comm').read_text().strip()} for p in Path(f'/proc/{app.pid}/task').glob('*') if (p/'comm').exists()]
 r['owned_stat']=[Path('/proc/'+pid+'/stat').read_text() for pid in owned]
 tab(1);enter();session.shot('responsive-running');enter();tab(1);enter()
 session.wait(lambda:app.poll() is not None,'close during execution')
 assert all(not Path('/proc/'+pid).exists() for pid in owned)
 r.update(app_exit=app.returncode,process_absent=not Path(f'/proc/{app.pid}').exists(),owned_absent=True,sentinel_preserved=(w/'sentinel').read_bytes()==b'preserve FIFO journey')
except Exception as e:r['error']=repr(e);traceback.print_exc()
finally:
 if session:session.close()
 out.mkdir(exist_ok=True);(out/'result.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r),flush=True)
