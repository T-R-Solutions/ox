import os,pathlib,subprocess,select,time,json
root=pathlib.Path('/home/rodrigo/Projetos/ox'); r=root/'docs/validation/f0-execution-20261102/x11-acceptance-scale2'; r.mkdir()
(r/'runner.py').write_bytes(pathlib.Path(__file__).read_bytes())
(r/'desktop.rs').write_bytes((root/'application/crates/ox-app/tests/desktop.rs').read_bytes())
readfd,writefd=os.pipe(); result={}
with (r/'server.log').open('x') as log:
 args=['Xwayland','-displayfd',str(writefd),'-fullscreen','-geometry','2000x1600','-nolisten','tcp','-shm']
 result['server_command']=args
 server=subprocess.Popen(args,pass_fds=(writefd,),stdout=log,stderr=subprocess.STDOUT)
 os.close(writefd)
 try:
  if not select.select([readfd],[],[],10)[0]: raise RuntimeError('Xwayland readiness exceeded 10s')
  display=os.read(readfd,32).decode().strip()
  if not display.isdigit(): raise RuntimeError('No display number: '+repr(display))
  result['display']=':'+display
  env=dict(os.environ,DISPLAY=result['display'],OX_DESKTOP_CAPTURE_DIR=str(r),WINIT_X11_SCALE_FACTOR='2')
  args=['cargo','test','-p','ox-app','--test','desktop','--locked','--','--ignored','visual_response_and_window_matrix','--nocapture','--test-threads=1']
  result['test_command']=args
  with (r/'desktop.log').open('x') as out:
   p=subprocess.run(args,cwd=root/'application',env=env,stdout=out,stderr=subprocess.STDOUT,timeout=90)
  result['test_exit_code']=p.returncode
 except Exception as e: result['error']=str(e)
 finally:
  os.close(readfd)
  server.terminate()
  try: result['server_exit_code']=server.wait(timeout=5)
  except subprocess.TimeoutExpired: server.kill(); result['server_exit_code']=server.wait()
(r/'result.json').write_text(json.dumps(result,indent=2)+'\n'); print(json.dumps(result,indent=2))
if (r/'desktop.log').exists(): print((r/'desktop.log').read_text())
