from pathlib import Path
import subprocess,json,hashlib
R=Path.cwd();out=R/'docs/validation/toolbox-operational-completion/report-rejections';out.mkdir(exist_ok=False);rows=[]
for name,label in [('ruff','ruff-finding'),('bandit','bandit-finding'),('shellcheck','shellcheck-finding'),('opengrep','opengrep-finding'),('osv','osv-finding'),('trivy','trivy-finding'),('grype','grype-finding'),('sbom','syft-inventory')]:
 original=R/'docs/validation/toolbox-operational-completion/real'/label/'stdout';data=original.read_bytes()
 for mutation,content in [('absent',None),('truncated',data[:len(data)//2]),('malformed',b'{broken'),('incompatible',b'{"unexpected":true}'),('empty',b'{}')]:
  dest=out/(name+'-'+mutation+'.json')
  if content is not None:dest.write_bytes(content)
  command=['bash','-c','source scripts/lib/common.sh; source scripts/lib/reports.sh; finding_count "$1" "$2"','report',name,str(dest)]
  run=subprocess.run(command,capture_output=True);rows.append({'scanner':name,'mutation':mutation,'source_report':str(original.relative_to(R)),'source_sha256':hashlib.sha256(data).hexdigest(),'command':command,'exit':run.returncode,'passed':run.returncode!=0})
  (out/(name+'-'+mutation+'.stderr')).write_bytes(run.stderr)
(out/'results.json').write_text(json.dumps(rows,indent=2));print(len(rows),all(x['passed'] for x in rows))
