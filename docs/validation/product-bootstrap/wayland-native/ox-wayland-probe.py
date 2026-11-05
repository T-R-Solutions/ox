import dbus, pathlib
r=pathlib.Path('/home/rodrigo/Projetos/ox/docs/validation/product-bootstrap/wayland-native')
bus=dbus.SessionBus()
lines=[]
def observe(label,fn):
 try: v=fn(); lines.append(label+': '+str(v)); return v
 except Exception as e: lines.append(label+': '+str(e))
name='org.gnome.Mutter.RemoteDesktop'
p=observe('CreateSession',lambda: bus.get_object(name,'/org/gnome/Mutter/RemoteDesktop').CreateSession(dbus_interface=name,timeout=15))
if p:
 obj=bus.get_object(name,p)
 observe('Session interface',lambda: obj.Introspect(dbus_interface='org.freedesktop.DBus.Introspectable',timeout=15))
 observe('Stop',lambda: obj.Stop(dbus_interface=name+'.Session',timeout=15))
observe('Read-only Shell Eval',lambda:bus.get_object('org.gnome.Shell','/org/gnome/Shell').Eval('JSON.stringify(global.get_window_actors().map(a => a.meta_window.get_pid()))',dbus_interface='org.gnome.Shell',timeout=15))
(r/'session-probe.log').write_text('\n'.join(lines)+'\n')
print('\n'.join(lines))
