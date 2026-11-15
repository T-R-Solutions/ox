"""Behavior of the two-date policy, raw logs and disposable working inputs."""
import concurrent.futures
import subprocess
import tempfile
import unittest
from pathlib import Path


class logs:
    @staticmethod
    def maintain(root, run=None, apply=True, day=None):
        script = Path(__file__).resolve().parents[1] / 'lib/logs.sh'
        result = subprocess.run(['/bin/bash', '-c', 'source "$1"; retain_logs "$2" "$3" "$4" "$5"',
                                 '_', str(script), str(root), str(run) if run else '',
                                 str(apply).lower(), day or '2026-11-11'], capture_output=True)
        if result.returncode:
            raise ValueError(result.stderr.decode())


class Lifecycle(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def publish(self, day, name='run'):
        run = self.root / name
        run.mkdir()
        (run / '.owner').write_text('ox-local-v2')
        (run / 'stdout.log').write_bytes(b'raw\x00failure\xff\n')
        (run / 'assessment.json').write_text('{"exit_code": 7}')
        for category in ('source', 'dataset', 'target', 'cache'):
            (run / category).mkdir()
            (run / category / 'copy.txt').write_text('not a log')
        logs.maintain(self.root, run, day=day)
        self.assertFalse(run.exists())

    def test_third_date_removes_oldest_and_only_logs_survive(self):
        for day in ('2026-11-09', '2026-11-10', '2026-11-11'):
            self.publish(day)
        base = self.root / '.local/logs'
        self.assertEqual(sorted(p.name for p in base.iterdir()), ['2026-11-10', '2026-11-11'])
        paths = list((base / '2026-11-11').iterdir())
        self.assertEqual(len(paths), 2)
        self.assertTrue(all(p.is_file() and p.suffix == '.log' for p in paths))
        self.assertEqual((base / '2026-11-11/run--stdout.log.log').read_bytes(), b'raw\x00failure\xff\n')

    def test_same_day_keeps_both_runs(self):
        self.publish('2026-11-11', 'one')
        self.publish('2026-11-11', 'two')
        self.assertEqual(len(list((self.root / '.local/logs/2026-11-11').iterdir())), 4)

    def test_symlink_root_refused(self):
        (self.root / '.local').symlink_to(self.root)
        with self.assertRaises(ValueError):
            logs.maintain(self.root)

    def test_symlink_date_refused(self):
        base = self.root / '.local/logs'
        base.mkdir(parents=True)
        (base / '2026-11-09').symlink_to(self.root)
        with self.assertRaises(ValueError):
            logs.maintain(self.root)

    def test_dry_run_then_prune(self):
        base = self.root / '.local/logs'
        for date in ('2026-11-09', '2026-11-10', '2026-11-11'):
            (base / date).mkdir(parents=True)
        logs.maintain(self.root, apply=False)
        self.assertEqual(len(list(base.iterdir())), 3)
        logs.maintain(self.root)
        self.assertEqual(len(list(base.iterdir())), 2)

    def test_clock_rollback_refused(self):
        self.publish('2026-11-10')
        self.publish('2026-11-11')
        with self.assertRaises(ValueError):
            self.publish('2026-11-09')

    def test_concurrent_publish_serializes_without_loss(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            futures = [pool.submit(self.publish, '2026-11-11', f'run-{i}') for i in range(8)]
            for future in futures:
                future.result()
        self.assertEqual(len(list((self.root / '.local/logs/2026-11-11').iterdir())), 16)
