from pathlib import Path
import json,re
b=Path(__file__).resolve().parent;rows=[]
for scale in [1,1.5,2]:
 for w,h in [(900,700),(640,480)]:
  for backend in ['native','x11']:
   p=b/f'final-history-{backend}-{scale}-{w}'
   replay=b/f'visible-history-{backend}-{scale}-{w}'
   if (replay/'result.json').exists():p=replay
   d=json.loads((p/'result.json').read_text());assert 'error' not in d,(p,d)
   assert d['app_exit']==0 and d['process_absent'] and d['sentinel_preserved']
   assert d['maximum_observed_run']==32
   assert len(d['samples'])==23 and sum(x['warmup'] for x in d['samples'])==3
   assert len(d['idle'])==3 and all(x['seconds']>=10 for x in d['idle'])
   text=(p/'client.log').read_text();frames=list(map(float,re.findall(r'OX_CLIENT_FRAME_MS=([0-9.]+)',text)));assert frames
   assert 'xdg_toplevel' in text if backend=='native' else (p/'x11-focus.txt').exists()
   row={'run':p.name,'retained_observations':32,'response_max_ms':max(x['response_ms'] for x in d['samples'] if not x['warmup']),'draw_all_frames_max_ms':max(frames),'rss_max_mib':max(x['rss_kib'] for x in d['rss_samples'])/1024,'hwm_max_mib':max(x['hwm_kib'] for x in d['rss_samples'])/1024,'idle_percent':[x['percent'] for x in d['idle']]}
   row['status']='APPROVED' if row['response_max_ms']<=120 and row['draw_all_frames_max_ms']<=125 and row['hwm_max_mib']<=64 and max(row['idle_percent'])<=5 else 'REJECTED'
   rows.append(row)
result={'cells':rows,'status':'APPROVED' if all(x['status']=='APPROVED' for x in rows) else 'REJECTED','authority':'docs/decisions/f0-boundary-20261102.md; 64MiB GUI, not256MiB large renderer-free','method':'3 warmups+20 responses; every client draw; 20ms RSS samples and HWM; three10s idle windows per cell'}
(b/'final-history-checks.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status']);assert result['status']=='APPROVED'
