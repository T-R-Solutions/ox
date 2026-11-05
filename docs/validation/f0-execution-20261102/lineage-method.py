from pathlib import Path
import sys,json,hashlib,tarfile,importlib.util
root=Path(__file__).resolve().parents[3];out=Path(__file__).parent
sys.path.insert(0,str(root/'tools/governance/scripts'))
from governance_support import preservation_bytes,relocated_path
spec=importlib.util.spec_from_file_location('maintenance',root/'tools/governance/scripts/verify-maintenance.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def sha(b):return hashlib.sha256(b).hexdigest()
manifest=json.loads((root/'docs/structure/files.json').read_text());translations=json.loads((root/'docs/validation/english-documentation/translations.json').read_text());metadata={r['destination']:r for v in manifest['revisions'] if v['id']=='skill-ui-metadata-001' for r in v['records']}
rows=[]
with tarfile.open(root/'docs/validation/adoption-baseline/copied-before-adaptation.tar.gz') as archive:
 for r in manifest['revisions'][0]['records']:
  path=('.codex/' if r['destination'].startswith('skills/') else '')+r['destination'];old=archive.extractfile(r['destination']).read();current=(root/path).read_bytes();restored=preservation_bytes(root,path)
  disposition='unchanged' if sha(current)==r['source_sha256'] else ('UI metadata successor' if path in metadata else ('authenticated documentary translation/succession' if sha(restored)==r['source_sha256'] else 'adapted local project document'))
  record=dict(r,current_path=path,current_sha256=sha(current),archive_verified=sha(old)==r['source_sha256'],recovered_sha256=sha(restored),disposition=disposition)
  if path in translations:record['translation']=translations[path]
  if path in metadata:record['metadata_successor']=metadata[path]
  rows.append(record)
(out/'library-lineage.json').write_text(json.dumps(rows,indent=2)+'\n')
rows=[]
with tarfile.open(root/'docs/validation/governance-layout/before.tar.gz') as archive:
 for r in json.loads((root/'docs/validation/governance-layout/relocation.json').read_text()):
  old=archive.extractfile(r['source']).read();p=root/r['destination'];current=p.read_bytes();historical=m.historical_bytes(root,r['destination'],r['sha256'])
  rows.append(dict(r,old_path_absent=not (root/r['source']).exists(),source_archive_verified=sha(old)==r['previous_sha256'],destination_rule_matches=relocated_path(r['source'])==r['destination'],post_relocation_recoverable=historical is not None,current_sha256=sha(current),current_matches_relocation=sha(current)==r['sha256']))
(out/'relocation-lineage.json').write_text(json.dumps(rows,indent=2)+'\n')
print('copies',len(manifest['revisions'][0]['records']),'relocations',len(rows),'unrecovered',[r['destination'] for r in rows if not r['post_relocation_recoverable']])
