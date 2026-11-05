"""Run local governance checks, preserving every run. No source-library access."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,platform,subprocess,sys
from governance_support import distribution_files
ROOT=Path(__file__).resolve().parents[3]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    run=ROOT/'docs/validation/runs'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
    run.mkdir(parents=True,exist_ok=False)
    inputs={}
    for p in distribution_files(ROOT):
        if not p.is_relative_to(run):
            inputs[p.relative_to(ROOT).as_posix()]=sha(p)
    (run/'inputs.json').write_text(json.dumps(inputs,ensure_ascii=False,indent=2)+'\n')
    commands=[['sdd/tools/validate.py','--root','.'],['sdd/tools/validate.py','--root','.','--structure-only'],['tools/governance/scripts/check-ox.py'],['-m','unittest','discover','-s','tools/governance/tests','-v']]
    results=[]; env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
    for i,args in enumerate(commands,1):
        command=[sys.executable,*args]
        if env.get('OX_ISOLATION_ORIGIN'):
            command=[sys.executable,'tools/governance/scripts/isolated-run.py',env['OX_ISOLATION_ORIGIN'],*args]
        process=subprocess.run(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        log=run/f'{i:02d}.log'; log.write_text(process.stdout)
        results.append({'command':'PYTHONDONTWRITEBYTECODE=1 python3 '+' '.join(args),'exit_code':process.returncode,'log':log.relative_to(ROOT).as_posix(),'sha256':sha(log)})
        print(process.stdout.strip())
    result={'scope':'governance/SDD/skills','product_acceptance':False,'environment':{'python':platform.python_version(),'system':platform.platform()},'results':results,'limitations':['Governance, SDD and skill-contract checks only.','No Rust compilation, application integration, sandbox effectiveness or product acceptance is established.'],'input_manifest':str((run/'inputs.json').relative_to(ROOT))}
    (run/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('Governance/SDD evidence:',run.relative_to(ROOT))
    return int(any(x['exit_code'] for x in results))
if __name__=='__main__': sys.exit(main())
