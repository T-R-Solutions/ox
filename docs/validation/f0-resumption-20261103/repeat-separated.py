"""Repeat whole X11 cells with incomplete client-frame records, preserving failures."""
from pathlib import Path
import json,re,subprocess,hashlib
B=Path(__file__).resolve().parent;assert (B/'optimized-batch.json').is_file()
rows=[];affected=[]
for scale,w,h in [(1,900,700),(1,640,480),(1.5,900,700),(1.5,640,480),(2,900,700),(2,640,480)]:
 p=B/f'optimized-x11-{scale}-{w}';assert json.loads((p/'result.json').read_text())['exit']==0
 mixed=[{'line':i,'text':line} for i,line in enumerate((p/'test.log').read_text().splitlines(),1) if 'OX_CLIENT_FRAME_MS=' in line and not re.fullmatch(r'OX_CLIENT_FRAME_MS=[0-9]+\.[0-9]+',line)]
 rows.append({'run':p.name,'mixed_frame_lines':mixed})
 if mixed:affected.append((scale,w,h))
(B/'optimized-instrumentation-final-review.json').write_text(json.dumps({'cause':'Parent resource sampler and child frame formatter wrote shared stderr in separate formatting writes. Mixed numeric PID fragments are instrument corruption, not product timing.','correction':'Dedicated child stderr and process resource files; strict full-line numeric validation; repeat entire affected cells.','rows':rows},indent=2)+'\n')
target=Path('/tmp/ox-f0-history-app/crates/ox-app/tests/desktop.rs');assert target.read_bytes()==(B/'optimized-diagnostic-tests.rs.bin').read_bytes();target.write_bytes((B/'optimized-diagnostic-tests-separated.rs.bin').read_bytes())
p=B/'optimized-build-inputs.json';old=B/'optimized-build-inputs-before-separated.json';assert not old.exists();old.write_bytes(p.read_bytes());doc=json.loads(p.read_text());doc['diagnostic_differences']['crates/ox-app/tests/desktop.rs']='optimized-diagnostic-tests-separated.rs.bin';p.write_text(json.dumps(doc,indent=2)+'\n')
results=[]
for scale,w,h in affected:
 cmd=['/usr/bin/python3',str(B/'optimized-separated-x11.py'),f'optimized-separated-x11-{scale}-{w}','optfull',str(scale),str(w),str(h)]
 p=subprocess.run(cmd);results.append({'command':cmd,'exit':p.returncode})
(B/'optimized-separated-batch.json').write_text(json.dumps(results,indent=2)+'\n')
print('Repeated',len(affected),'complete cells with dedicated observation streams',flush=True)
