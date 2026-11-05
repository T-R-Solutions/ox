"""Run fast fixtures, full-copy integration checks, or both (default), with timings."""
from pathlib import Path
import argparse
import json
import sys
import time
import unittest

ROOT = Path(__file__).resolve().parents[3]
# Explicit classification: unknown/new tests are fast unless decorated or their class
# is integration. Default/discovery always executes every test regardless of grouping.
INTEGRATION = frozenset({
    'test_translation_predecessor_is_authenticated',
    'test_independent_copy_and_corrupt_resource',
    'test_implementation_phase_consistency',
    'test_product_feature_isolated_from_skill_acceptance',
    'test_normative_hash_requires_review',
    'test_historical_files_remain_immutable',
    'test_relocated_contracts_remain_protected',
    'test_directory_links_stay_within_root',
    'test_specialized_frontmatter_preserves_original_content',
    'test_clean_export_and_recovery',
})


def flatten(suite):
    for test in suite:
        if isinstance(test, unittest.TestSuite):
            yield from flatten(test)
        else:
            yield test


def group(test):
    return 'integration' if (getattr(test, 'integration', False)
                            or test._testMethodName in INTEGRATION) else 'fast'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--group', choices=('fast', 'integration', 'all'), default='all')
    parser.add_argument('--timings', type=Path)
    args = parser.parse_args()
    timings = []

    class TimedResult(unittest.TextTestResult):
        def startTest(self, test):
            self.started = time.perf_counter()
            super().startTest(test)

        def stopTest(self, test):
            timings.append({'test': test.id(), 'group': group(test),
                            'seconds': time.perf_counter() - self.started})
            super().stopTest(test)

    discovered = list(flatten(unittest.defaultTestLoader.discover(str(ROOT/'tools/governance/tests'))))
    selected = [t for t in discovered if args.group == 'all' or group(t) == args.group]
    result = unittest.TextTestRunner(verbosity=2, resultclass=TimedResult).run(unittest.TestSuite(selected))
    if args.timings:
        # Never overwrite a previous observation.
        with args.timings.open('x') as output:
            json.dump({'group': args.group, 'discovered': len(discovered),
                       'executed': result.testsRun, 'failures': len(result.failures),
                       'errors': len(result.errors), 'skipped': len(result.skipped),
                       'tests': timings}, output, indent=2)
            output.write('\n')
    return int(not result.wasSuccessful())


if __name__ == '__main__':
    sys.exit(main())
