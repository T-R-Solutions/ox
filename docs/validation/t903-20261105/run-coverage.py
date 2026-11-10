from pathlib import Path
import time,subprocess
b=Path(__file__).resolve().parent
while not (b/'current-final-analysis.log').exists():time.sleep(1)
# Wait for replay analysis to finish writing its final verdict.
while not ('cells' in (b/'current-final-analysis.log').read_text() or 'Traceback' in (b/'current-final-analysis.log').read_text()):time.sleep(1)
with (b/'coverage-current.log').open('w') as log:p=subprocess.run(['/usr/bin/python3',str(b/'coverage-current.py')],stdout=log,stderr=log)
print('coverage',p.returncode,flush=True)
