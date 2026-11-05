"""Controlled isolated Mutter session; no primary-desktop input/capture."""
import os,sys,pathlib,socket,subprocess,time,json,threading,hashlib,traceback
import gi
gi.require_version('Gst','1.0')
from gi.repository import Gio,GLib,Gst
from PIL import Image
Gst.init(None)
BASE=pathlib.Path(__file__).resolve().parent;ROOT=BASE.parents[2]
class Session:
 def __init__(self,out):
  self.out=out;out.mkdir(exist_ok=False);self.children=[];self.frames=[];self.latest=None;self.pipeline=None;self.events=[]
  self.log=(out/'compositor.log').open('w');self.buspath='/tmp/ox-f0-bus-'+str(os.getpid());self.sock=socket.socket(socket.AF_UNIX);self.sock.bind(self.buspath);self.sock.listen(16)
  bus=subprocess.Popen(['/usr/bin/python3',str(BASE/'probe-session.py'),'bus-child',str(self.sock.fileno())],pass_fds=(self.sock.fileno(),),stdout=self.log,stderr=self.log);self.children.append(bus)
  self.display='ox-f0-native-'+str(os.getpid());self.env=dict(os.environ,DBUS_SESSION_BUS_ADDRESS='unix:path='+self.buspath,GIO_USE_VFS='local',WAYLAND_DISPLAY=self.display);self.env.pop('DISPLAY',None)
  compositor=subprocess.Popen(['mutter','--headless','--virtual-monitor','1200x900','--wayland','--no-x11','--wayland-display',self.display],env=self.env,stdout=self.log,stderr=self.log);self.children.append(compositor)
  self.conn=Gio.DBusConnection.new_for_address_sync(self.env['DBUS_SESSION_BUS_ADDRESS'],Gio.DBusConnectionFlags.AUTHENTICATION_CLIENT|Gio.DBusConnectionFlags.MESSAGE_BUS_CONNECTION,None,None)
  until=time.monotonic()+15
  while time.monotonic()<until:
   try:self.rd=self.call('RemoteDesktop','/org/gnome/Mutter/RemoteDesktop','CreateSession')[0];break
   except GLib.Error:time.sleep(.1)
  else:raise RuntimeError('compositor readiness exceeded 15s')
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
  self.identity={'compositor_pid':compositor.pid,'bus_pid':bus.pid,'display':self.display,'node':nodes[0],'environment':{'GIO_USE_VFS':'local','backend':'native Wayland, isolated headless Mutter'},'monitor':'1200x900','primary_desktop_input':False}
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
  session=Session(out)
  binary=ROOT/'application/target/debug/ox';log=(out/'wayland.log').open('w');env=dict(session.env,WAYLAND_DEBUG='1',OX_VALIDATION_SESSION=out.name)
  app=subprocess.Popen([str(binary)],env=env,stdout=log,stderr=log);session.children.append(app)
  result.update(binary_sha256=hashlib.sha256(binary.read_bytes()).hexdigest(),pid=app.pid)
  session.wait(lambda:'xdg_toplevel' in (out/'wayland.log').read_text(),'native toplevel');time.sleep(.7);session.shot('initial')
  session.key(0xffe1);session.wait(lambda:'.enter(' in (out/'wayland.log').read_text(),'keyboard enter');time.sleep(.2)
  session.key(0xff09);session.shot('tab-details');session.key(0xff09);session.shot('tab-exit')
  session.key(0xffe1,True);session.key(0xff09);session.key(0xffe1,False);session.shot('shift-tab-details')
  session.key(0xff0d);session.shot('details-expanded')
  session.key(0x20);session.shot('details-collapsed')
  session.key(0xff09);session.key(0xff0d);session.wait(lambda:app.poll() is not None,'application exit');result['app_exit']=app.returncode
 except Exception as e:result['error']=str(e);traceback.print_exc()
 finally:
  if session:session.close()
  out.mkdir(exist_ok=True);(out/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
