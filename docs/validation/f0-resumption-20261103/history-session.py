"""Controlled isolated Mutter session; no primary-desktop input/capture."""
import os,sys,pathlib,socket,subprocess,time,json,threading,hashlib,traceback
import gi
gi.require_version('Gst','1.0')
from gi.repository import Gio,GLib,Gst
from PIL import Image
Gst.init(None)
BASE=pathlib.Path(__file__).resolve().parent;ROOT=BASE.parents[2]
class Session:
 def __init__(self,out,monitor='1200x900',scale=1.0):
  self.out=out;out.mkdir(exist_ok=False);self.children=[];self.frames=[];self.latest=None;self.pipeline=None;self.events=[]
  self.log=(out/'compositor.log').open('w');self.buspath='/tmp/ox-f0-bus-'+str(os.getpid());self.sock=socket.socket(socket.AF_UNIX);self.sock.bind(self.buspath);self.sock.listen(16)
  bus=subprocess.Popen(['/usr/bin/python3',str(BASE/'probe-session.py'),'bus-child',str(self.sock.fileno())],pass_fds=(self.sock.fileno(),),stdout=self.log,stderr=self.log);self.children.append(bus)
  self.display='ox-f0-native-'+str(os.getpid());self.env=dict(os.environ,DBUS_SESSION_BUS_ADDRESS='unix:path='+self.buspath,GIO_USE_VFS='local',WAYLAND_DISPLAY=self.display);self.env.pop('DISPLAY',None)
  compositor=subprocess.Popen(['mutter','--headless','--virtual-monitor',monitor,'--wayland','--no-x11','--wayland-display',self.display],env=self.env,stdout=self.log,stderr=self.log);self.children.append(compositor)
  self.conn=Gio.DBusConnection.new_for_address_sync(self.env['DBUS_SESSION_BUS_ADDRESS'],Gio.DBusConnectionFlags.AUTHENTICATION_CLIENT|Gio.DBusConnectionFlags.MESSAGE_BUS_CONNECTION,None,None)
  until=time.monotonic()+15
  while time.monotonic()<until:
   try:self.rd=self.call('RemoteDesktop','/org/gnome/Mutter/RemoteDesktop','CreateSession')[0];break
   except GLib.Error:time.sleep(.1)
  else:raise RuntimeError('compositor readiness exceeded 15s')
  state=self.conn.call_sync('org.gnome.Mutter.DisplayConfig','/org/gnome/Mutter/DisplayConfig','org.gnome.Mutter.DisplayConfig','GetCurrentState',None,None,Gio.DBusCallFlags.NONE,3000,None).unpack()
  (out/'display-state.json').write_text(json.dumps(state,indent=2)+'\n')
  if scale!=1:
   serial,monitors,logical,props=state;connector=monitors[0][0][0];mode=monitors[0][1][0][0]
   self.conn.call_sync('org.gnome.Mutter.DisplayConfig','/org/gnome/Mutter/DisplayConfig','org.gnome.Mutter.DisplayConfig','ApplyMonitorsConfig',GLib.Variant('(uua(iiduba(ssa{sv}))a{sv})',(serial,1,[(0,0,scale,0,True,[(connector,mode,{})])],{})),None,Gio.DBusCallFlags.NONE,3000,None)
  applied=self.conn.call_sync('org.gnome.Mutter.DisplayConfig','/org/gnome/Mutter/DisplayConfig','org.gnome.Mutter.DisplayConfig','GetCurrentState',None,None,Gio.DBusCallFlags.NONE,3000,None).unpack()
  (out/'display-applied.json').write_text(json.dumps(applied,indent=2)+'\n')
  assert applied[2][0][2]==scale, 'compositor scale mismatch'
  sid=self.conn.call_sync('org.gnome.Mutter.RemoteDesktop',self.rd,'org.freedesktop.DBus.Properties','Get',GLib.Variant('(ss)',('org.gnome.Mutter.RemoteDesktop.Session','SessionId')),None,Gio.DBusCallFlags.NONE,3000,None).unpack()[0]
  self.sc=self.call('ScreenCast','/org/gnome/Mutter/ScreenCast','CreateSession','(a{sv})',({'remote-desktop-session-id':GLib.Variant('s',sid)},))[0]
  self.stream=self.call('ScreenCast',self.sc,'RecordMonitor','(sa{sv})',('Meta-0',{'cursor-mode':GLib.Variant('u',0)}))[0]
  nodes=[]
  self.conn.signal_subscribe('org.gnome.Mutter.ScreenCast','org.gnome.Mutter.ScreenCast.Stream','PipeWireStreamAdded',self.stream,None,Gio.DBusSignalFlags.NONE,lambda c,s,p,i,n,args,data:nodes.append(args.unpack()[0]),None)
  self.call('RemoteDesktop',self.rd,'Start')
  until=time.monotonic()+10
  while not nodes and time.monotonic()<until:
   while GLib.MainContext.default().iteration(False):pass
   time.sleep(.01)
  if not nodes:raise RuntimeError('missing PipeWire node')
  self.pipeline=Gst.parse_launch(f'pipewiresrc path={nodes[0]} do-timestamp=true ! videoconvert ! video/x-raw,format=RGB ! appsink name=sink emit-signals=true max-buffers=1 drop=true sync=false')
  sink=self.pipeline.get_by_name('sink');sink.connect('new-sample',self.sample)
  self.pipeline.set_state(Gst.State.PLAYING)
  self.wait(lambda:self.latest is not None,'first monitor frame')
  self.identity={'compositor_pid':compositor.pid,'bus_pid':bus.pid,'display':self.display,'node':nodes[0],'environment':{'GIO_USE_VFS':'local','backend':'native Wayland, isolated headless Mutter'},'monitor':monitor,'scale':scale,'primary_desktop_input':False}
  (out/'environment.json').write_text(json.dumps(self.identity,indent=2)+'\n')
 def call(self,service,path,method,sig=None,args=()):
  interface='org.gnome.Mutter.'+service+('' if path=='/org/gnome/Mutter/'+service else '.Session')
  result=self.conn.call_sync('org.gnome.Mutter.'+service,path,interface,method,GLib.Variant(sig,args) if sig else None,None,Gio.DBusCallFlags.NONE,5000,None)
  return result.unpack() if result else ()
 def sample(self,sink):
  s=sink.emit('pull-sample');b=s.get_buffer();caps=s.get_caps().get_structure(0);w=caps.get_value('width');h=caps.get_value('height');raw=b.extract_dup(0,b.get_size());now=time.monotonic()
  self.latest=(now,w,h,raw);self.frames.append(now)
  return Gst.FlowReturn.OK
 def wait(self,fn,label,timeout=15):
  end=time.monotonic()+timeout
  while time.monotonic()<end:
   if fn():return
   while GLib.MainContext.default().iteration(False):pass
   time.sleep(.02)
  raise RuntimeError('timeout: '+label)
 def key(self,sym,pressed=None):
  for state in ([True,False] if pressed is None else [pressed]):
   self.events.append({'time':time.monotonic(),'keysym':sym,'pressed':state})
   self.call('RemoteDesktop',self.rd,'NotifyKeyboardKeysym','(ub)',(sym,state));time.sleep(.04)
 def shot(self,label):
  time.sleep(.15);stamp,w,h,raw=self.latest
  im=Image.frombytes('RGB',(w,h),raw,'raw','RGB',len(raw)//h);im.save(self.out/(label+'.png'))
  self.events.append({'time':time.monotonic(),'capture':label,'frame_time':stamp,'size':[w,h]})
 def close(self):
  if self.pipeline:self.pipeline.set_state(Gst.State.NULL)
  for p in reversed(self.children):
   if p.poll() is None:
    p.terminate()
    try:p.wait(timeout=5)
    except subprocess.TimeoutExpired:p.kill();p.wait()
  self.sock.close();self.log.close()
  (self.out/'events.json').write_text(json.dumps(self.events,indent=2)+'\n')
if __name__=='__main__':
 out=BASE/(sys.argv[1] if len(sys.argv)>1 else 'native-probe-1');session=None;result={}
 try:
  cell=sys.argv[sys.argv.index('--cell')+1:sys.argv.index('--cell')+4] if '--cell' in sys.argv else None
  scale,w,h=(float(cell[0]),int(cell[1]),int(cell[2])) if cell else (1,900,700)
  session=Session(out,f'{int(1200*scale)}x{int(900*scale)}',scale)
  binary=pathlib.Path('/tmp/ox-f0-history-target/debug/ox') if cell else ROOT/'application/target/debug/ox';log=(out/'wayland.log').open('w');env=dict(session.env,WAYLAND_DEBUG='1',OX_VALIDATION_SESSION=out.name,OX_VALIDATION_WIDTH=str(w),OX_VALIDATION_HEIGHT=str(h))
  app=subprocess.Popen([str(binary)],env=env,stdout=log,stderr=log);session.children.append(app)
  rss_samples=[];rss_stop=threading.Event()
  def collect_rss():
   import re
   while not rss_stop.wait(.02):
    try:
     status=pathlib.Path(f'/proc/{app.pid}/status').read_text()
     rss_samples.append({'time':time.monotonic(),'rss_kib':int(re.search(r'VmRSS:\s+(\d+)',status)[1]),'hwm_kib':int(re.search(r'VmHWM:\s+(\d+)',status)[1])})
    except (FileNotFoundError,TypeError):break
  threading.Thread(target=collect_rss,daemon=True).start()
  result.update(scale=scale,logical_size=[w,h],instrumented=bool(cell),binary_sha256=hashlib.sha256(binary.read_bytes()).hexdigest(),pid=app.pid)
  session.wait(lambda:'xdg_toplevel' in (out/'wayland.log').read_text(),'native toplevel');time.sleep(.7);session.shot('initial')
  session.key(0xffe1);session.wait(lambda:'.enter(' in (out/'wayland.log').read_text(),'keyboard enter');time.sleep(.2)
  session.key(0xff09);session.shot('tab-details');session.key(0xff09);session.shot('tab-exit')
  session.key(0xffe1,True);session.key(0xff09);session.key(0xffe1,False);session.shot('shift-tab-details')
  session.key(0xff0d);session.shot('details-expanded')
  session.key(0x20);session.shot('details-collapsed')
  if '--flow' in sys.argv:
   workspace=out/'workspace';workspace.mkdir();(workspace/'sentinel').write_text('preserve native flow\n');result['workspace']=str(workspace)
   def tabs(n,back=False):
    if back:session.key(0xffe1,True)
    for _ in range(n):session.key(0xff09)
    if back:session.key(0xffe1,False)
   def enter():session.key(0xff0d);time.sleep(.2)
   tabs(2)
   for ch in str(workspace):session.key(ord(ch))
   tabs(1);enter();session.shot('workspace-valid')
   tabs(1);enter()
   session.wait(lambda:len(list(workspace.glob('.ox-task-*/result.txt')))==1,'good artifact')
   tabs(4);enter();session.shot('approved');session.key(0xff56);session.shot('approved-history');session.key(0xff55)
   tabs(3,True);enter()
   session.wait(lambda:len(list(workspace.glob('.ox-task-*/result.txt')))==2,'bad artifact')
   tabs(3);enter();session.shot('rejected');session.key(0xff56);session.shot('retained-history');session.key(0xff55)
   tabs(1,True);enter()
   def children():
    ids=[]
    for p in pathlib.Path(f'/proc/{app.pid}/task').glob('*/children'):
     try:ids.extend(p.read_text().split())
     except FileNotFoundError:pass
    return [pid for pid in ids if pathlib.Path('/proc/'+pid+'/cmdline').exists() and b'local-task' in pathlib.Path('/proc/'+pid+'/cmdline').read_bytes()]
   session.wait(lambda:bool(children()),'owned hang child');owned=children();result['cancel_children']=owned
   tabs(1);enter();session.shot('responsive-during-hang');enter()
   tabs(2);enter();session.wait(lambda:all(not pathlib.Path('/proc/'+pid).exists() for pid in owned),'cancelled child exit');session.shot('cancelled');result['cancel_children_absent']=True
   assert (workspace/'sentinel').read_text()=='preserve native flow\n'
   artifacts=[]
   for path in sorted(workspace.rglob('*')):
    if path.is_file():artifacts.append({'path':str(path.relative_to(workspace)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'content':path.read_text()})
   (out/'artifacts.json').write_text(json.dumps(artifacts,indent=2)+'\n')
   tabs(2);enter()
  else:
   session.key(0xff09);session.key(0xff0d)
  session.wait(lambda:app.poll() is not None,'application exit');result['app_exit']=app.returncode
 except Exception as e:result['error']=str(e);traceback.print_exc()
 finally:
  if 'rss_stop' in locals():
   rss_stop.set();result['rss_samples']=rss_samples
  if session:session.close()
  out.mkdir(exist_ok=True);(out/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='rss_samples'}),flush=True)
