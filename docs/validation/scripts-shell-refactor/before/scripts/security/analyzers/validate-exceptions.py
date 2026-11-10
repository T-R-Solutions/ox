#!/usr/bin/env python3
"""Validate normalized scoped exceptions; does not suppress scanner findings."""
import argparse
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from reporting import read_json
from reporting import exceptions


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('registry', type=Path)
    args = parser.parse_args()
    try:
        if args.registry.stat().st_size > 2 * 1024 * 1024: raise ValueError('registry exceeds 2 MiB')
        result = exceptions(read_json(args.registry))
        print(json.dumps(result)); return 0
    except (OSError, ValueError, TypeError, KeyError) as error:
        print(json.dumps({'state':'error','reason':str(error)})); return 2


if __name__ == '__main__': raise SystemExit(main())
