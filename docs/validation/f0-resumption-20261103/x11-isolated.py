import importlib.util,pathlib,os,subprocess,select,json,sys,traceback,time,socket,threading
base=pathlib.Path(__file__).resolve().parent;spec=importlib.util.spec_from_file_location('native',base/'native-session.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
if sys.argv[1]=='--repeat-coverage':
 for run in [2,3]:subprocess.run(['/usr/bin/python3',__file__,f'x11-covered-held-{run}','coverage-held'],check=True)
 sys.exit(0)
if sys.argv[1]=='--matrix':
 deadline=time.monotonic()+360
 while not (base/'native-metrics-2-640/result.json').exists() and time.monotonic()<deadline:time.sleep(1)
 if not (base/'native-metrics-2-640/result.json').exists():raise RuntimeError('native measurement has not completed; avoid concurrent load')
 for scale,w,h in [(1,900,700),(1,640,480),(1.5,900,700),(1.5,640,480),(2,900,700),(2,640,480)]:
  subprocess.run(['/usr/bin/python3',__file__,f'x11-metrics-{scale}-{w}','adopted_cell_metrics',str(scale),str(w),str(h)],check=True)
 sys.exit(0)
out=base/sys.argv[1];session=None;result={}
try:
 session=m.Session(out,'2400x1800');session.key(0xffe1)
 rd,wr=os.pipe();serverlog=(out/'xwayland.log').open('w')
 server=subprocess.Popen(['Xwayland','-displayfd',str(wr),'-geometry','2000x1600','-nolisten','tcp','-shm','-noreset'],pass_fds=(wr,),env=session.env,stdout=serverlog,stderr=serverlog);session.children.append(server);os.close(wr)
 if not select.select([rd],[],[],10)[0]:raise RuntimeError('Xwayland readiness')
 display=':'+os.read(rd,32).decode().strip()
 sockpath='/tmp/ox-f0-keys-'+str(os.getpid());bridge=socket.socket(socket.AF_UNIX);bridge.bind(sockpath);bridge.listen(4)
 def serve():
  while True:
   client,_=bridge.accept()
   with client:
    try:
     action,sym=client.recv(128).decode().split();
     for state in ([True,False] if action=='key' else [action=='down']):
      session.call('RemoteDesktop',session.rd,'NotifyKeyboardKeysym','(ub)',(int(sym),state))
     client.sendall(b'ok')
    except Exception as error:client.sendall(str(error).encode())
 threading.Thread(target=serve,daemon=True).start()
 time.sleep(.5);session.key(0xffe1)
 env=dict(session.env,OX_KEY_SOCKET=sockpath,DISPLAY=display,CARGO_TARGET_DIR='/tmp/ox-f0-frame-target',OX_DESKTOP_CAPTURE_DIR=str(out));result['display']=display
 if len(sys.argv)>3:
  env.update(WINIT_X11_SCALE_FACTOR=sys.argv[3],OX_VALIDATION_WIDTH=sys.argv[4],OX_VALIDATION_HEIGHT=sys.argv[5])
  result.update(scale=sys.argv[3],logical_size=[int(sys.argv[4]),int(sys.argv[5])])
 (out/'desktop-test.rs.bin').write_bytes(pathlib.Path('/tmp/ox-f0-frame-app/crates/ox-app/tests/desktop.rs').read_bytes())
 if len(sys.argv)>2 and sys.argv[2]=='coverage-held':
  env.update(CARGO_TARGET_DIR='/tmp/ox-f0-resume-coverage-target',RUSTFLAGS='-C instrument-coverage',LLVM_PROFILE_FILE=str(out/'%m-%p.profraw'))
  with (out/'build.log').open('w') as buildlog:
   subprocess.run(['cargo','build','--workspace','--offline'],cwd='/tmp/ox-f0-frame-app',env=env,stdout=buildlog,stderr=buildlog,check=True,timeout=300)
 cmd=['cargo','test','-p','ox-app','--test','desktop','--offline','--','--ignored','--nocapture','--test-threads=1']
 if len(sys.argv)>2 and sys.argv[2]!='full':cmd.append('cancel_verification_observes_oracle_exit_in_ui' if sys.argv[2]=='coverage-held' else sys.argv[2])
 if len(sys.argv)>2 and sys.argv[2]=='full':cmd.extend(['--skip','adopted_cell_metrics'])
 with (out/'test.log').open('w') as log:p=subprocess.run(cmd,cwd='/tmp/ox-f0-frame-app',env=env,stdout=log,stderr=log,timeout=180)
 result['exit']=p.returncode
except Exception as e:result['error']=str(e);traceback.print_exc()
finally:
 if session:session.close()
 out.mkdir(exist_ok=True);(out/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
