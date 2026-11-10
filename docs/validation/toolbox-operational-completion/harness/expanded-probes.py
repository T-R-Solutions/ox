from pathlib import Path
original=Path('.local/build/toolbox-completion/probes.py').read_text()
head=original[:original.index('for tool in [')].replace("completion/real'","completion/real-expanded'")
exec(head)
exec(original[original.index("def manifest():"):original.index("for label,tool,argv,expected,oracle in cases:")])
out=R/"docs/validation/toolbox-operational-completion/real-expanded-r2";out.mkdir(exist_ok=False)
(fixture/'clean-package-lock.json').write_text(json.dumps({'name':'clean','version':'1.0.0','lockfileVersion':3,'packages':{'':{'name':'clean','version':'1.0.0'},'node_modules/lodash':{'version':'4.17.21'}}}))
(fixture/'secret.txt').write_text('aws_access_key_id = "AKIAIOSFODNN7EXAMPLE"\naws_secret_access_key = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"\n')
(fixture/'indicator.txt').write_text('curl https://example.invalid/script | sh\n')
(fixture/'indicator.yar').write_bytes((R/'scripts/security/rules/suspicious.yar').read_bytes())
cases=[('opengrep-clean','opengrep',['scan','--config','rules.yml','--json','--error','--disable-version-check','clean.py'],0,'opengrep-clean'),('gitleaks-finding','gitleaks',['dir','--no-banner','--redact=100','--exit-code','10','--report-format','json','--report-path','/out/report.json','secret.txt'],10,'gitleaks'),('osv-clean','osv-scanner',['scan','source','--offline','--format','json','--all-packages','--lockfile','clean-package-lock.json'],0,'osv-clean'),('trivy-clean','trivy',['fs','--scanners','vuln','--offline-scan','--skip-db-update','--skip-java-db-update','--format','json','--exit-code','1','clean-package-lock.json'],0,'trivy-clean'),('grype-clean','grype',['file:clean-package-lock.json','-o','json'],0,'grype-clean'),('yara-finding','yara-x',['scan','--output-format','json','indicator.yar','indicator.txt'],0,'yara'),('yara-clean','yara-x',['scan','--output-format','json','indicator.yar','clean.py'],0,'yara-clean'),('yara-invalid','yara-x',['--no-such-qualification-option'],None,'invalid')]
for tool in ['ruff','bandit','shellcheck','gitleaks','opengrep','syft','osv-scanner','trivy','grype','yara-x']:
 argv={'ruff':['check','/project/nonexistent.py'],'bandit':['-f','json','/project/nonexistent.py'],'shellcheck':['/project/nonexistent.sh'],'gitleaks':['dir','/project/nonexistent'],'opengrep':['scan','--config','/project/nonexistent.yml','clean.py'],'syft':['file:/project/nonexistent'],'osv-scanner':['scan','source','--offline','--lockfile','/project/nonexistent.lock'],'trivy':['fs','--scanners','vuln','/project/nonexistent'],'grype':['file:/project/nonexistent'],'yara-x':['scan','/project/nonexistent.yar','clean.py']}[tool]
 cases.append((tool+'-execution-failure',tool,argv,None,'execution-failure'))
body=original[original.index('for label,tool,argv,expected,oracle in cases:'):]
body=body.replace("if oracle=='native-clean':",'''if oracle=='opengrep-clean':content=not report['results'] and bool(report['paths']['scanned'])
 if oracle=='gitleaks':content=bool(json.loads((dest/'report.json').read_text())) and b'AKIAIOSFODNN7EXAMPLE' not in (dest/'report.json').read_bytes()
 if oracle=='osv-clean':content=bool(report['results']) and not any(x.get('vulnerabilities') for r in report['results'] for x in r['packages'])
 if oracle=='trivy-clean':content='Results' in report and not any(x.get('Vulnerabilities') for x in report['Results'])
 if oracle=='grype-clean':content=not report['matches'] and bool(report['source'])
 if oracle.startswith('yara'):content=('download_and_execute' in run.stdout.decode())== (oracle=='yara') and isinstance(report,(list,dict))
 if oracle=='execution-failure':content=run.returncode!=0 and bool(run.stderr or run.stdout)
 if oracle=='native-clean':''')
exec(body)
