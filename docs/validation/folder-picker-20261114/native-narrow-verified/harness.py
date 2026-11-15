import argparse,hashlib,importlib.util,json,subprocess,time
from pathlib import Path
ROOT=Path('/home/rodrigo/Projetos/ox')
p=argparse.ArgumentParser();p.add_argument('--name',required=True);p.add_argument('--narrow',action='store_true');a=p.parse_args()
spec=importlib.util.spec_from_file_location('native',ROOT/'docs/validation/f0-resumption-20261103/native-session.py');n=importlib.util.module_from_spec(spec);spec.loader.exec_module(n)
out=ROOT/'docs/validation/folder-picker-20261114'/a.name
s=None;app=None;log=None;r={'method':'isolated Mutter native Wayland, real Zenity GTK dialog, RemoteDesktop keyboard/PipeWire captures','narrow':a.narrow,'test_environment':{'GDK_DEBUG':'no-portals','GTK_A11Y':'none','GSETTINGS_BACKEND':'memory','GTK_USE_PORTAL':'0'}}
def chord(mod,key):
 s.key(mod,True);s.key(key);s.key(mod,False)
def tabs(count):
 for _ in range(count):s.key(0xFF09)
def click(x,y):
 s.call('RemoteDesktop',s.rd,'NotifyPointerMotionAbsolute','(sdd)',(s.stream,float(x),float(y)))
 s.call('RemoteDesktop',s.rd,'NotifyPointerButton','(ib)',(272,True));s.call('RemoteDesktop',s.rd,'NotifyPointerButton','(ib)',(272,False));time.sleep(.3)
def enter():s.key(0xFF0D);time.sleep(.35)
def nav(code):
 chord(0xFFE3,ord('k'))
 for c in code:s.key(ord(c))
 enter()
def text(value):
 for c in value:s.key(ord(c) if ord(c)<256 else 0x01000000|ord(c))
def chooser_pids():
 ids=set()
 for f in Path(f'/proc/{app.pid}/task').glob('*/children'):
  try:ids.update(f.read_text().split())
  except FileNotFoundError:pass
 found=[]
 for pid in ids:
  try:
   if b'zenity' in Path(f'/proc/{pid}/cmdline').read_bytes():found.append(pid)
  except FileNotFoundError:pass
 return found
def open_chooser():
 nav('S01');tabs(6);s.shot('choose-keyboard-focus');enter();s.wait(lambda:bool(chooser_pids()),'real Zenity child');time.sleep(30);r.setdefault('chooser_pids',[]).append(chooser_pids());s.shot('real-folder-dialog')
def cancel(label):
 s.key(0xFF1B);s.wait(lambda:not chooser_pids(),'cancel reaps chooser');time.sleep(.5);s.shot(label)
try:
 s=n.Session(out,'640x480' if a.narrow else '1440x900',1)
 binary=ROOT/'application/target/debug/ox';r['binary_sha256']=hashlib.sha256(binary.read_bytes()).hexdigest()
 r['inputs']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'application/crates/ox-ui/src').rglob('*.rs')}
 log=(out/'wayland.log').open('w');app=subprocess.Popen([str(binary)],cwd=ROOT,env=dict(s.env,WAYLAND_DEBUG='1',OX_VALIDATION_SESSION=a.name,GDK_DEBUG='no-portals',GTK_A11Y='none',GSETTINGS_BACKEND='memory',GTK_USE_PORTAL='0'),stdout=log,stderr=log);s.children.append(app)
 s.wait(lambda:'xdg_toplevel' in (out/'wayland.log').read_text(),'native toplevel');time.sleep(.8);s.key(0xFFE1);s.wait(lambda:'.enter(' in (out/'wayland.log').read_text(),'keyboard focus');s.shot('initial');nav('A06');nav('S01')
 if a.narrow:
  tabs(3);enter();nav('S01')
 open_chooser();cancel('cancel-empty-focus-restored');tabs(2);s.shot('validate-focus-after-cancel');s.key(0xFFE1,True);tabs(1);s.key(0xFFE1,False);s.shot('shift-back-chooser-focus')
 if not a.narrow:
  workspace=out/'pasta com espaços';workspace.mkdir()
  open_chooser();chord(0xFFE3,ord('l'));text(str(workspace)+'/');s.key(0xFFFF);s.shot('dialog-path-unicode');enter();time.sleep(.5)
  if chooser_pids():enter()
  s.wait(lambda:not chooser_pids(),'confirm reaps chooser');time.sleep(1);s.shot('confirmed-opens-task');r['no_task_before_execution']=not list(workspace.glob('.ox-task-*'));assert r['no_task_before_execution'];(workspace/'sentinel').write_text('preserve existing content\n')
  open_chooser();cancel('cancel-preserves-valid-session');s.shot('session-resume')
  nav('S04');tabs(7);enter();s.wait(lambda:bool(list(workspace.rglob('result.txt'))),'real task artifact');time.sleep(.5);s.shot('task-executed');tabs(4);enter();time.sleep(.8);s.shot('task-verified')
  assert (workspace/'sentinel').read_text()=='preserve existing content\n'
  r['artifacts']=[{'path':str(p.relative_to(workspace)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'text':p.read_text()} for p in workspace.rglob('*') if p.is_file()]
 nav('S01');chord(0xFFE3,ord('k'));s.shot('command-responsive');s.key(0xFF1B);s.shot('escape-return')
 nav('S01');tabs(4);enter();s.wait(lambda:app.poll() is not None,'natural exit');r['app_exit']=app.returncode;r['chooser_children_after_exit']=chooser_pids();assert not r['chooser_children_after_exit'];r['result']='observed'
except Exception as error:
 r['error']=str(error)
 if s:s.shot('failure-state')
 raise
finally:
 if s:s.close()
 if log:log.close()
 out.mkdir(exist_ok=True);(out/'result.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k!='inputs'}))
