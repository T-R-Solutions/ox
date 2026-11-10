from pathlib import Path
import json,subprocess,shutil,hashlib,os
ROOT=Path('/home/rodrigo/Projetos/ox'); base=ROOT/'.local/build/toolbox-completion'; candidate=base/'candidate'; source=Path('/home/rodrigo/Projetos/dev_audit/shared-toolbox'); out=ROOT/'docs/validation/toolbox-operational-completion'; results=[]
for tool in ['ruff','bandit','gitleaks','shellcheck','opengrep','syft','trivy','grype','osv-scanner']:
 record=ROOT/'.local/build/operational-qualification'/f'{tool}-image.json'
 run=subprocess.run([str(candidate/'bin/toolbox'),'central','register','--tool',tool,'--record',str(record)],capture_output=True)
 (out/f'{tool}-register.stdout').write_bytes(run.stdout);(out/f'{tool}-register.stderr').write_bytes(run.stderr)
 row={'tool':tool,'register_exit':run.returncode,'image_record_sha256':hashlib.sha256(record.read_bytes()).hexdigest()}
 if run.returncode==0:
  value=json.loads(run.stdout);row['registration']=value
  print(tool,value,flush=True)
  revision=value['revision']
  activation=subprocess.run([str(candidate/'bin/toolbox'),'central','activate','--tool',tool,'--revision',revision],capture_output=True)
  row['isolated_activation_exit']=activation.returncode
 if tool in ['trivy','grype']:
  target=candidate/'tools'/tool/'volume/databases'
  shutil.copytree(source/'tools'/tool/'volume/databases',target,dirs_exist_ok=True)
 results.append(row)
 (out/'candidate-registration.json').write_text(json.dumps(results,indent=2))
run=subprocess.run([str(candidate/'bin/toolbox'),'central','list'],capture_output=True)
(out/'candidate-catalog.json').write_bytes(run.stdout)
