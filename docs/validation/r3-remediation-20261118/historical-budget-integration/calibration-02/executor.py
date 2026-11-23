"""Bounded diagnostic budget measurement; does not change the live test deadline."""
from pathlib import Path
import hashlib
import importlib.util
import json
import subprocess
import sys
import time
import unittest

root = Path('/home/rodrigo/Projetos/ox')
output = Path('/tmp/ox-r3-historical-budget-calibration-02')
output.mkdir()
source_path = root / 'tools/governance/tests/test_historical_link_resolution.py'
before = source_path.read_bytes()
candidate = before.replace(b'timeout=120)', b'timeout=600)')
if candidate == before or before.count(b'timeout=120)') != 1:
    raise RuntimeError('Unexpected diagnostic timeout substitution')
candidate_path = output / 'source/tools/governance/tests/test_historical_link_resolution.py'
candidate_path.parent.mkdir(parents=True)
candidate_path.write_bytes(candidate)
sys.path.insert(0, str(root / 'tools/governance/scripts'))
from governance_support import distribution_files


def manifest():
    return {str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in distribution_files(root)}


inputs = manifest()
(output / 'inputs-before.json').write_text(json.dumps(inputs, indent=2) + '\n')
spec = importlib.util.spec_from_file_location('candidate_historical_budget', candidate_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
# Candidate assertion code is unchanged; explicitly bind its real fixture source.
module.ROOT = root
original_run = subprocess.run
calls = []


def observed_run(command, *args, **kwargs):
    index = len(calls)
    row = {'argv': list(map(str, command)), 'timeout': kwargs.get('timeout'),
           'cwd': str(kwargs.get('cwd')), 'started_monotonic': time.perf_counter()}
    calls.append(row)
    try:
        result = original_run(command, *args, **kwargs)
        row['exit_code'] = result.returncode
        for stream in ('stdout', 'stderr'):
            data = getattr(result, stream)
            if data is not None:
                (output / f'command-{index:02}-{stream}.log').write_bytes(data.encode() if isinstance(data, str) else data)
        return result
    except subprocess.TimeoutExpired as error:
        row['timeout_expired'] = True
        for stream in ('stdout', 'stderr'):
            data = getattr(error, stream)
            if data is not None:
                (output / f'command-{index:02}-{stream}.log').write_bytes(data.encode() if isinstance(data, str) else data)
        raise
    finally:
        row['seconds'] = time.perf_counter() - row['started_monotonic']
        (output / 'commands.json').write_text(json.dumps(calls, indent=2) + '\n')


subprocess.run = observed_run
started = time.perf_counter()
try:
    suite = unittest.TestSuite([module.PublicHistoricalLinkTests('test_public_copy_rejects_unregistered_live_readme_append')])
    result = unittest.TextTestRunner(verbosity=2).run(suite)
finally:
    subprocess.run = original_run
after = manifest()
(output / 'inputs-after.json').write_text(json.dumps(after, indent=2) + '\n')
report = {'seconds': time.perf_counter() - started, 'tests': result.testsRun,
          'failures': len(result.failures), 'errors': len(result.errors), 'skipped': len(result.skipped),
          'inputs_unchanged': inputs == after, 'original_test_sha256': hashlib.sha256(before).hexdigest(),
          'candidate_test_sha256': hashlib.sha256(candidate).hexdigest(), 'diagnostic_ceiling_seconds': 600,
          'scope': 'Diagnostic calibration only. Live timeout remains120. Same assertion/oracle/isolation code, only a finite experimental process ceiling changed in the copied test source. No final acceptance or runtime SLO inferred.'}
(output / 'result.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
raise SystemExit(0 if result.wasSuccessful() and inputs == after else 1)
