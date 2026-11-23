"""Exact eight-path Windows design successor; preserve all earlier registries."""

import hashlib
import json
import re

REGISTRY = "docs/validation/windows-design-20261117/succession.json"
REVIEWED = "83419f852c1b7a5a554bf0292b1b19bbe5c60daae31951167a4f0a637269cae1"
DESTINATIONS = frozenset({
    "AGENTS.md", "sdd/project.md",
    ".codex/skills/design-system/SKILL.md",
    ".codex/skills/design-review/SKILL.md",
    ".codex/skills/iced-engineering/SKILL.md",
    ".codex/skills/design-system/references/visual-composition.md",
    ".codex/skills/design-review/references/visual-quality.md",
    ".codex/skills/iced-engineering/references/native-visual-contract.md",
})


def digest(data):
    return hashlib.sha256(data).hexdigest()


def records(root):
    from visual_skill_revision import _file, _unique

    raw = _file(root, REGISTRY).read_bytes()
    if digest(raw) != REVIEWED:
        raise ValueError("Windows design registry changed")
    doc = json.loads(raw, object_pairs_hook=_unique)
    if (not isinstance(doc, dict)
            or set(doc) != {"schema_version", "revision", "records"}
            or type(doc["schema_version"]) is not int or doc["schema_version"] != 1
            or doc["revision"] != "windows-design-001"
            or not isinstance(doc["records"], list)):
        raise ValueError("Unexpected Windows design registry schema")
    rows = {}
    for row in doc["records"]:
        if (not isinstance(row, dict)
                or set(row) != {"destination", "sha256", "previous_sha256", "reverse_edits"}
                or not isinstance(row["destination"], str)
                or row["destination"] not in DESTINATIONS or row["destination"] in rows
                or any(not isinstance(row[key], str)
                       or not re.fullmatch("[a-f0-9]{64}", row[key])
                       for key in ("sha256", "previous_sha256"))
                or row["sha256"] == row["previous_sha256"]
                or not isinstance(row["reverse_edits"], list) or not row["reverse_edits"]):
            raise ValueError("Unexpected Windows design successor inventory")
        last_end = -1
        for edit in row["reverse_edits"]:
            if (not isinstance(edit, dict) or set(edit) != {"start", "end", "previous_hex"}
                    or type(edit["start"]) is not int or type(edit["end"]) is not int
                    or edit["start"] <= last_end or edit["end"] < edit["start"]
                    or not isinstance(edit["previous_hex"], str)
                    or not re.fullmatch("(?:[a-f0-9]{2})*", edit["previous_hex"])):
                raise ValueError("Invalid Windows design reverse edit")
            last_end = edit["end"]
        rows[row["destination"]] = row
    if rows.keys() != DESTINATIONS:
        raise ValueError("Windows design successor scope differs")
    return rows


def predecessor(root, relative, data):
    from audit_revision import predecessor as audit_predecessor
    from visual_skill_revision import _file, _reverse

    data = audit_predecessor(root, relative, data)
    if relative not in DESTINATIONS:
        return data
    row = records(root)[relative]
    live = audit_predecessor(root, relative, _file(root, relative).read_bytes())
    if digest(live) == row["previous_sha256"]:
        raise ValueError("Windows design predecessor downgrade: " + relative)
    if digest(live) != row["sha256"] or digest(data) != row["sha256"]:
        return data
    return _reverse(data, row)


def errors(root):
    from audit_revision import errors as audit_errors
    from audit_revision import predecessor as audit_predecessor
    from visual_skill_revision import _file, _reverse

    result = audit_errors(root)
    for name, row in records(root).items():
        try:
            data = audit_predecessor(root, name, _file(root, name).read_bytes())
            if digest(data) != row["sha256"]:
                raise ValueError("Windows design current changed: " + name)
            _reverse(data, row)
        except ValueError as error:
            result.append(str(error))
    return result


def fixture_paths(root):
    from audit_revision import fixture_paths as audit_paths

    return [REGISTRY, *records(root), *audit_paths(root)]
