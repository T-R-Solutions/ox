from pathlib import Path
s=Path('.local/build/toolbox-completion/report-rejections.py').read_text().replace("completion/report-rejections'","completion/report-rejections-more'")
s=s.replace("[('ruff','ruff-finding'),('bandit','bandit-finding'),('shellcheck','shellcheck-finding'),('opengrep','opengrep-finding'),('osv','osv-finding'),('trivy','trivy-finding'),('grype','grype-finding'),('sbom','syft-inventory')]","[('gitleaks','gitleaks-finding'),('malware','yara-finding')]")
s=s.replace("/real'/label/'stdout'","/real-expanded-r4'/label/('report.json' if name=='gitleaks' else 'stdout')")
exec(compile(s,'more-reports','exec'))
