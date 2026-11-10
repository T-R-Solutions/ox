from pathlib import Path
import subprocess,json
R=Path.cwd();base=R/'.local/build/toolbox-completion';cli=base/'candidate/bin/toolbox';out=R/'docs/validation/toolbox-operational-completion/recovery-rehearsal';out.mkdir(exist_ok=False)
def call(label,args):
 r=subprocess.run([str(cli),*args],capture_output=True);(out/(label+'.stdout')).write_bytes(r.stdout);(out/(label+'.stderr')).write_bytes(r.stderr);return r
old=json.loads(call('before',['central','list']).stdout)['ruff']
failed=call('invalid-activation',['central','activate','--tool','ruff','--revision','0'*64]);assert failed.returncode!=0
assert json.loads(call('after-failed',['central','list']).stdout)['ruff']==old
record=base/'candidate/tools/ruff/volume/central/revisions'/(old['revision']+'.json')
new=json.loads(call('register',['central','register','--tool','ruff','--record',str(record)]).stdout)
assert call('activate',['central','activate','--tool','ruff','--revision',new['revision']]).returncode==0
assert call('rollback',['central','rollback','--tool','ruff','--revision',old['revision']]).returncode==0
assert json.loads(call('after-rollback',['central','list']).stdout)['ruff']['revision']==old['revision']
(out/'result.json').write_text(json.dumps({'passed':True,'failed_activation_exit':failed.returncode,'original':old,'rehearsal_revision':new['revision']},indent=2))
