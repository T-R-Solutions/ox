import os, pathlib, subprocess, time, dbus, json
r=pathlib.Path('/home/rodrigo/Projetos/ox/docs/validation/product-bootstrap/wayland-native')
env=dict(os.environ,WAYLAND_DEBUG='1'); env.pop('DISPLAY',None)
result={'method':'native Wayland process with DISPLAY removed; WAYLAND_DEBUG=1; bounded 15-second observation','environment':{k:env.get(k) for k in ['WAYLAND_DISPLAY','XDG_SESSION_TYPE','XDG_RUNTIME_DIR','DISPLAY']}}
with (r/'native-probe.stderr.log').open('w') as err,(r/'native-probe.stdout.log').open('w') as out:
 app=subprocess.Popen(['/home/rodrigo/Projetos/ox/application/target/debug/ox'],env=env,stderr=err,stdout=out)
 result['pid']=app.pid
 try:
  time.sleep(3)
  result['exit_before_capture']=app.poll()
  bus=dbus.SessionBus()
  try:
   obj=bus.get_object('org.gnome.Shell.Screenshot','/org/gnome/Shell/Screenshot')
   result['screenshot']=str(obj.ScreenshotWindow(True,False,False,str(r/'native-probe.png'),dbus_interface='org.gnome.Shell.Screenshot',timeout=10))
  except Exception as e: result['screenshot_error']=str(e)
  try:
   obj=bus.get_object('org.gnome.Shell','/org/gnome/Shell/Introspect')
   result['windows']=str(obj.GetWindows(dbus_interface='org.gnome.Shell.Introspect',timeout=10))
  except Exception as e: result['windows_error']=str(e)
 finally:
  if app.poll() is None:
   result['cleanup']='SIGTERM to owned probe process; not UI/native-close acceptance'; app.terminate()
  try: result['exit_code']=app.wait(timeout=5)
  except subprocess.TimeoutExpired: app.kill(); result['exit_code']=app.wait(); result['cleanup']='SIGKILL after 5 seconds'
(r/'native-probe.json').write_text(json.dumps(result,indent=2)+'\n'); print(json.dumps(result,indent=2))
