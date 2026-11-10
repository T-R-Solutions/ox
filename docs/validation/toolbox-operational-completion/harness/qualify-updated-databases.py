from pathlib import Path
import json,subprocess,os
R=Path.cwd();base=R/'.local/build/toolbox-completion';candidate=base/'candidate';out=R/'docs/validation/toolbox-operational-completion/updated-database-qualification';out.mkdir(exist_ok=False);rows=[]
for tool,version in [('trivy','0.76.2'),('grype','0.119.0')]:
 pointer=candidate/'tools'/tool/'volume/databases'/version/'current.json';before=pointer.read_bytes();desired=(R/'docs/validation/toolbox-operational-completion/updates'/tool/'pointer-after.json').read_bytes();pointer.write_bytes(desired)
 dest=out/tool;dest.mkdir();argv=['fs','--scanners','vuln','--offline-scan','--skip-db-update','--skip-java-db-update','--format','json','--exit-code','1','/project'] if tool=='trivy' else ['dir:/project','-o','json']
 command=[str(R/'scripts/toolbox.sh'),'exec','--tool',tool,'--project-root',str(base/'fixtures'),'--results',str(dest),'--timeout','180','--diagnostic-file',str(dest/'execution.json'),'--',*argv]
 run=subprocess.run(command,capture_output=True,env=dict(os.environ,TOOLBOX_BIN=str(candidate/'bin/toolbox')));(dest/'stdout').write_bytes(run.stdout);(dest/'stderr').write_bytes(run.stderr)
 meta=json.loads((dest/'execution.json').read_text());report=json.loads(run.stdout);content=bool(report['matches']) if tool=='grype' else any(x.get('Vulnerabilities') for x in report['Results'])
 passed=content and run.returncode==(1 if tool=='trivy' else 0) and meta['outcome']=='native' and meta['cleanup']=='removed' and meta['database']==json.loads(desired)['database']
 rows.append({'tool':tool,'command':command,'exit':run.returncode,'passed':passed,'database':meta.get('database')});(out/'results.json').write_text(json.dumps(rows,indent=2));print(tool,passed,flush=True)
 if not passed:pointer.write_bytes(before);raise RuntimeError('Updated database qualification failed')
