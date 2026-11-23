"""Exact focus-contract correction successor; historical observations stay unchanged."""

import hashlib
import json
import re

BASE = "docs/validation/audit-followup-20261117"
REGISTRY = BASE + "/document-successors.json"
REVIEWED = "673e3c0d73e72f9b1c06e5f3f41878d5aaa52fea9ed9309fbb172b83106ca1c9"
DESTINATIONS = frozenset({"docs/design/components.md"})


def sha(data):
    return hashlib.sha256(data).hexdigest()


def records(root):
    from readme_revision import file, unique

    raw = file(root, REGISTRY).read_bytes()
    if sha(raw) != REVIEWED:
        raise ValueError("Audit follow-up document registry changed")
    doc = json.loads(raw, object_pairs_hook=unique)
    if (not isinstance(doc, dict)
            or set(doc) != {"schema_version", "revision", "records"}
            or type(doc["schema_version"]) is not int or doc["schema_version"] != 1
            or doc["revision"] != "audit-followup-documents-001"
            or not isinstance(doc["records"], list)):
        raise ValueError("Unexpected Audit follow-up document schema")
    rows = {}
    for row in doc["records"]:
        if (not isinstance(row, dict)
                or set(row) != {"destination", "sha256", "previous", "previous_sha256"}
                or not isinstance(row["destination"], str)
                or row["destination"] not in DESTINATIONS
                or row["destination"] in rows
                or row["previous"] != BASE + "/before/" + row["destination"] + ".bin"
                or any(not isinstance(row[key], str)
                       or not re.fullmatch("[a-f0-9]{64}", row[key])
                       for key in ("sha256", "previous_sha256"))
                or row["sha256"] == row["previous_sha256"]):
            raise ValueError("Unexpected Audit follow-up document inventory")
        if sha(file(root, row["previous"]).read_bytes()) != row["previous_sha256"]:
            raise ValueError("Audit follow-up document predecessor changed")
        rows[row["destination"]] = row
    if rows.keys() != DESTINATIONS:
        raise ValueError("Audit follow-up document scope differs")
    return rows


def predecessor(root, relative, data, *, strict=True):
    """Strict callers reject drift; historical projections leave unknown bytes intact."""
    from readme_revision import file

    if relative not in DESTINATIONS:
        return data
    row = records(root)[relative]
    live = file(root, relative).read_bytes()
    if sha(live) == row["previous_sha256"]:
        raise ValueError("Audit follow-up document predecessor downgrade: " + relative)
    if sha(live) != row["sha256"]:
        if strict:
            raise ValueError("Audit follow-up document current changed: " + relative)
        return data
    if sha(data) == row["sha256"]:
        return file(root, row["previous"]).read_bytes()
    return data


def fixture_paths(root):
    return [REGISTRY, *[name for row in records(root).values()
                       for name in (row["destination"], row["previous"])]]
