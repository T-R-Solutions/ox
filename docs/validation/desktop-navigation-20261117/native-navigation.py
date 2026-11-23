"""Real pointer/keyboard navigation observation in private Mutter, never primary input."""
import argparse, hashlib, importlib.util, json, re, subprocess, time
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[3]; BASE=Path(__file__).resolve().parent
P=argparse.ArgumentParser(description=__doc__); P.add_argument('--name',required=True); P.add_argument('--monitor',default='1366x768'); P.add_argument('--capture-only',action='store_true'); A=P.parse_args()
OUT=BASE/A.name
if OUT.exists(): raise SystemExit('Choose new name; preserve prior evidence')
helper=ROOT/'docs/validation/f0-resumption-20261103/native-session.py'; sp=importlib.util.spec_from_file_location('native',helper); native=importlib.util.module_from_spec(sp);sp.loader.exec_module(native)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
binary=ROOT/'application/target/debug/ox'; paths=list((ROOT/'application/crates/ox-ui/src').rglob('*.rs'))+list((ROOT/'application/crates/ox-ui/assets').rglob('*'))+[ROOT/'application/Cargo.lock',ROOT/'application/Cargo.toml',ROOT/'application/crates/ox-ui/Cargo.toml',Path(__file__),helper]
inputs={str(p.relative_to(ROOT)):digest(p) for p in paths if p.is_file()}; record={'method':'private Mutter native Wayland pointer/keyboard; pixel geometry and native event delivery','monitor':A.monitor,'binary_sha256':digest(binary),'inputs':inputs}; session=None;app=None
try:
 session=native.Session(OUT,A.monitor,1)
 def move(x,y):
  session.call('RemoteDesktop',session.rd,'NotifyPointerMotionAbsolute','(sdd)',(session.stream,float(x),float(y)));session.events.append({'move':[x,y]});time.sleep(.12)
 def button(down):
  session.call('RemoteDesktop',session.rd,'NotifyPointerButton','(ib)',(272,down));session.events.append({'left_button':down});time.sleep(.12)
 def chord(mod,key):
  session.key(mod,True);session.key(key);session.key(mod,False);time.sleep(.2)
 def nav(code):
  chord(0xFFE3,ord('k'))
  for c in code:session.key(ord(c))
  session.key(0xFF0D);time.sleep(.3)
 def shot(name):
  session.shot(name)
  im=Image.open(OUT/(name+'.png')); w,h=im.size
  # Observational pixel measurement; source geometry and visual inspection remain independent oracles.
  scores=[sum(im.getpixel((x,y))[:3]==(242,244,246) for y in range(110,h-60))/max(1,h-170) for x in range(min(w,501))]
  xs=[x for x,v in enumerate(scores) if v>.65]
  raw_edge=max(xs)+1 if xs else None
  # Actual screenshots show the scrollable's 10px gutter after its neutral background.
  # This calibration is checked against the visible divider/source initial256/rail52.
  entry=name in ('initial','settings-hover','settings-keyboard','return-home')
  edge=None if entry or raw_edge is None else raw_edge+10
  record.setdefault('pixel_background_edges',{})[name]=raw_edge
  record.setdefault('pixel_sidebar_edges',{})[name]=edge
  return edge
 def drag(edge,target,label):
  y=min(350,monitor_h-100);move(edge+3,y);button(True)
  for i in range(1,6):move(edge+3+(target-edge)*i/5,y)
  button(False);time.sleep(.2);return shot(label)
 monitor_w,monitor_h=map(int,A.monitor.split('x'))
 # Prime virtual pointer before application binds wl_seat, avoiding a lost initial click.
 move(1,1)
 with (OUT/'application.log').open('w') as log:
  app=subprocess.Popen([str(binary)],cwd=ROOT,env=dict(session.env,WAYLAND_DEBUG='1',XDG_STATE_HOME=str(OUT/'state')),stdout=log,stderr=log);session.children.append(app)
  session.wait(lambda:'xdg_toplevel' in (OUT/'application.log').read_text(),'toplevel');time.sleep(.7);session.key(0xFFE1)
  session.wait(lambda:'.enter(' in (OUT/'application.log').read_text(),'keyboard')
  configs=lambda:re.findall(r'xdg_toplevel#\d+\.configure\((\d+), (\d+),',(OUT/'application.log').read_text())
  if int(configs()[-1][0])<monitor_w:chord(0xFFE9,0xFFC7);time.sleep(.5)
  record['initial_window_configure']=[int(v) for v in configs()[-1]]
  shot('initial');move(monitor_w-26,60);time.sleep(.8);shot('settings-hover')
  move(monitor_w//2,100);session.key(0xFF09);shot('settings-keyboard')
  nav('W00');edge=shot('workbench-expanded')
  if not A.capture_only:
   if edge is None:raise AssertionError('No measurable Light navigation boundary')
   edge=drag(edge,min(edge+80,400),'drag-wider')
   move(min(500,monitor_w-20),350);shot('released-pointer-move')
   edge=drag(edge,550,'drag-max')
   edge=drag(edge,80,'drag-min')
   edge=drag(edge,280,'drag-restored')
   chord(0xFFE3,ord('b'));shot('collapsed-rail');move(26,150);time.sleep(.8);shot('rail-hover')
   chord(0xFFE3,ord('b'));edge=shot('expanded-restored')
   session.key(0xFFE3,True);session.key(0xFFE9,True);session.key(0xFF53);session.key(0xFFE9,False);session.key(0xFFE3,False);shot('keyboard-wider')
   session.key(0xFFE3,True);session.key(0xFFE9,True);session.key(0xFF51);session.key(0xFFE9,False);session.key(0xFFE3,False);edge=shot('keyboard-narrower')
   # Reliable keyboard equivalent: focus the visible shrink/grow buttons, not WM-reserved keys.
   nav('W00')
   for _ in range(6):session.key(0xFF09)
   shot('resize-smaller-keyboard-focus');session.key(0xFF0D);shot('resize-smaller-keyboard')
   session.key(0xFF09);shot('resize-larger-keyboard-focus');session.key(0xFF0D);edge=shot('resize-larger-keyboard')
   # Leave client through native title bar while held, release outside, then move in client.
   move(edge+3,min(350,monitor_h-100));button(True);move(edge+3,10);button(False);move(edge+70,min(350,monitor_h-100));shot('outside-release-safe')
   # Escape terminates a held drag; later motion stays inert.
   move(edge+3,min(350,monitor_h-100));button(True);move(edge+19,min(350,monitor_h-100));session.key(0xFF1B);button(False)
   escaped=shot('escape-drag');move(edge+70,min(350,monitor_h-100));shot('escape-drag-inert')
   if monitor_w>1000:
    move(escaped+3,350);button(True);chord(0xFFE9,0xFFC7);move(600,400);button(False);shot('resize-mid-drag-windowed')
    chord(0xFFE9,0xFFC7);move(escaped+70,350);shot('resize-mid-drag-restored')
   chord(0xFFE3,ord('b'));nav('W00')
   for index in range(1,33):
    session.key(0xFF09)
    if index in (5,6,20,32):shot('rail-focus-'+str(index))
   chord(0xFFE3,ord('b'));shot('last-focus-expanded')
   chord(0xFFE3,ord('b'));shot('last-focus-collapsed')
   session.key(0xFF0D);shot('rail-last-destination')
   nav('S14');shot('rail-navigation-preferences')
   # First traversal after navigation is the existing theme cycle trigger.
   for theme in ['dark','high-contrast','light']:
    session.key(0xFF09);session.key(0xFF0D);shot('preferences-'+theme);nav('W00');shot('workbench-'+theme);nav('S14')
   chord(0xFFE3,ord('b'));shot('preferences-expanded')
  if not A.capture_only:
   edges=record['pixel_sidebar_edges'];maximum=min(420,monitor_w-326)
   assert edges['drag-wider']>edges['workbench-expanded'], edges
   assert edges['released-pointer-move']==edges['drag-wider'], edges
   assert edges['drag-max']==maximum and edges['drag-min']==200, edges
   assert edges['collapsed-rail']==52 and edges['expanded-restored']==edges['drag-restored'], edges
   assert edges['resize-smaller-keyboard']==edges['keyboard-narrower']-24, edges
   assert edges['resize-larger-keyboard']==edges['keyboard-narrower'], edges
   assert edges['outside-release-safe']==edges['resize-larger-keyboard'], edges
   assert edges['escape-drag-inert']==edges['escape-drag'], edges
   if monitor_w>1000:assert edges['resize-mid-drag-restored']==edges['escape-drag'], edges
   record['drag_keyboard_geometry_oracles']='passed'
  nav('S01');shot('return-home')
  chord(0xFFE9,0xFFC1);session.wait(lambda:app.poll() is not None,'natural exit');assert app.returncode==0
  record['natural_exit']=app.returncode;record['result']='observed; inspect captures and geometry'
except Exception as e:
 record['error']=str(e)
 if session:session.shot('failure')
 raise
finally:
 if session:session.close()
 OUT.mkdir(exist_ok=True);record['sources_stable']=all((ROOT/p).is_file() and digest(ROOT/p)==v for p,v in inputs.items());record['binary_stable']=digest(binary)==record['binary_sha256'];(OUT/'result.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps({k:v for k,v in record.items() if k!='inputs'}))
