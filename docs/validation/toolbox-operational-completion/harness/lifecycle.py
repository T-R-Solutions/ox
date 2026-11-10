from pathlib import Path
import subprocess,os,json,time,signal,hashlib,concurrent.futures
R=Path('/home/rodrigo/Projetos/ox');base=R/'.local/build/toolbox-completion';out=R/'docs/validation/toolbox-operational-completion/lifecycle';out.mkdir(exist_ok=False);cli=base/'candidate/bin/toolbox';fixture=base/'cancel-fixture';fixture.mkdir()
(fixture/'rules.yml').write_text('rules:\n- id: controlled\n  pattern: print(...)\n  message: fixture\n  severity: WARNING\n  languages: [python]\n')
(fixture/'large.py').write_text('print("controlled")\n'*300000)
before={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in fixture.iterdir()}
cmd=[str(R/'scripts/toolbox.sh'),'exec','--tool','opengrep','--project-root',str(fixture),'--results',str(out),'--timeout','120','--diagnostic-file',str(out/'cancel.json'),'--','scan','--json','--disable-version-check','--config','rules.yml','large.py']
with (out/'stdout').open('wb') as stdout,(out/'stderr').open('wb') as stderr:
 p=subprocess.Popen(cmd,env=dict(os.environ,TOOLBOX_BIN=str(cli)),stdout=stdout,stderr=stderr)
 seen=[]
 for i in range(100):
  inspect=subprocess.run(['docker','ps','--filter','name=toolbox-native-','--format','{{.Names}}'],capture_output=True)
  names=inspect.stdout.decode().splitlines()
  for name in names:
   result=subprocess.run(['docker','inspect',name],capture_output=True)
   if result.returncode==0:
    data=json.loads(result.stdout)[0]
    if any(m.get('Source')==str(fixture) for m in data['Mounts']):seen.append(name)
  if seen:break
  if p.poll() is not None:break
  time.sleep(.1)
 if not seen:raise RuntimeError('No actual running controlled scanner observed')
 p.send_signal(signal.SIGTERM);code=p.wait(timeout=45)
meta=json.loads((out/'cancel.json').read_text());cleanup=[]
for name in seen:
 r=subprocess.run(['docker','inspect',name],capture_output=True);cleanup.append({'container':name,'exit':r.returncode,'stderr':r.stderr.decode()})
after={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in fixture.iterdir()}
result={'command':cmd,'exit':code,'diagnostic':meta,'observed_running':seen,'cleanup':cleanup,'sources_before':before,'sources_after':after,'passed':code==143 and meta['outcome']=='cancelled' and meta['cleanup']=='removed' and all(x['exit']!=0 for x in cleanup) and before==after}
(out/'results.json').write_text(json.dumps(result,indent=2));print(result['passed'])
