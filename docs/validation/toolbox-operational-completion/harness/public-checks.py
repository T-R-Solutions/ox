from pathlib import Path
import subprocess,os,json
R=Path('/home/rodrigo/Projetos/ox');base=R/'.local/build/toolbox-completion';out=R/'docs/validation/toolbox-operational-completion/public';out.mkdir(exist_ok=True);cli=base/'candidate/bin/toolbox'
revision=json.loads((R/'docs/validation/toolbox-operational-completion/yara-prepare.stdout').read_text())['revision']
r=subprocess.run([str(cli),'central','activate','--tool','yara-x','--revision',revision],capture_output=True);(out/'yara-isolated-activation.json').write_bytes(r.stdout)
rows=[]
for check in ['ruff','bandit','shellcheck','gitleaks','opengrep','osv','trivy','grype','sbom','malware','history']:
 command=['bash',str(R/'scripts/checks/run.sh'),'--check',check]
 r=subprocess.run(command,capture_output=True,env=dict(os.environ,TOOLBOX_BIN=str(cli)))
 (out/(check+'.stdout')).write_bytes(r.stdout);(out/(check+'.stderr')).write_bytes(r.stderr)
 try:
  path=Path(r.stdout.decode().split('Assessment: ')[-1].strip());assessment=json.loads(path.read_text());(out/(check+'-assessment.json')).write_text(json.dumps(assessment,indent=2));state=assessment['state']
 except Exception as e:state=str(e)
 rows.append({'check':check,'command':command,'exit':r.returncode,'state':state});print(rows[-1],flush=True)
 (out/'results.json').write_text(json.dumps(rows,indent=2))
