"""Age checks against real public diagnostics and rejected successor metadata."""

import datetime
import json
import tempfile
import unittest
from pathlib import Path

import support as S

ROOT = Path(__file__).resolve().parents[2]


class DatabaseAge(unittest.TestCase):
    def accepted(self, record, scanner):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "record.json"
            path.write_text(json.dumps(record))
            run = S.run(
                [
                    "bash",
                    "-c",
                    'source "${1%/*}/common.sh"; source "${1%/*}/registry.sh"; source "$1"; validate_database_metadata "$2" "$3"',
                    "age",
                    str(ROOT / "scripts/lib/backends.sh"),
                    str(path),
                    scanner,
                ],
                capture_output=True,
            )
            return run.returncode == 0

    def record(self, age):
        timestamp = (
            datetime.datetime.now(datetime.UTC) - datetime.timedelta(hours=age)
        ).isoformat()
        return {
            "database": "a" * 64,
            "database_metadata": {
                "schema": 1,
                "snapshot": "a" * 64,
                "data_timestamp": timestamp,
                "timestamp_semantics": "oldest_required_source",
                "sources": [
                    {
                        "url": "https://official.example",
                        "sha256": "b" * 64,
                        "data_timestamp": timestamp,
                        "timestamp_semantics": "native_database_updated_at",
                    }
                ]
                * 2,
            },
        }

    def test_osv_upstream_dates_do_not_expire_acquired_database(self):
        for age in (1, 26, 120, 24 * 365, -1):
            with self.subTest(age=age):
                self.assertTrue(self.accepted(self.record(age), "osv"))

    def test_trivy_age_policy_is_preserved(self):
        self.assertTrue(self.accepted(self.record(119), "trivy"))
        for age in (121, -1):
            self.assertFalse(self.accepted(self.record(age), "trivy"))

    def test_inconsistent_or_missing_provenance_is_rejected(self):
        for scanner in ("osv", "trivy"):
            record = self.record(1)
            record["database_metadata"]["snapshot"] = "b" * 64
            self.assertFalse(self.accepted(record, scanner))
            record = self.record(1)
            record["database_metadata"]["data_timestamp"] = "2000-01-01T00:00:00Z"
            self.assertFalse(self.accepted(record, scanner))
            record = self.record(1)
            del record["database_metadata"]["sources"][0]["data_timestamp"]
            self.assertFalse(self.accepted(record, scanner))
