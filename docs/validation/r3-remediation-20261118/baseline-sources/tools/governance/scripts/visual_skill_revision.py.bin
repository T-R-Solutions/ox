"""Exact visual-skill documentary successor; reverse reviewed edits in memory only."""

import hashlib
import json
import re

REGISTRY = "docs/validation/visual-skills-20261116/succession.json"
REVIEWED = "8d758bb831971529df7af2adb580faf48d2496c172c800977797852acb1d7208"
EXISTING = frozenset({
    "tools/governance/scripts/check-ox.py",
    ".codex/skills/design-system/SKILL.md",
    ".codex/skills/design-review/SKILL.md",
    ".codex/skills/iced-engineering/SKILL.md",
    ".codex/skills/iced-engineering/references/native-visual-contract.md",
})
ADDED = frozenset({
    ".codex/skills/design-system/references/visual-composition.md",
    ".codex/skills/design-system/references/interaction-patterns.md",
    ".codex/skills/design-review/references/visual-quality.md",
})


def _sha(data):
    return hashlib.sha256(data).hexdigest()


def _file(root, relative):
    path = root / relative
    if (not path.is_file() or not path.resolve().is_relative_to(root.resolve())
            or any(p.is_symlink() for p in (path, *path.parents)
                   if p.is_relative_to(root))):
        raise ValueError("Visual skill missing/escaping/symlinked file: " + relative)
    return path


def _unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate visual skill successor property: " + key)
        result[key] = value
    return result


def records(root):
    content = _file(root, REGISTRY).read_bytes()
    if _sha(content) != REVIEWED:
        raise ValueError("Visual skill successor registry changed")
    doc = json.loads(content, object_pairs_hook=_unique)
    if (not isinstance(doc, dict)
            or set(doc) != {"schema_version", "revision", "records"}
            or type(doc["schema_version"]) is not int
            or doc["schema_version"] != 1
            or doc["revision"] != "visual-skill-refinement-001"
            or not isinstance(doc["records"], list)):
        raise ValueError("Unexpected visual skill successor schema")
    rows = {}
    for row in doc["records"]:
        if (not isinstance(row, dict)
                or set(row) != {"destination", "sha256", "previous_sha256", "reverse_edits"}
                or not isinstance(row["destination"], str)
                or row["destination"] not in EXISTING | ADDED
                or row["destination"] in rows
                or not isinstance(row["sha256"], str)
                or not re.fullmatch("[a-f0-9]{64}", row["sha256"])):
            raise ValueError("Unexpected visual skill successor inventory")
        if row["destination"] in ADDED:
            if row["previous_sha256"] is not None or row["reverse_edits"] != []:
                raise ValueError("Unexpected visual skill new-resource predecessor")
        else:
            if (not isinstance(row["previous_sha256"], str)
                    or not re.fullmatch("[a-f0-9]{64}", row["previous_sha256"])
                    or row["previous_sha256"] == row["sha256"]
                    or not isinstance(row["reverse_edits"], list)
                    or not row["reverse_edits"]):
                raise ValueError("Invalid visual skill predecessor")
            last_end = -1
            for edit in row["reverse_edits"]:
                if (not isinstance(edit, dict) or set(edit) != {"start", "end", "previous_hex"}
                        or type(edit["start"]) is not int or type(edit["end"]) is not int
                        or edit["start"] <= last_end or edit["end"] < edit["start"]
                        or not isinstance(edit["previous_hex"], str)
                        or not re.fullmatch("(?:[a-f0-9]{2})*", edit["previous_hex"])):
                    raise ValueError("Invalid visual skill reverse edit")
                last_end = edit["end"]
        rows[row["destination"]] = row
    if rows.keys() != EXISTING | ADDED:
        raise ValueError("Visual skill successor scope differs")
    return rows


def _reverse(data, row):
    result = data
    for edit in reversed(row["reverse_edits"]):
        if edit["end"] > len(data):
            raise ValueError("Visual skill reverse edit exceeds input")
        result = result[:edit["start"]] + bytes.fromhex(edit["previous_hex"]) + result[edit["end"]:]
    if _sha(result) != row["previous_sha256"]:
        raise ValueError("Visual skill reconstructed predecessor changed: " + row["destination"])
    return result


def predecessor(root, relative, data):
    from windows_design_revision import predecessor as windows_predecessor

    data = windows_predecessor(root, relative, data)
    if relative not in EXISTING:
        return data
    row = records(root)[relative]
    live = windows_predecessor(root, relative, _file(root, relative).read_bytes())
    if _sha(live) == row["previous_sha256"]:
        raise ValueError("Visual skill predecessor downgrade: " + relative)
    # A mutation never gains a path-level exemption. The live errors pass and
    # original preservation comparisons reject unknown bytes without rewriting.
    if _sha(live) != row["sha256"] or _sha(data) != row["sha256"]:
        return data
    return _reverse(data, row)


def errors(root):
    from windows_design_revision import errors as windows_errors
    from windows_design_revision import predecessor as windows_predecessor

    result = windows_errors(root)
    for relative, row in records(root).items():
        try:
            data = windows_predecessor(root, relative, _file(root, relative).read_bytes())
            if _sha(data) != row["sha256"]:
                raise ValueError("Visual skill current changed: " + relative)
            if relative in EXISTING:
                _reverse(data, row)
        except ValueError as error:
            result.append(str(error))
    return result
