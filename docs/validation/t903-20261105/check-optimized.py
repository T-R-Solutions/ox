"""Verify the optimized full-flow corpus; never infer passing rows from absent observations."""
from pathlib import Path
import json,re,datetime
B=Path(__file__).resolve().parent
rows=[]
for scale in [1,1.5,2]:
 for w,h in [(900,700),(640,480)]:
  for backend in ['native','x11']:
   p=B/f'optimized-{backend}-{scale}-{w}'
   if backend=='x11' and (B/f'optimized-separated-x11-{scale}-{w}/result.json').exists():p=B/f'optimized-separated-x11-{scale}-{w}'
   r=json.loads((p/'result.json').read_text());assert 'error' not in r,r
   if backend=='native':
    assert r['app_exit']==0 and r['cancel_children_absent']
    samples=r['metric_samples'];assert len(samples)==23 and sum(x['warmup'] for x in samples)==3
    responses=[x['response_ms'] for x in samples if not x['warmup']];idle=[x['percent'] for x in r['idle']]
    assert all(x['seconds']>=10 for x in r['idle'])
    rss=max(x['hwm_kib'] for x in r['rss_samples'])/1024
    text=(p/'wayland.log').read_text();assert all(s in text for s in ['Focus(true)','APPROVED','REJECTED','Cancelled; observed exit'])
    attempts=sorted((p/'workspace').glob('.ox-task-*'));assert len(attempts)==3
    for i,a in enumerate(attempts):
     req=(a/'request.txt').read_bytes()
     if i<2:assert (a/'result.txt').read_bytes()==req+(b'result=42\n' if i==0 else b'result=41\n')
     else:assert not (a/'result.txt').exists()
    assert (p/'workspace/sentinel').read_text()=='preserve native flow\n'
    checks='good/bad exact artifacts, retained verdict history, actual reverse focus, responsive cancel, owned child absent, natural exit 0'
   else:
    assert r['exit']==0,r
    text=(p/'test.log').read_text();assert '7 passed; 0 failed; 0 ignored' in text
    responses=list(map(float,re.findall(r'VISUAL_RESPONSE_MS=([\d.]+)',text)))
    # Other existing tests log separate latency observations; isolate the adopted 20-sample test.
    segment=text[text.index('CELL_MEASUREMENT_BEGIN'):text.index('CELL_MEASUREMENT_END')]
    responses=list(map(float,re.findall(r'VISUAL_RESPONSE_MS=([\d.]+)',segment)))
    idle=[]
    for duration,before,after in re.findall(r'IDLE_SAMPLE=\d+\nGUI_IDLE_SECONDS=([^\n]+)\nGUI_STAT_BEFORE=([^\n]+)\nGUI_STAT_AFTER=([^\n]+)',text):
     ticks=lambda v:sum(map(int,v.rsplit(')',1)[1].split()[11:13]));assert float(duration)>=10
     idle.append((ticks(after)-ticks(before))/100/float(duration)*100)
    resource_text='\n'.join(x.read_text() for x in p.glob('resources-*.log')) if list(p.glob('resources-*.log')) else text
    rss=max(map(int,re.findall(r'VmHWM:\s+(\d+)',resource_text)))/1024
    if list(p.glob('client-*.log')):text='\n'.join(x.read_text() for x in p.glob('client-*.log'))
    checks='seven real graphical cases: metrics, modifiers/focus, flow/history, cancel, held verification, close'
   frame_lines=[line for line in text.splitlines() if 'OX_CLIENT_FRAME_MS=' in line]
   assert all(re.fullmatch(r'OX_CLIENT_FRAME_MS=[0-9]+\.[0-9]+',line) for line in frame_lines),f'Corrupt frame output: {p}'
   frames=list(map(float,re.findall(r'OX_CLIENT_FRAME_MS=([\d.]+)',text)));assert frames
   assert len(responses)==20 and len(idle)==3,(p,len(responses),len(idle))
   row={'backend':'Wayland' if backend=='native' else 'X11','scale':scale,'logical_size':[w,h],'response_max_ms':max(responses),'client_full_corpus_max_ms':max(frames),'client_frame_count':len(frames),'rss_max_mib':rss,'idle_percent':idle,'functional_checks':checks,'run':p.name}
   row['status']='APPROVED' if row['response_max_ms']<=120 and row['client_full_corpus_max_ms']<=125 and rss<=64 and all(v<=5 for v in idle) else 'REJECTED'
   rows.append(row)
result={'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'cells':rows,'status':'APPROVED' if all(r['status']=='APPROVED' for r in rows) else 'REJECTED','method':'maximum of 20 response samples after 3 warmups; every recorded client draw including startup and full history (more conservative than warmup exclusion); lifetime RSS high-water; three 10-second idle windows per cell','limits':['native compositor capture vs X11 client pixels; neither physical exposure','controlled isolated Mutter/Xwayland; no extrapolation to other desktops','diagnostic message logs/client timer/size selectors and external input bridge explicitly retained','finite repetition is not a universal flake-rate estimate','100 Hz CPU ticks: zero measured delta does not mean zero work']}
(B/'optimized-checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(result['status'],len(rows),'cells');assert result['status']=='APPROVED',[(r['run'],r) for r in rows if r['status']!='APPROVED']
