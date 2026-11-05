"""Independent artifact/contract checks; screenshots require the separate visual review."""
import pathlib,json,re,hashlib,datetime
B=pathlib.Path(__file__).resolve().parent;rows=[];checks=[]
def read(p):return json.loads(p.read_text())
for scale in [1,1.5,2]:
 for width,height in [(900,700),(640,480)]:
  native=B/f'native-metrics-{scale}-{width}';d=read(native/'result.json');s=[x for x in d['samples'] if not x['warmup']]
  assert len(s)==20 and len(d['idle'])==3 and d['app_exit']==0 and 'error' not in d
  row={'backend':'Wayland','scale':scale,'logical_size':[width,height],'response_max_ms':max(x['response_ms'] for x in s),'client_max_ms':max(t for x in s for t in x['client_frames_ms']),'rss_max_mib':max(x['rss_kib'] for x in d['rss_samples'])/1024,'idle_percent':[x['percent_one_core'] for x in d['idle']],'artifact':str((native/'result.json').relative_to(B))};rows.append(row)
  x11=B/f'x11-metrics-{scale}-{width}';d=read(x11/'result.json');text=(x11/'test.log').read_text();assert d['exit']==0
  responses=list(map(float,re.findall(r'VISUAL_RESPONSE_MS=([\d.]+)',text)));a=text.index('CELL_MEASUREMENT_BEGIN');b=text.index('CELL_MEASUREMENT_END');frames=list(map(float,re.findall(r'OX_CLIENT_FRAME_MS=([\d.]+)',text[a:b])));assert len(responses)==len(frames)==20
  idle=[]
  for duration,before,after in re.findall(r'GUI_IDLE_SECONDS=([^\n]+)\nGUI_STAT_BEFORE=([^\n]+)\nGUI_STAT_AFTER=([^\n]+)',text):
   ticks=lambda v:sum(map(int,v.rsplit(')',1)[1].split()[11:13]));idle.append((ticks(after)-ticks(before))/100/float(duration)*100)
  assert len(idle)==3
  rows.append({'backend':'X11','scale':scale,'logical_size':[width,height],'response_max_ms':max(responses),'client_max_ms':max(frames),'rss_max_mib':max(map(int,re.findall(r'VmHWM:\s+(\d+)',text)))/1024,'idle_percent':idle,'artifact':str((x11/'test.log').relative_to(B))})
  support=B/f'native-support-{scale}-{width}';r=read(support/'result.json');assert r['app_exit']==0 and r['cancel_children_absent'] and 'error' not in r
  log=(support/'wayland.log').read_text();assert 'Focus(true)' in log and 'APPROVED' in log and 'REJECTED' in log and 'Cancelled; observed exit' in log
  ws=support/'workspace';attempts=sorted(ws.glob('.ox-task-*'));assert len(attempts)==3
  for i,p in enumerate(attempts):
   req=(p/'request.txt').read_bytes()
   if i<2:assert (p/'result.txt').read_bytes()==req+(b'result=42\n' if i==0 else b'result=41\n')
   else:assert not (p/'result.txt').exists()
  assert (ws/'sentinel').read_text()=='preserve native flow\n'
  x=B/f'x11-support-{scale}-{width}';assert read(x/'result.json')['exit']==0
  assert '6 passed; 0 failed; 0 ignored' in (x/'test.log').read_text()
  checks.append({'cell':[scale,width,height],'native_artifacts':'good=42; bad=41; cancelled missing; sentinel preserved','native_processes':'cancel child absent; natural exit 0','x11_tests':6,'visual_inspection':'separate graphical-review.md'})
for row in rows:
 assert row['response_max_ms']<=120 and row['client_max_ms']<=125 and row['rss_max_mib']<=64 and all(x<=5 for x in row['idle_percent']),row
for i in range(1,4):
 r=read(B/f'native-held-{i}/result.json');assert r['app_exit']==0 and r['second_absent'] and 'error' not in r
 r=read(B/f'x11-covered-held-{i}/result.json');assert r['exit']==0
 assert '1 passed; 0 failed; 0 ignored' in (B/f'x11-covered-held-{i}/test.log').read_text()
primary=read(B/'primary-native-1/correlation-review.json');assert primary['status']=='APPROVED'
result={'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'exact controlled artifact bytes/identities, raw logged outcomes, process observations, per-cell warmup/sample/resource checks against adopted contract','status':'APPROVED','cells':rows,'functional_checks':checks,'native_held_repeats':3,'covered_x11_held_repeats':3,'limits':['copied diagnostic sizing/logging/frame timer explicitly identified','native performance is isolated headless Mutter, primary-session journey separately human observed','X11 pixels are client framebuffer; Wayland pixels are compositor capture; neither is physical scanout','CPU zero ticks at 100 Hz over 10 seconds is below observation resolution, not proof of zero work','finite corpus and repetitions do not establish universal flake rate; historical failures retained']}
(B/'observation-checks.json').write_text(json.dumps(result,indent=2)+'\n');print('12 metric cells; 6 native journeys; 36 X11 tests; 3 native held; 3 covered X11 held: PASS')
