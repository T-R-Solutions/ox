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
 tab(4);enter();session.wait(lambda:'Workspace ready' in text() or 'workspace accepted' in text().lower() or 'Done(' in text(),'select done');session.shot('selected');tab(1);enter();session.wait(lambda:bool(list(w.glob('.ox-task-*/result.txt'))),'artifact');time.sleep(.2)
 attempt=next(w.glob('.ox-task-*'));result=attempt/'result.txt';original=result.read_bytes();assert original==(attempt/'request.txt').read_bytes()+b'result=42\n';tab(4);enter();session.wait(lambda:'APPROVED' in text(),'approval');session.shot('approved');session.key(0xff56);session.shot('approved-history');session.key(0xff55)
 # Never operate on user files: this exact result was produced above in our fixture.
 result.rename(attempt/'saved-result.txt');os.mkfifo(result);r['fifo_mode']=oct(result.stat().st_mode);r['fifo_writer']=False
 tab(1);offset=len(text());start=time.monotonic();enter();session.wait(lambda:'Done(' in text()[offset:],'FIFO refresh done');r['refresh_seconds']=time.monotonic()-start;r['refresh_log']=text()[offset:];r['threads_after_refresh']=[(p/'comm').read_text().strip() for p in Path(f'/proc/{app.pid}/task').glob('*') if (p/'comm').exists()];session.shot('fifo-refresh');session.key(0xff56);session.shot('fifo-refresh-history');session.key(0xff55)
 # reverse focus: Refresh->Verify
 session.key(0xffe1,True);tab(1);session.key(0xffe1,False);offset=len(text());start=time.monotonic();enter();session.wait(lambda:'Done(' in text()[offset:],'FIFO verify done');r['verify_seconds']=time.monotonic()-start;r['verify_log']=text()[offset:];session.shot('fifo-verify-error')
 assert 'APPROVED' not in r['refresh_log'] and 'APPROVED' not in r['verify_log']
 # refresh may render historical APPROVED bytes, so inspect current verdict separately.
 result.rename(attempt/'fifo-no-writer');(attempt/'saved-result.txt').rename(result)
 tab(1);offset=len(text());enter();session.wait(lambda:'Done(' in text()[offset:],'restored refresh done');r['restored_log']=text()[offset:];session.key(0xff56);session.shot('restored-history');session.key(0xff55)
 r['sentinel_preserved']=(w/'sentinel').read_bytes()==b'preserve FIFO journey'
 tab(2);enter();session.wait(lambda:app.poll() is not None,'natural close');r['app_exit']=app.returncode;r['process_absent']=not Path(f'/proc/{app.pid}').exists()
except Exception as e:r['error']=repr(e);traceback.print_exc()
finally:
 if session:session.close()
 out.mkdir(exist_ok=True);(out/'result.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r),flush=True)
