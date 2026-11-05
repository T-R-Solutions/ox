import importlib.util,pathlib,os,subprocess,select,json,sys,traceback,time
base=pathlib.Path(__file__).resolve().parent;spec=importlib.util.spec_from_file_location('native',base/'native-session.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
out=base/sys.argv[1];session=None;result={}
try:
 session=m.Session(out,'2400x1800');session.key(0xffe1)
 rd,wr=os.pipe();serverlog=(out/'xwayland.log').open('w')
 server=subprocess.Popen(['Xwayland','-displayfd',str(wr),'-geometry','2000x1600','-nolisten','tcp','-shm'],pass_fds=(wr,),env=session.env,stdout=serverlog,stderr=serverlog);session.children.append(server);os.close(wr)
 if not select.select([rd],[],[],10)[0]:raise RuntimeError('Xwayland readiness')
 display=':'+os.read(rd,32).decode().strip();os.close(rd)
 env=dict(session.env,DISPLAY=display,CARGO_TARGET_DIR='/tmp/ox-f0-frame-target',OX_DESKTOP_CAPTURE_DIR=str(out));result['display']=display
 cmd=['cargo','test','-p','ox-app','--test','desktop','--offline','--','--ignored','--nocapture','--test-threads=1']
 if len(sys.argv)>2:cmd.append(sys.argv[2])
 with (out/'test.log').open('w') as log:p=subprocess.run(cmd,cwd='/tmp/ox-f0-frame-app',env=env,stdout=log,stderr=log,timeout=180)
 result['exit']=p.returncode
except Exception as e:result['error']=str(e);traceback.print_exc()
finally:
 if session:session.close()
 out.mkdir(exist_ok=True);(out/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
