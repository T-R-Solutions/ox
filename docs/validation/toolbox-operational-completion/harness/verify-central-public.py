from pathlib import Path
import subprocess,os,json,shutil,hashlib
R=Path('/home/rodrigo/Projetos/ox');base=R/'.local/build/toolbox-completion';out=R/'docs/validation/toolbox-operational-completion/central-public';out.mkdir(exist_ok=True);cli=Path('/home/rodrigo/Projetos/dev_audit/shared-toolbox/bin/toolbox')
catalog=subprocess.run([str(R/'scripts/toolbox.sh'),'central','list'],capture_output=True,env=dict(os.environ,TOOLBOX_BIN=str(cli)));(out/'catalog.json').write_bytes(catalog.stdout)
inputs={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (R/'scripts').rglob('*') if p.is_file() and p.suffix in ('.sh','.toml','.yaml','.yml','.yar')}
(out/'observed-code.json').write_text(json.dumps(inputs,indent=2))
rows=[]
for check in ['ruff','bandit','shellcheck','gitleaks','opengrep','osv','trivy','grype','sbom','malware','history']:
 command=['bash',str(R/'scripts/checks/run.sh'),'--check',check]
 r=subprocess.run(command,capture_output=True,env=dict(os.environ,TOOLBOX_BIN=str(cli)))
 (out/(check+'.stdout')).write_bytes(r.stdout);(out/(check+'.stderr')).write_bytes(r.stderr)
 try:
  path=Path(r.stdout.decode().split('Assessment: ')[-1].strip());assessment=json.loads(path.read_text());(out/(check+'-assessment.json')).write_text(json.dumps(assessment,indent=2));state=assessment['state'];dest=out/check;dest.mkdir();
  for name in ['backend_record.json','inputs.json','input_modes.json','report.json']:
   if (path.parent/name).exists():shutil.copyfile(path.parent/name,dest/name)
  shutil.copytree(path.parent/'tool',dest/'tool')
  meta=assessment['backend_record'];assert meta['outcome']=='native' and meta['cleanup']=='removed';assert state in ('passed','findings','recorded')
 except Exception as e:
  subprocess.run([__import__('sys').executable,str(base/'recover-central.py')],check=True)
  raise
 rows.append({'check':check,'command':command,'exit':r.returncode,'state':state});print(rows[-1],flush=True)
 (out/'results.json').write_text(json.dumps(rows,indent=2))
