import datetime, hashlib, json, os, pathlib, subprocess, sys, time
root=pathlib.Path('/home/rodrigo/Projetos/ox')
run=root/'docs/validation/product-local-task-ui'/('manual-'+sys.argv[1]+'-'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ'))
run.mkdir()
(run/'runner.py').write_bytes(pathlib.Path(__file__).read_bytes())
binary=root/'application/target/debug/ox'
inputs=[binary,root/'application/Cargo.toml',root/'application/Cargo.lock',root/'application/rust-toolchain.toml']+list((root/'application/crates').rglob('*.rs'))
record={'scenario':sys.argv[1],'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'deadline_seconds':1800,'method':'Human visual observation and interaction; separate WAYLAND_DEBUG trace and supervised process exit; no synthetic events or state calls','inputs':[{'path':str(p.relative_to(root)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in inputs],'human_observation':'pending'}
env=dict(os.environ,WAYLAND_DEBUG='1'); env.pop('DISPLAY',None)
record['environment']={k:env.get(k) for k in ['WAYLAND_DISPLAY','DISPLAY','XDG_RUNTIME_DIR','XDG_SESSION_TYPE']}
start=time.monotonic()
with (run/'stderr.log').open('x') as err,(run/'stdout.log').open('x') as out:
 child=subprocess.Popen([str(binary)],cwd=root/'application',env=env,stderr=err,stdout=out)
 record['pid']=child.pid
 print('RUNNING',child.pid,str(run),flush=True)
 try:
  record['exit_code']=child.wait(timeout=1800); record['supervisor_terminated']=False
 except subprocess.TimeoutExpired:
  record['supervisor_terminated']=True; child.terminate()
  try: record['exit_code']=child.wait(timeout=5)
  except subprocess.TimeoutExpired: child.kill(); record['exit_code']=child.wait()
 record['elapsed_seconds']=time.monotonic()-start
(run/'result.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({k:v for k,v in record.items() if k!='inputs'},indent=2),flush=True)
