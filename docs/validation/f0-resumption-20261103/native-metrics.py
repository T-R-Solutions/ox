import pathlib,importlib.util,subprocess,os,json,time,hashlib,threading,re,sys,traceback
base=pathlib.Path(__file__).resolve().parent;spec=importlib.util.spec_from_file_location('native',base/'native-session.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
if sys.argv[1]=='--remaining':
 for scale,width,height in [(1,640,480),(1.5,900,700),(1.5,640,480),(2,900,700),(2,640,480)]:
  code=subprocess.call(['/usr/bin/python3',__file__,f'native-metrics-{scale}-{width}',str(scale),str(width),str(height)])
  print('cell process exit',code,flush=True)
 sys.exit(0)
scale=float(sys.argv[2]);w=int(sys.argv[3]);h=int(sys.argv[4]);out=base/sys.argv[1];session=None;result={'scale':scale,'logical_size':[w,h]};samples=[];resources=[];stop=threading.Event()
try:
 session=m.Session(out,f'{int(1200*scale)}x{int(900*scale)}',scale)
 binary=pathlib.Path('/tmp/ox-f0-frame-target/debug/ox');logpath=out/'app.log';log=logpath.open('w')
 env=dict(session.env,OX_VALIDATION_WIDTH=str(w),OX_VALIDATION_HEIGHT=str(h),OX_VALIDATION_SESSION=out.name);env.pop('WAYLAND_DEBUG',None)
 app=subprocess.Popen([str(binary)],env=env,stdout=log,stderr=log);session.children.append(app);result['pid']=app.pid;result['binary_sha256']=hashlib.sha256(binary.read_bytes()).hexdigest()
 def rss():
  while not stop.wait(.02):
   try:
    text=pathlib.Path(f'/proc/{app.pid}/status').read_text();resources.append({'time':time.monotonic(),'rss_kib':int(re.search(r'VmRSS:\s+(\d+)',text)[1]),'hwm_kib':int(re.search(r'VmHWM:\s+(\d+)',text)[1])})
   except (FileNotFoundError,TypeError):break
 collector=threading.Thread(target=rss);collector.start()
 time.sleep(.7);session.key(0xffe1);time.sleep(.2);session.key(0xff09);session.shot('focused')
 # Observe content pixels, excluding window title and focus changes.
 def roi(frame):
  stamp,pw,ph,raw=frame;im=m.Image.frombytes('RGB',(pw,ph),raw,'raw','RGB',len(raw)//ph)
  x=int((1200-w)/2*scale);y=int(((900-h-36)/2+36)*scale)
  return im.crop((x,y,x+int(min(w,400)*scale),y+int(200*scale))).tobytes()
 for i in range(23):
  before=roi(session.latest);offset=len(logpath.read_bytes());start=time.monotonic()
  session.call('RemoteDesktop',session.rd,'NotifyKeyboardKeysym','(ub)',(0xff0d,True))
  session.wait(lambda:session.latest[0]>=start and roi(session.latest)!=before,'visible response',3)
  frame_time=session.latest[0];observed=time.monotonic();session.call('RemoteDesktop',session.rd,'NotifyKeyboardKeysym','(ub)',(0xff0d,False));time.sleep(.1)
  chunk=logpath.read_text()[offset:];frames=[float(x) for x in re.findall(r'OX_CLIENT_FRAME_MS=([\d.]+)',chunk)]
  if not frames:raise RuntimeError('client draw timer missing')
  samples.append({'iteration':i,'warmup':i<3,'start':start,'captured_frame_at':frame_time,'observed_at':observed,'response_ms':(frame_time-start)*1000,'poll_observed_ms':(observed-start)*1000,'client_frames_ms':frames})
 session.shot('after-samples');session.key(0xff56);session.shot('page-down');session.key(0xff55)
 def ticks():return sum(map(int,pathlib.Path(f'/proc/{app.pid}/stat').read_text().rsplit(')',1)[1].split()[11:13]))
 idle=[]
 for i in range(3):
  start=time.monotonic();a=ticks();time.sleep(10);b=ticks();elapsed=time.monotonic()-start;idle.append({'seconds':elapsed,'ticks_before':a,'ticks_after':b,'hz':os.sysconf('SC_CLK_TCK'),'percent_one_core':(b-a)/os.sysconf('SC_CLK_TCK')/elapsed*100});print(out.name,'idle',i+1,flush=True)
 result['idle']=idle
 session.key(0xff09);session.key(0xff0d);session.wait(lambda:app.poll() is not None,'natural exit');result['app_exit']=app.returncode
except Exception as e:result['error']=str(e);traceback.print_exc()
finally:
 stop.set()
 if session:session.close()
 out.mkdir(exist_ok=True);result['samples']=samples;result['rss_samples']=resources
 (out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k not in ['samples','rss_samples']}),flush=True)
