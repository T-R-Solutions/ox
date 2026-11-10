#!/usr/bin/env python3
"""Check an existing scanner report using the same parser as the automation runner."""
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from reporting import read_json
from reporting import findings


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--parser', required=True, choices=['sarif', 'opengrep', 'osv', 'gitleaks', 'yara', 'shellcheck', 'pssa', 'syft', 'grype', 'json-findings'])
    parser.add_argument('report', type=Path)
    args = parser.parse_args(argv)
    try:
        if args.report.stat().st_size > 8 * 1024 * 1024: raise ValueError('report exceeds 8 MiB')
        count = findings(args.parser, read_json(args.report))
        print(json.dumps({'state': 'findings' if count else 'passed', 'count': count}))
        return int(bool(count))
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as error:
        print(json.dumps({'state': 'error', 'reason': str(error)}))
        return 2


if __name__ == '__main__': raise SystemExit(main())
