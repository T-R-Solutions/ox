from pathlib import Path
import hashlib,json,stat,os
r=Path(__file__).resolve().parents[3];b=Path(__file__).resolve().parent;rows=[]
for directory in sorted(p for p in b.iterdir() if p.is_dir() and not p.name.startswith('before') and p.name!='instrumentation' and p.name!='__pycache__'):
 for p in sorted(directory.rglob('*')):
  mode=p.lstat().st_mode
  if stat.S_ISREG(mode):
   with p.open('rb') as f:sha=hashlib.file_digest(f,'sha256').hexdigest()
   rows.append({'path':str(p.relative_to(r)),'sha256':sha,'bytes':p.stat().st_size})
  elif not stat.S_ISDIR(mode):rows.append({'path':str(p.relative_to(r)),'mode':oct(mode),'content_read':False,'target':os.readlink(p) if stat.S_ISLNK(mode) else None})
(b/'execution-artifacts.json').write_text(json.dumps(rows,indent=2)+'\n');print(len(rows),'raw artifact identities; special files not read')
