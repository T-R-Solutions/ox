"""Focus only the Ox window in this runner's own X server; no primary input."""
import ctypes as c,sys,time
x=c.CDLL('libX11.so.6');D=c.c_void_p;W=c.c_ulong
x.XOpenDisplay.argtypes=[c.c_char_p];x.XOpenDisplay.restype=D
x.XDefaultRootWindow.argtypes=[D];x.XDefaultRootWindow.restype=W
x.XQueryTree.argtypes=[D,W,c.POINTER(W),c.POINTER(W),c.POINTER(c.POINTER(W)),c.POINTER(c.c_uint)]
x.XFetchName.argtypes=[D,W,c.POINTER(c.c_char_p)]
x.XSetInputFocus.argtypes=[D,W,c.c_int,c.c_ulong];x.XRaiseWindow.argtypes=[D,W];x.XFlush.argtypes=[D];x.XFree.argtypes=[D];x.XCloseDisplay.argtypes=[D]
d=x.XOpenDisplay(sys.argv[1].encode());assert d
root=x.XDefaultRootWindow(d)
def find(w):
 name=c.c_char_p()
 if x.XFetchName(d,w,c.byref(name)) and name.value:
  title=name.value.decode(errors='replace');x.XFree(c.cast(name,D))
  if title.startswith('Ox'):return w,title
 a=W();p=W();children=c.POINTER(W)();n=c.c_uint()
 if x.XQueryTree(d,w,c.byref(a),c.byref(p),c.byref(children),c.byref(n)):
  ids=[children[i] for i in range(n.value)];x.XFree(children)
  for child in ids:
   found=find(child)
   if found:return found
for _ in range(100):
 found=find(root)
 if found:break
 time.sleep(.05)
assert found,'own Ox window absent'
x.XRaiseWindow(d,found[0]);x.XSetInputFocus(d,found[0],1,0);x.XFlush(d);print(found);x.XCloseDisplay(d)
