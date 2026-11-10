from pathlib import Path
import subprocess,os,json
R=Path.cwd();base=R/'.local/build/toolbox-completion';candidate=base/'candidate';out=R/'docs/validation/toolbox-operational-completion/updates';out.mkdir(exist_ok=False)
for name,version,argv,env in [('grype','0.119.0',['db','update'],['--env','GRYPE_DB_AUTO_UPDATE=true']),('trivy','0.76.2',['fs','--download-db-only','--no-progress'],['--env','TRIVY_SKIP_DB_UPDATE=false'])]:
 dest=out/name;dest.mkdir();pointer=candidate/'tools'/name/'volume/databases'/version/'current.json';before=pointer.read_bytes();(dest/'pointer-before.json').write_bytes(before)
 command=[str(R/'scripts/toolbox.sh'),'exec','--tool',name,'--project-root',str(base/'fixtures'),'--results',str(dest),'--maintenance','--network','bridge','--timeout','600','--diagnostic-file',str(dest/'execution.json'),*env,'--',*argv]
 run=subprocess.run(command,capture_output=True,env=dict(os.environ,TOOLBOX_BIN=str(candidate/'bin/toolbox')))
 (dest/'stdout').write_bytes(run.stdout);(dest/'stderr').write_bytes(run.stderr);(dest/'pointer-after.json').write_bytes(pointer.read_bytes())
 print(name,run.returncode,flush=True)
 (dest/'result.json').write_text(json.dumps({'command':command,'exit':run.returncode,'selection_changed':before!=pointer.read_bytes()},indent=2))
 # Selection recovery is verified before future qualification/promotion; originals remain.
 pointer.write_bytes(before)
