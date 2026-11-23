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
 fixtures=[(OUT/'fixtures'/'Projeto de validação').resolve()]
 for fixture in fixtures:fixture.mkdir(parents=True)
 state=OUT/'state'/'ox';state.mkdir(parents=True)
 data=b'OXRECENT'+(1).to_bytes(4,'little')+len(fixtures).to_bytes(4,'little')
 for fixture in fixtures:
  value=str(fixture).encode();data+=len(value).to_bytes(4,'little')+value
 (state/'recent-projects.v1').write_bytes(data)
 with (OUT/'application.log').open('w') as log:
  app=subprocess.Popen([str(binary)],cwd=ROOT,env=dict(session.env,WAYLAND_DEBUG='1',XDG_STATE_HOME=str(OUT/'state')),stdout=log,stderr=log);session.children.append(app)
  session.wait(lambda:'xdg_toplevel' in (OUT/'application.log').read_text(),'toplevel');time.sleep(.7);session.key(0xFFE1)
  session.wait(lambda:'.enter(' in (OUT/'application.log').read_text(),'keyboard')
  configs=lambda:re.findall(r'xdg_toplevel#\d+\.configure\((\d+), (\d+),',(OUT/'application.log').read_text())
  if int(configs()[-1][0])<monitor_w:chord(0xFFE9,0xFFC7);time.sleep(.5)
  record['initial_window_configure']=[int(v) for v in configs()[-1]]
  shot('initial');move(monitor_w-26,60);time.sleep(.8);shot('settings-hover')
  move(monitor_w//2,100);session.key(0xFF09);shot('settings-keyboard')
  # Open the actual settings cog, preview Dark, discard, then save and reopen.
  move(monitor_w-26,60);button(True);button(False);time.sleep(.3);shot('settings')
  session.key(0xFF09);session.key(0xFF09);session.key(0xFF0D);shot('settings-dark-preview')
  session.key(0xFF1B);shot('back-discarded')
  move(monitor_w-26,60);button(True);button(False);time.sleep(.3)
  session.key(0xFF09);session.key(0xFF09);session.key(0xFF0D)
  for _ in range(5):session.key(0xFF09)
  shot('save-focused');session.key(0xFF0D);shot('saved-dark')
  move(monitor_w-26,60);button(True);button(False);time.sleep(.3);shot('settings-reopened')
  session.key(0xFF1B)
  # Activate Plugins with the pointer at the bottom of the fixed sidebar.
  move(80,monitor_h-60);button(True);button(False);time.sleep(.3);shot('plugins')
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
