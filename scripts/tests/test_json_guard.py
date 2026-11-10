"""Independent JSON oracle for the shell lexical and duplicate-key guards."""

import json
from pathlib import Path
import tempfile
import unittest
import support as S


def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate decoded JSON key")
        result[key] = value
    return result


def finite_literal(value):
    raise ValueError("nonfinite literal: " + value)


class JsonGuard(unittest.TestCase):
    def test_decoded_duplicates_unicode_and_nonfinite_against_independent_oracle(self):
        cases = [
            '{}', '[]', 'null', 'true', 'false', '1.2e+3', '1E-2',
            '{"á":"日本 🦀"}', '{"a":[{"x":1},{"x":2}]}',
            '{"a":{"x":{},"y":[]},"b":{"x":2}}',
            '{"a":1,"a":2}', '{"\\u0061":1,"a":2}',
            '{"a":{"x":1},"a":{"y":2}}', '{"a":[],"a":{}}',
            '{"a":[{"x":1,"x":2}]}', '{"a":{"x":{},"x":1}}',
            '{} {}', 'NaN', 'nan', 'Infinity', '-Infinity', 'inf',
            '1NaN', 'nullx', 'fals', '"unfinished', '"bad\nstring"',
            json.dumps([{"value": i, "nested": [True, None, "ñ"]} for i in range(1000)]),
        ]
        with tempfile.TemporaryDirectory(prefix="Ox JSON guard ") as temporary:
            path = Path(temporary) / "input.json"
            for value in cases:
                with self.subTest(value=value[:100]):
                    try:
                        json.loads(value, object_pairs_hook=unique_keys, parse_constant=finite_literal)
                        expected = True
                    except ValueError:
                        expected = False
                    path.write_text(value)
                    try:
                        S.shell('strict_json "$1"', path)
                        observed = True
                    except ValueError:
                        observed = False
                    self.assertEqual(observed, expected)
