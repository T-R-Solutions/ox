from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import subprocess,os,json,hashlib
R=Path('/home/rodrigo/Projetos/ox');B=R/'.local/build/toolbox-completion';OUT=R/'docs/validation/toolbox-operational-completion/concurrent';OUT.mkdir(exist_ok=False);source=B/'fixtures';cli=B/'candidate/bin/toolbox'
before={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in source.iterdir() if p.is_file()}
def run(item):
 name,args=item;dest=OUT/name;dest.mkdir();cmd=[str(cli),'exec','--tool',name,'--project-root',str(source),'--results',str(dest),'--timeout','90','--diagnostic-file',str(dest/'execution.json'),'--',*args]
 p=subprocess.run(cmd,env=dict(os.environ,TOOLBOX_SELINUX_LABEL='shared'),capture_output=True,timeout=120);(dest/'stdout').write_bytes(p.stdout);(dest/'stderr').write_bytes(p.stderr);m=json.loads((dest/'execution.json').read_text());valid=p.returncode==1 and m['outcome']=='native' and m['cleanup']=='removed'
 if name=='ruff':valid=valid and b'F401' in p.stdout
 else:valid=valid and len(json.loads(p.stdout)['results'])>0
 return {'tool':name,'exit':p.returncode,'passed':valid,'diagnostic':m}
with ThreadPoolExecutor(max_workers=2) as pool:rows=list(pool.map(run,[('ruff',['check','bad.py']),('bandit',['-f','json','bad.py'])]))
after={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in source.iterdir() if p.is_file()}
result={'operations':rows,'source_unchanged':before==after};(OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));raise SystemExit(0 if before==after and all(x['passed'] for x in rows) else 1)
