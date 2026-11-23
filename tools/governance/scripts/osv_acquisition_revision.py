"""Authenticate exact OSV policy and closure successors; preserve old registries."""

import hashlib
import json
import re

BASE = "docs/validation/osv-acquisition-20261116"
REGISTRY = BASE + "/document-successors.json"
REVIEWED = "72103f35d7c9271ca551d2114a2e82b13adcfe7d7809af4c10306e0813c24720"
DECISION = "docs/decisions/osv-acquisition-validity.md"
DECISION_REVIEWED = "a05424cf07abfbfd754d54298a38ef8884cb64f5089aead5c8e3b354a0989e86"
DESTINATIONS = frozenset({"scripts/README.md", "sdd/project.md"})
CLOSURE_REGISTRY = BASE + "/closure-successor.json"
CLOSURE_REVIEWED = "706d551337cd81ea10523909a3aa8846bd53d1d93d5a924a855e0d1d15ae903f"
CLOSURE_DESTINATIONS = frozenset({"sdd/features/scripts-toolbox-native/converge.md"})


class CurrentContentError(ValueError):
    """Live bytes differ from a reviewed terminal; metadata integrity is separate."""


def _records(root, registry, reviewed, revision, destinations):
    from readme_revision import file, unique

    data = file(root, registry).read_bytes()
    if hashlib.sha256(data).hexdigest() != reviewed:
        raise ValueError("OSV documentary successor registry changed")
    doc = json.loads(data, object_pairs_hook=unique)
    if (not isinstance(doc, dict)
            or set(doc) != {"schema_version", "revision", "decision", "records"}
            or type(doc["schema_version"]) is not int or doc["schema_version"] != 1
            or doc["revision"] != revision
            or doc["decision"] != DECISION or not isinstance(doc["records"], list)):
        raise ValueError("Unexpected OSV documentary successor schema")
    if hashlib.sha256(file(root, DECISION).read_bytes()).hexdigest() != DECISION_REVIEWED:
        raise ValueError("OSV acquisition decision changed")
    seen = set()
    for row in doc["records"]:
        if (not isinstance(row, dict)
                or set(row) != {"destination", "sha256", "previous", "previous_sha256"}
                or not isinstance(row["destination"], str)
                or row["destination"] not in destinations
                or row["destination"] in seen
                or row["previous"] != BASE + "/before/" + row["destination"] + ".bin"
                or any(not isinstance(row[key], str)
                       or not re.fullmatch("[a-f0-9]{64}", row[key])
                       for key in ("sha256", "previous_sha256"))
                or row["sha256"] == row["previous_sha256"]):
            raise ValueError("Unexpected OSV documentary successor inventory")
        seen.add(row["destination"])
        if hashlib.sha256(file(root, row["previous"]).read_bytes()).hexdigest() != row["previous_sha256"]:
            raise ValueError("OSV documentary predecessor changed: " + row["destination"])
    if seen != destinations:
        raise ValueError("Unexpected OSV documentary successor inventory")
    return doc["records"]


def records(root):
    return [*_records(root, REGISTRY, REVIEWED, "osv-acquisition-documents-001", DESTINATIONS),
            *_records(root, CLOSURE_REGISTRY, CLOSURE_REVIEWED,
                      "osv-acquisition-closure-001", CLOSURE_DESTINATIONS)]


def predecessor(root, relative, data):
    from audit_revision import project_bridge
    from readme_revision import file
    from windows_design_revision import predecessor as windows_predecessor

    if relative not in DESTINATIONS | CLOSURE_DESTINATIONS:
        return data
    rows = records(root)
    data = windows_predecessor(root, relative, data)
    data = project_bridge(root, relative, data)
    for row in rows:
        if row["destination"] != relative:
            continue
        current = hashlib.sha256(project_bridge(root, relative,
            windows_predecessor(root, relative, file(root, relative).read_bytes()))).hexdigest()
        if current == row["previous_sha256"]:
            raise CurrentContentError("OSV documentary predecessor downgrade: " + relative)
        if current != row["sha256"]:
            raise CurrentContentError("OSV acquisition current changed (unknown content or predecessor downgrade): " + relative)
        if hashlib.sha256(data).hexdigest() == row["sha256"]:
            return file(root, row["previous"]).read_bytes()
    return data


def fixture_paths(root):
    from windows_design_revision import fixture_paths as windows_paths

    return [REGISTRY, CLOSURE_REGISTRY, DECISION,
            *[name for row in records(root) for name in (row["destination"], row["previous"])],
            *windows_paths(root)]
