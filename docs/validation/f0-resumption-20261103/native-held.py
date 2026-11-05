import importlib.util,pathlib,subprocess,os,json,time,hashlib,shutil,sys,traceback
base=pathlib.Path(__file__).resolve().parent;spec=importlib.util.spec_from_file_location('native',base/'native-session.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
if len(sys.argv)==1:
 deadline=time.monotonic()+900
 while not (base/'x11-support-batch.json').exists() and time.monotonic()<deadline:time.sleep(1)
 if not (base/'x11-support-batch.json').exists():raise RuntimeError('X11 support not complete')
 for run in range(1,4):subprocess.run(['/usr/bin/python3',__file__,f'native-held-{run}'],check=True)
 sys.exit(0)
out=base/sys.argv[1];session=None;result={}
try:
 session=m.Session(out);bins=out/'bins';bins.mkdir();workspace=out/'workspace';workspace.mkdir();(workspace/'sentinel').write_text('preserve\n')
 built=m.ROOT/'application/target/debug';identities=[]
 for name,target in [('ox','ox'),('local-task','local-task'),('held-task-oracle','task-oracle')]:
  src=built/name;shutil.copy2(src,bins/target);identities.append({'name':target,'source':str(src),'sha256':hashlib.sha256(src.read_bytes()).hexdigest()})
 # Keep binary copies in /tmp; retain content identities in the evidence directory.
 temp=pathlib.Path('/tmp')/('ox-f0-held-'+str(os.getpid()));shutil.copytree(bins,temp)
 for p in bins.iterdir():p.unlink()
 bins.rmdir()
 log=(out/'wayland.log').open('w');app=subprocess.Popen([str(temp/'ox')],env=dict(session.env,WAYLAND_DEBUG='1',OX_VALIDATION_SESSION=out.name),stdout=log,stderr=log);session.children.append(app);result.update(pid=app.pid,binaries=identities)
 time.sleep(.8);session.key(0xffe1);time.sleep(.2)
 def tabs(n,back=False):
  if back:session.key(0xffe1,True)
  for _ in range(n):session.key(0xff09)
  if back:session.key(0xffe1,False)
 def enter():session.key(0xff0d);time.sleep(.2)
 tabs(3)
 for ch in str(workspace):session.key(ord(ch))
 tabs(1);enter();tabs(1);enter()
 session.wait(lambda:bool(list(workspace.glob('.ox-task-*/result.txt'))),'good artifact');attempt=next(workspace.glob('.ox-task-*'))
 tabs(4);enter();session.wait(lambda:(attempt/'oracle-ready').exists(),'held oracle ready');pid=(attempt/'oracle-ready').read_text();assert pathlib.Path('/proc/'+pid).exists()
 tabs(1);enter();session.shot('held-responsive');enter();tabs(2);enter()
 session.wait(lambda:not pathlib.Path('/proc/'+pid).exists(),'cancelled oracle exit');session.shot('cancelled-inconclusive');result['cancelled_pid']=pid
 tabs(1);tabs(2,True);enter();session.wait(lambda:(attempt/'oracle-ready').read_text()!=pid,'second oracle ready');second=(attempt/'oracle-ready').read_text();assert pathlib.Path('/proc/'+second).exists()
 tabs(2);enter();session.wait(lambda:app.poll() is not None,'close during verification');assert not pathlib.Path('/proc/'+second).exists();assert (workspace/'sentinel').read_text()=='preserve\n'
 result.update(second_pid=second,second_absent=True,app_exit=app.returncode)
except Exception as e:result['error']=str(e);traceback.print_exc()
finally:
 if session:session.close()
 out.mkdir(exist_ok=True);(out/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
