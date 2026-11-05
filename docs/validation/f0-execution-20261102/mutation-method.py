from pathlib import Path
import shutil,subprocess,json,hashlib
root=Path('/home/rodrigo/Projetos/ox'); out=root/'docs/validation/f0-execution-20261102/mutations';out.mkdir(exist_ok=True)
target=Path('/tmp/ox-f0-mutations');shutil.copytree(root/'application/crates',target/'crates')
for name in ['Cargo.toml','Cargo.lock','rust-toolchain.toml']:shutil.copy2(root/'application'/name,target/name)
cases=[('stale-input','crates/ox-verification/src/engine.rs','observation.check != *check || observation.before != current','observation.check != *check','ox-verification','failure_history_survives_repair'),('grant-bypass','crates/ox-plugin/src/host.rs','if !self.allowed {','if false {','ox-plugin','incompatible_and_unauthorized'),('late-ui','crates/ox-ui/src/desktop.rs','if g == self.generation && self.busy','if self.busy','ox-ui','busy_and_stale_events')]
rows=[]
for name,rel,old,new,package,test in cases:
 p=target/rel;before=p.read_text();assert old in before;p.write_text(before.replace(old,new,1));(out/(name+'.rs')).write_bytes(p.read_bytes())
 cmd=['cargo','test','-p',package,'--locked','--offline',test,'--','--nocapture']
 with (out/(name+'.log')).open('w') as log:r=subprocess.run(cmd,cwd=target,stdout=log,stderr=subprocess.STDOUT)
 rows.append({'name':name,'mutation':{'path':rel,'before':old,'after':new},'command':cmd,'exit':r.returncode,'log':name+'.log','compiled': 'Finished `test`' in (out/(name+'.log')).read_text(),'test_failed':'test result: FAILED' in (out/(name+'.log')).read_text()})
 p.write_text(before)
(out/'results.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows,indent=2))
