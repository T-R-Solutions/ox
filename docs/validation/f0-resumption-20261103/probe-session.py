import os,sys,pathlib,socket,subprocess,time,json
if len(sys.argv)>1 and sys.argv[1]=='bus-child':
 fd=int(sys.argv[2]);os.dup2(fd,3);os.set_inheritable(3,True)
 os.environ.update(LISTEN_FDS='1',LISTEN_PID=str(os.getpid()))
 os.execv('/usr/bin/dbus-broker-launch',['dbus-broker-launch','--scope','user'])
from gi.repository import Gio,GLib
root=pathlib.Path(__file__).resolve().parent
out=root/'session-probe-8';out.mkdir(exist_ok=False)
buspath='/tmp/ox-f0-private-bus-'+str(os.getpid());s=socket.socket(socket.AF_UNIX);s.bind(buspath);s.listen(16)
log=(out/'session.log').open('w');children=[]
import signal
for owned in [2031615,2032017]:
 try:
  cmd=pathlib.Path(f'/proc/{owned}/cmdline').read_bytes()
  if b'mutter\x00--headless\x00' in cmd and b'ox-f0-probe\x00' in cmd:
   os.kill(owned,signal.SIGTERM);print('Terminated probe-owned compositor',owned,flush=True)
 except (FileNotFoundError,ProcessLookupError):pass
try:
 bus=subprocess.Popen(['/usr/bin/python3',__file__,'bus-child',str(s.fileno())],pass_fds=(s.fileno(),),stdout=log,stderr=log);children.append(bus)
 env=dict(os.environ,DBUS_SESSION_BUS_ADDRESS='unix:path='+buspath,LIBGL_ALWAYS_SOFTWARE='1',GIO_USE_VFS='local')
 p=subprocess.Popen(['mutter','--headless','--virtual-monitor','1200x900','--wayland','--no-x11','--wayland-display','ox-f0-probe-'+str(os.getpid())],env=env,stdout=log,stderr=log);children.append(p)
 time.sleep(5)
 result={'bus_pid':bus.pid,'compositor_pid':p.pid,'compositor_exit':p.poll()}
 for service in ['RemoteDesktop','ScreenCast','DisplayConfig']:
  cmd=['gdbus','introspect','--address',env['DBUS_SESSION_BUS_ADDRESS'],'--dest','org.gnome.Mutter.'+service,'--object-path','/org/gnome/Mutter/'+service]
  r=subprocess.run(cmd,text=True,capture_output=True,timeout=5);(out/(service+'.txt')).write_text(r.stdout+r.stderr);result[service]=r.returncode
 connection=Gio.DBusConnection.new_for_address_sync(env['DBUS_SESSION_BUS_ADDRESS'],Gio.DBusConnectionFlags.AUTHENTICATION_CLIENT|Gio.DBusConnectionFlags.MESSAGE_BUS_CONNECTION,None,None)
 for service in ['RemoteDesktop','ScreenCast']:
  name='org.gnome.Mutter.'+service
  args=GLib.Variant('(a{sv})',({},)) if service=='ScreenCast' else None
  try:
   session=connection.call_sync(name,'/org/gnome/Mutter/'+service,name,'CreateSession',args,None,Gio.DBusCallFlags.NONE,3000,None).unpack()[0]
   xml=connection.call_sync(name,session,'org.freedesktop.DBus.Introspectable','Introspect',None,None,Gio.DBusCallFlags.NONE,3000,None).unpack()[0]
   (out/(service+'-session.xml')).write_text(xml)
  except Exception as e:result[service+'_error']=str(e)
 (out/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
finally:
 for p in reversed(children):
  p.terminate()
  try:p.wait(timeout=5)
  except subprocess.TimeoutExpired:p.kill();p.wait()
 s.close();log.close()
