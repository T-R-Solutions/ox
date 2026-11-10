from pathlib import Path
import subprocess,os,json,hashlib
R=Path('/home/rodrigo/Projetos/ox');base=R/'.local/build/toolbox-completion';out=R/'docs/validation/toolbox-operational-completion/real';out.mkdir(exist_ok=True);fixture=base/'fixtures';fixture.mkdir(exist_ok=True)
(fixture/'clean.py').write_text('value = 1\n');(fixture/'bad.py').write_text('import os\nimport subprocess\nsubprocess.call("echo fixture", shell=True)\n')
(fixture/'clean.sh').write_text('#!/bin/sh\nprintf "%s\\n" fixture\n');(fixture/'bad.sh').write_text('#!/bin/sh\necho $unquoted\n')
(fixture/'rules.yml').write_text('rules:\n- id: fixture-call\n  pattern: subprocess.call(...)\n  message: controlled finding\n  severity: ERROR\n  languages: [python]\n')
(fixture/'package-lock.json').write_text(json.dumps({'name':'fixture','version':'1.0.0','lockfileVersion':3,'packages':{'':{'name':'fixture','version':'1.0.0'},'node_modules/lodash':{'version':'4.17.15','resolved':'https://registry.npmjs.org/lodash/-/lodash-4.17.15.tgz'}}}))
cli=base/'candidate/bin/toolbox'; rows=[]
cases=[('ruff-clean','ruff',['check','--output-format','json','clean.py'],0,'ruff-clean'),('ruff-finding','ruff',['check','--output-format','json','bad.py'],1,'ruff-finding'),('bandit-clean','bandit',['-f','json','clean.py'],0,'bandit-clean'),('bandit-finding','bandit',['-f','json','bad.py'],1,'bandit-finding'),('shellcheck-clean','shellcheck',['--format=json','clean.sh'],0,'shellcheck-clean'),('shellcheck-finding','shellcheck',['--format=json','bad.sh'],1,'shellcheck-finding'),('gitleaks-clean','gitleaks',['dir','--no-banner','--redact=100','--exit-code','10','clean.py'],0,'native-clean'),('opengrep-finding','opengrep',['scan','--config','rules.yml','--json','--error','--disable-version-check','bad.py'],1,'opengrep'),('syft-inventory','syft',['scan','dir:/project','-o','syft-json'],0,'syft'),('osv-finding','osv-scanner',['scan','source','--offline','--format','json','--all-packages','--lockfile','package-lock.json'],1,'osv'),('trivy-finding','trivy',['fs','--scanners','vuln','--offline-scan','--skip-db-update','--skip-java-db-update','--format','json','--exit-code','1','/project'],1,'trivy'),('grype-finding','grype',['dir:/project','-o','json'],0,'grype')]
for tool in ['ruff','bandit','shellcheck','gitleaks','opengrep','syft','osv-scanner','trivy','grype']:
 cases.append((tool+'-invalid',tool,['--no-such-qualification-option'],None,'invalid'))
def manifest():return {str(p.relative_to(fixture)):hashlib.sha256(p.read_bytes()).hexdigest() for p in fixture.rglob('*') if p.is_file()}
for label,tool,argv,expected,oracle in cases:
 dest=out/label;dest.mkdir(exist_ok=False);before=manifest()
 command=[str(R/'scripts/toolbox.sh'),'exec','--tool',tool,'--project-root',str(fixture),'--results',str(dest),'--timeout','180','--diagnostic-file',str(dest/'execution.json'),'--',*argv]
 run=subprocess.run(command,capture_output=True,env=dict(os.environ,TOOLBOX_BIN=str(cli)),timeout=230)
 (dest/'stdout').write_bytes(run.stdout);(dest/'stderr').write_bytes(run.stderr); meta=json.loads((dest/'execution.json').read_text()); content=False
 try:
  report=json.loads(run.stdout)
  if oracle.startswith('ruff'):content=(len(report)==0 if oracle.endswith('clean') else any(x['code']=='F401' for x in report))
  if oracle.startswith('bandit'):content=report['metrics']['_totals']['loc']>0 and not report['errors'] and (bool(report['results'])==oracle.endswith('finding'))
  if oracle.startswith('shellcheck'):content=bool(report)==oracle.endswith('finding')
  if oracle=='opengrep':content=any(x['check_id']=='fixture-call' for x in report['results'])
  if oracle=='syft':content=any(x['name']=='lodash' for x in report['artifacts'])
  if oracle=='osv':content=bool(report['results']) and 'lodash' in run.stdout.decode()
  if oracle=='trivy':content=any(x.get('Vulnerabilities') for x in report['Results'])
  if oracle=='grype':content=bool(report['matches'])
 except (ValueError,KeyError,TypeError):pass
 if oracle=='native-clean':content=b'no leaks found' in run.stderr.lower()
 if oracle=='invalid':content=run.returncode!=0 and (b'unknown' in run.stderr.lower() or b'invalid' in run.stderr.lower() or b'unrecognized' in run.stderr.lower() or b'flag' in run.stderr.lower() or b'usage' in run.stderr.lower())
 passed=(expected is None or run.returncode==expected) and meta['outcome']=='native' and meta['cleanup']=='removed' and before==manifest() and content
 row={'label':label,'command':command,'expected_exit':expected,'exit':run.returncode,'content_oracle':oracle,'content_valid':content,'source_hashes':before,'source_preserved':before==manifest(),'passed':passed};rows.append(row);print(label,passed,run.returncode,flush=True)
 (out/'results.json').write_text(json.dumps(rows,indent=2))
