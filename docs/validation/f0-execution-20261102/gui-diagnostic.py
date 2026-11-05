from pathlib import Path
import argparse,subprocess,os,select,json
parser=argparse.ArgumentParser();parser.add_argument('--coverage',action='store_true');parser.add_argument('--suffix',default='');parser.add_argument('--filter');args=parser.parse_args()
root=Path('/tmp/ox-f0-frame-app').parent;application=Path('/tmp/ox-f0-frame-app');base=Path('/home/rodrigo/Projetos/ox/docs/validation/f0-execution-20261102')
for scale in ['1']:
 out=base/(('gui-covered' if args.coverage else 'gui-diagnostic-'+scale)+args.suffix);out.mkdir()
 (out/'desktop.rs.bin').write_bytes((application/'crates/ox-app/tests/desktop.rs').read_bytes());(out/'desktop-ui.rs.bin').write_bytes((application/'crates/ox-ui/src/desktop.rs').read_bytes())
 rd,wr=os.pipe();result={'scale':scale,'coverage':args.coverage}
 with (out/'server.log').open('w') as log:
  server=subprocess.Popen(['Xwayland','-displayfd',str(wr),'-fullscreen','-geometry','2000x1600','-nolisten','tcp','-shm'],pass_fds=(wr,),stdout=log,stderr=subprocess.STDOUT);os.close(wr)
  try:
   if not select.select([rd],[],[],10)[0]:raise RuntimeError('Xwayland not ready')
   display=os.read(rd,32).decode().strip();assert display.isdigit();env=dict(os.environ,CARGO_TARGET_DIR='/tmp/ox-f0-frame-target',DISPLAY=':'+display,WINIT_X11_SCALE_FACTOR=scale,OX_DESKTOP_CAPTURE_DIR=str(out))
   if args.coverage:env.update(CARGO_TARGET_DIR='/tmp/ox-f0-coverage-target',RUSTFLAGS='-C instrument-coverage',LLVM_PROFILE_FILE=str(base/'coverage-complete/raw/%m-%p.profraw'))
   cmd=['cargo','test','-p','ox-app','--test','desktop','--offline','--','--ignored','--nocapture','--test-threads=1']
   if scale!='1':cmd.insert(cmd.index('--nocapture'),'visual_response_and_window_matrix')
   elif args.filter:cmd.insert(cmd.index('--nocapture'),args.filter)
   result['command']=cmd
   with (out/'desktop.log').open('w') as output:p=subprocess.run(cmd,cwd=application,env=env,stdout=output,stderr=subprocess.STDOUT,timeout=600)
   result['exit']=p.returncode
  except Exception as e:result['error']=str(e)
  finally:
   os.close(rd);server.terminate()
   try:server.wait(timeout=5)
   except subprocess.TimeoutExpired:server.kill();server.wait()
 (out/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
