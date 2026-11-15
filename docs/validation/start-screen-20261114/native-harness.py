import argparse, hashlib, importlib.util, json, subprocess, time
from pathlib import Path
ROOT=Path('/home/rodrigo/Projetos/ox')
p=argparse.ArgumentParser();p.add_argument('--name',required=True);p.add_argument('--monitor',default='1440x900');p.add_argument('--flow',action='store_true');p.add_argument('--details',action='store_true');a=p.parse_args()
spec=importlib.util.spec_from_file_location('native',ROOT/'docs/validation/f0-resumption-20261103/native-session.py');n=importlib.util.module_from_spec(spec);spec.loader.exec_module(n)
out=ROOT/'docs/validation/start-screen-20261114'/a.name
s=None;app=None;log=None;r={'method':'isolated Mutter Wayland real keyboard and PipeWire captures','monitor':a.monitor,'flow':a.flow}
def chord(mod,key):
 s.key(mod,True);s.key(key);s.key(mod,False)
def tabs(count):
 for _ in range(count):s.key(0xFF09)
def enter():s.key(0xFF0D);time.sleep(.3)
def nav(code):
 chord(0xFFE3,ord('k'))
 for c in code:s.key(ord(c))
 enter()
def fill(value):
 chord(0xFFE3,ord('a'))
 for c in value:s.key(ord(c))
try:
 s=n.Session(out,a.monitor,1)
 binary=ROOT/'application/target/debug/ox';r['binary_sha256']=hashlib.sha256(binary.read_bytes()).hexdigest()
 r['inputs']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'application/crates/ox-ui/src/desktop.rs',ROOT/'application/crates/ox-ui/src/desktop/views.rs']}
 log=(out/'wayland.log').open('w');app=subprocess.Popen([str(binary)],cwd=ROOT,env=dict(s.env,WAYLAND_DEBUG='1',OX_VALIDATION_SESSION=a.name),stdout=log,stderr=log);s.children.append(app)
 s.wait(lambda:'xdg_toplevel' in (out/'wayland.log').read_text(),'native toplevel');time.sleep(.8);s.key(0xFFE1);s.wait(lambda:'.enter(' in (out/'wayland.log').read_text(),'keyboard enter');s.shot('initial')
 nav('A06');nav('S01');s.shot('start-navigation-collapsed')
 if not a.flow:
  if a.details:
   tabs(5);fill('/tmp/'+'long-path-'*20);enter();time.sleep(.7);nav('S01');tabs(3);enter();nav('S01');s.shot('details-expanded')
  tabs(8);s.shot('last-action-keyboard-focus')
  s.key(0xFFE1,True);tabs(3);s.key(0xFFE1,False);s.shot('return-input-keyboard-focus');tabs(1);s.shot('validate-keyboard-focus');s.key(0xFFE1,True);tabs(1);s.key(0xFFE1,False);s.shot('shift-back-input-focus')
 if a.flow:
  tabs(5);fill(str(out/'missing-directory'));enter();time.sleep(.7);nav('S01');s.shot('invalid-path')
  tabs(5);workspace=out/'workspace';workspace.mkdir();(workspace/'sentinel').write_text('preserve original files\n');fill(str(workspace));enter();time.sleep(.8);s.shot('validated-task')
  nav('S01');s.shot('session-resume');tabs(7);s.shot('resume-keyboard-focus');enter();s.shot('resumed-task')
  nav('S04');tabs(7);enter();s.wait(lambda:bool(list(workspace.rglob('result.txt'))),'real task artifact');time.sleep(.5);s.shot('task-executed')
  tabs(4);enter();time.sleep(.8);s.shot('task-verified')
  r['artifacts']=[{'path':str(p.relative_to(workspace)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'text':p.read_text()} for p in workspace.rglob('*') if p.is_file()]
  assert (workspace/'sentinel').read_text()=='preserve original files\n'
  nav('S01');tabs(5);fill(str(workspace)+'-edited');s.shot('edited-path-no-resume')
 for theme in ['dark','high-contrast','light']:
  nav('S01');tabs(1);enter();s.shot(theme)
 tabs(1);enter();s.shot('compact')
 chord(0xFFE3,ord('k'));s.shot('command-keyboard');s.key(0xFF1B);s.shot('escape-return')
 chord(0xFFE9,0xFFC1);s.wait(lambda:app.poll() is not None,'natural exit');r['app_exit']=app.returncode;r['result']='observed'
except Exception as error:
 r['error']=str(error)
 raise
finally:
 if s:s.close()
 if log:log.close()
 out.mkdir(exist_ok=True);(out/'result.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
