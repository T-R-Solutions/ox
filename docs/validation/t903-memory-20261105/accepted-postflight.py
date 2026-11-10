from pathlib import Path
import subprocess,json,time,os,hashlib,platform
b=Path(__file__).resolve().parent;r=b.parents[2];runs=[]
while not (b/'accepted-runs.json').exists() or not any(x['name']=='accepted-original-native' for x in json.loads((b/'accepted-runs.json').read_text())):time.sleep(1)
def run(name,cmd,cwd=r,env=None):
 start=time.monotonic()
 with (b/(name+'.log')).open('x') as log:p=subprocess.run(cmd,cwd=cwd,env=env,stdout=log,stderr=log)
 runs.append({'name':name,'command':cmd,'cwd':str(cwd),'exit':p.returncode,'seconds':time.monotonic()-start});(b/'accepted-postflight.json').write_text(json.dumps(runs,indent=2)+'\n');print(name,p.returncode,flush=True)
run('accepted-build-examples',['cargo','build','--workspace','--examples','--locked','--offline'],r/'application')
run('backend-accepted',['/usr/bin/time','-v',str(r/'application/target/debug/examples/f0_measure'),str(r/'application/target/debug'),str(b/'backend-accepted-workspace')])
for i in range(3):run('large-accepted-'+str(i),['/usr/bin/time','-v',str(r/'application/target/debug/examples/history_measure'),str(b/f'large-accepted-history-{i}'),str(r/'application/target/debug/task-oracle')])
for name,cmd in [('check',['cargo','check','--workspace','--locked','--offline']),('fmt',['cargo','fmt','--all','--','--check']),('clippy',['cargo','clippy','--workspace','--all-targets','--locked','--offline','--','-D','warnings'])]:run('accepted-'+name,cmd,r/'application')
run('accepted-coverage',['/usr/bin/python3',str(b/'coverage-accepted.py')])
run('accepted-flow-analysis',['/usr/bin/python3',str(b/'check-accepted-flow.py')])
run('accepted-history-analysis',['/usr/bin/python3',str(b/'check-accepted-history.py')])
env={'platform':platform.uname()._asdict(),'profile':'dev, first-party unoptimized; existing tiny-skia0.11.4 opt-level3 unchanged','renderer':'tiny-skia','capture':'isolated Mutter PipeWire RGB native+extra history/FIFO X11; X11 full tests get_image; 20ms poll; CPU100Hz; no physical scanout'}
for key,cmd in [('cpu',['lscpu']),('rustc',['rustc','-vV']),('mutter',['mutter','--version']),('processes',['ps','-eo','pid,ppid,comm'])]:env[key]=subprocess.check_output(cmd,text=True)
env['binaries']=[{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [r/'application/target/debug/ox',Path('/tmp/ox-t903-target/debug/ox')]]
env['fixtures']=[]
for directory in [r/'application/target/debug',Path('/tmp/ox-t903-target/debug')]:
 for name in ['local-task','task-oracle','held-task-oracle','local-agent','local-oracle','local-plugin']:
  p=directory/name
  if p.is_file():env['fixtures'].append({'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size,'mtime_ns':p.stat().st_mtime_ns})
(b/'accepted-environment.json').write_text(json.dumps(env,indent=2)+'\n')
