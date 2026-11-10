from pathlib import Path
import sys,json
sys.path.insert(0,str(Path('.local/build/toolbox-completion/candidate').resolve()))
from toolbox.prepare import update_osv_database
from toolbox.storage import Store
root=Path('.local/build/toolbox-completion/candidate').resolve()
record=json.loads(Path('.local/build/operational-qualification/osv-scanner-image.json').read_text())
result=update_osv_database(Store(root/'.local/state',root/'tools'),{'version':record['version']},{'tools':{'osv-scanner':record}})
Path('docs/validation/toolbox-operational-completion/osv-preparation.json').write_text(json.dumps(result,indent=2))
