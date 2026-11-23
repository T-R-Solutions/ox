"""Authenticate the bounded 2026-11-15 historical-link repair, never infer origins."""

import hashlib
import json
import re
from pathlib import PurePosixPath

BASE = "docs/validation/governance-link-repair-20261115"
DECISION = "docs/decisions/governance-historical-links.md"
ORIGINS = BASE + "/origins.json"
ORIGINS_SHA256 = "efc3c2288e631619efefb77caa2618b3675b2e435898f13f1eee6b571cfc8fd0"
PREVIOUS_ORIGINS = "docs/validation/log-repair-20261115/governance-origins.json"
PREVIOUS_ORIGINS_SHA256 = "115729da28c4f28de481fe5db836618ef98fb7e99f17e32be29fa1485e9c3a94"
SUCCESSORS = BASE + "/successors.json"
SUCCESSORS_SHA256 = "904ff6329d22d7a1bc8754663f0e4f1f679a46b4f9ea3b554c334015888dcdbf"
PREVIOUS_SUCCESSORS = "docs/validation/log-repair-20261115/governance-successors.json"
PREVIOUS_SUCCESSORS_SHA256 = "caeb0dd6397b93beebaf4e1964ec15ac2bd9e4d409258fb54d89583017626013"

PAIRS = {
    "docs/validation/terminal-style-20261115/before/terminal-converge.md":
        "sdd/features/terminal-progress/converge.md",
    "docs/validation/terminal-style-20261115/before/scripts-README.md": "scripts/README.md",
    "docs/validation/terminal-style-20261115/pre-final-validation/terminal-progress-converge.md":
        "sdd/features/terminal-progress/converge.md",
    "docs/validation/history-correction-20261115/coordinator/terminal-converge-before.md":
        "sdd/features/terminal-progress/converge.md",
    "docs/validation/history-correction-20261115/coordinator/scripts-readme-before.md": "scripts/README.md",
}
DESTINATIONS = frozenset({
    "sdd/features/configuration-cohesion/" + name
    for name in ("spec.md", "plan.md", "tasks.md", "traceability.json")
} | {"scripts/README.md"})


def keys(value, expected, label):
    if not isinstance(value, dict) or set(value) != set(expected):
        raise ValueError("Unexpected historical-link " + label + " schema")


def path(value):
    """Validate lexical spelling before a filesystem normalization can hide it."""
    if (not isinstance(value, str) or not value or "\\" in value
            or any(ord(char) < 32 or ord(char) == 127 for char in value)
            or PurePosixPath(value).is_absolute()
            or any(part in ("", ".", "..") for part in value.split("/"))):
        raise ValueError("Unsafe historical-link path: " + repr(value))
    return value


def digest(value):
    if not isinstance(value, str) or not re.fullmatch(r"[a-f0-9]{64}", value):
        raise ValueError("Invalid historical-link digest")


def authenticated(root, name, expected):
    from readme_revision import file

    path(name)
    data = file(root, name).read_bytes()
    if hashlib.sha256(data).hexdigest() != expected:
        raise ValueError("Historical-link registry changed: " + name)
    return data


def document(root, name, expected, revision):
    from readme_revision import file, unique

    doc = json.loads(authenticated(root, name, expected), object_pairs_hook=unique)
    keys(doc, ("schema_version", "revision", "decision", "previous_registry", "records")
         if name == ORIGINS else
         ("schema_version", "revision", "decision", "origins_sha256", "previous_registry", "records"),
         "registry")
    if (type(doc["schema_version"]) is not int or doc["schema_version"] != 1
            or doc["revision"] != revision or doc["decision"] != DECISION):
        raise ValueError("Unexpected historical-link revision")
    file(root, DECISION)
    binding = doc["previous_registry"]
    keys(binding, ("path", "sha256"), "previous registry")
    previous = PREVIOUS_ORIGINS if name == ORIGINS else PREVIOUS_SUCCESSORS
    expected_previous = PREVIOUS_ORIGINS_SHA256 if name == ORIGINS else PREVIOUS_SUCCESSORS_SHA256
    path(binding["path"])
    if binding != {"path": previous, "sha256": expected_previous}:
        raise ValueError("Historical-link previous registry binding changed")
    authenticated(root, previous, expected_previous)
    if not isinstance(doc["records"], list):
        raise ValueError("Unexpected historical-link records schema")
    return doc


def origin_records(root, previous):
    """A mandatory exact inventory; no missing-registry or old-consumer fallback."""
    from readme_revision import file

    doc = document(root, ORIGINS, ORIGINS_SHA256, "governance-historical-links-001")
    seen = set()
    old_sources = {row["source"] for row in previous}
    result = []
    for row in doc["records"]:
        keys(row, ("source", "origin", "sha256"), "origin row")
        source, origin = path(row["source"]), path(row["origin"])
        digest(row["sha256"])
        if source in seen or source in old_sources:
            raise ValueError("Duplicate/conflicting historical-link source: " + source)
        seen.add(source)
        if PAIRS.get(source) != origin:
            raise ValueError("Unexpected historical-link origin inventory")
        data = file(root, source).read_bytes()
        if hashlib.sha256(data).hexdigest() != row["sha256"]:
            raise ValueError("Historical source changed: " + source)
        file(root, origin)  # Both new origins belong to every supported consumer.
        result.append(dict(row, excluded_targets={}))
    if seen != set(PAIRS):
        raise ValueError("Unexpected historical-link origin inventory")
    return result


def successor_records(root):
    from osv_acquisition_revision import predecessor as osv_predecessor
    from readme_revision import file

    doc = document(root, SUCCESSORS, SUCCESSORS_SHA256,
                   "governance-historical-links-successors-001")
    if doc["origins_sha256"] != ORIGINS_SHA256:
        raise ValueError("Historical-link origin registry binding changed")
    authenticated(root, ORIGINS, ORIGINS_SHA256)
    seen = set()
    for row in doc["records"]:
        keys(row, ("destination", "sha256", "previous", "previous_sha256"), "successor row")
        name = path(row["destination"])
        previous = path(row["previous"])
        digest(row["sha256"])
        digest(row["previous_sha256"])
        if name in seen:
            raise ValueError("Duplicate historical-link successor destination: " + name)
        seen.add(name)
        if name not in DESTINATIONS or previous != BASE + "/before/" + name + ".bin":
            raise ValueError("Unexpected historical-link successor inventory")
        if row["sha256"] == row["previous_sha256"]:
            raise ValueError("Historical-link successor must change content")
        if hashlib.sha256(file(root, previous).read_bytes()).hexdigest() != row["previous_sha256"]:
            raise ValueError("Historical-link predecessor changed: " + name)
    if seen != DESTINATIONS:
        raise ValueError("Unexpected historical-link successor inventory")
    # Every supported consumer must expose the exact reviewed live terminals.
    # A predecessor mapping alone cannot protect paths with no older content gate.
    for row in doc["records"]:
        name = row["destination"]
        current = hashlib.sha256(osv_predecessor(root, name, file(root, name).read_bytes())).hexdigest()
        if current == row["previous_sha256"]:
            raise ValueError("Historical-link predecessor downgrade: " + name)
        if current != row["sha256"]:
            raise ValueError("Historical-link current changed (unknown content or predecessor downgrade): " + name)
    return doc["records"]


def predecessor(root, relative, data):
    """Normalize one exact reviewed successor before the immutable older chain."""
    from osv_acquisition_revision import predecessor as osv_predecessor
    from readme_revision import file

    data = osv_predecessor(root, relative, data)
    for row in successor_records(root):
        if row["destination"] != relative:
            continue
        if (file(root, relative).read_bytes() == data
                and hashlib.sha256(data).hexdigest() == row["previous_sha256"]):
            raise ValueError("Historical-link predecessor downgrade: " + relative)
        if hashlib.sha256(data).hexdigest() == row["sha256"]:
            return file(root, row["previous"]).read_bytes()
    return data


def fixture_paths(root):
    """Declare all additional inputs used by isolated succession consumers."""
    from osv_acquisition_revision import fixture_paths as osv_paths

    return [DECISION, ORIGINS, PREVIOUS_SUCCESSORS, SUCCESSORS,
            *[name for row in successor_records(root)
              for name in (row["previous"], row["destination"])], *osv_paths(root)]
