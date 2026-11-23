"""Bounded reviewed successors and original locations of preserved Markdown."""
import hashlib
import json
from pathlib import Path

BASE = "docs/validation/log-repair-20261115"
ORIGINS = BASE + "/governance-origins.json"
ORIGINS_SHA256 = "115729da28c4f28de481fe5db836618ef98fb7e99f17e32be29fa1485e9c3a94"


def origin_records(root):
    """Authenticate captured metadata and the complete preserved-source inventory."""
    from historical_link_revision import digest, keys, path
    from instruction_revision import governance_copy
    from readme_revision import file, unique
    registry = root / ORIGINS
    if not registry.exists() and not registry.is_symlink():
        raise ValueError("Missing historical origin registry")
    content = file(root, ORIGINS).read_bytes()
    if hashlib.sha256(content).hexdigest() != ORIGINS_SHA256:
        raise ValueError("Historical origin registry changed")
    document = json.loads(content, object_pairs_hook=unique)
    keys(document, ("schema_version", "records"), "previous origin registry")
    if type(document["schema_version"]) is not int or document["schema_version"] != 1:
        raise ValueError("Unexpected historical origin schema")
    rows = document["records"]
    if not isinstance(rows, list) or len(rows) != 16:
        raise ValueError("Unexpected historical origin inventory")
    seen = set()
    for row in rows:
        keys(row, ("source", "origin", "sha256", "excluded_targets"), "previous origin row")
        source = path(row["source"])
        path(row["origin"])
        digest(row["sha256"])
        if source in seen:
            raise ValueError("Duplicate historical source: " + source)
        seen.add(source)
        if not isinstance(row["excluded_targets"], dict):
            raise ValueError("Unexpected historical excluded targets schema")
        for target, sha256 in row["excluded_targets"].items():
            path(target)
            digest(sha256)
    copy_mode = governance_copy(root)
    for row in rows:
        data = file(root, row["source"]).read_bytes()
        if hashlib.sha256(data).hexdigest() != row["sha256"]:
            raise ValueError("Historical source changed: " + row["source"])
        if copy_mode:
            for name in row["excluded_targets"]:
                target = root / name
                if target.exists() or symlinked(root, target):
                    raise ValueError("Excluded historical target present in governance copy: " + name)
    from audit_revision import origin_records as audit_origins
    from historical_link_revision import origin_records as additional_origins

    combined = rows + additional_origins(root, rows)
    return combined + audit_origins(root, combined)


def origin(root, relative):
    """Return an authenticated original path; changed snapshots fail closed."""
    for row in origin_records(root):
        if row["source"] != relative:
            continue
        destination = Path(row["origin"])
        if destination.is_absolute() or ".." in destination.parts:
            raise ValueError("Historical origin escapes project")
        return row["origin"]
    return relative


REGISTRY = BASE + "/governance-successors.json"
REVIEWED = "caeb0dd6397b93beebaf4e1964ec15ac2bd9e4d409258fb54d89583017626013"


def records(root):
    from readme_revision import file, unique
    path = root / REGISTRY
    if not path.exists() and not path.is_symlink():
        return []
    content = file(root, REGISTRY).read_bytes()
    if hashlib.sha256(content).hexdigest() != REVIEWED:
        raise ValueError("Log repair successor registry changed")
    from instruction_revision import REGISTRY as historical_registry
    from instruction_revision import REVIEWED as historical_sha256
    if hashlib.sha256(file(root, historical_registry).read_bytes()).hexdigest() != historical_sha256:
        raise ValueError("Historical instruction registry changed")
    rows = json.loads(content, object_pairs_hook=unique)["records"]
    for row in rows:
        if hashlib.sha256(file(root, row["previous"]).read_bytes()).hexdigest() != row["previous_sha256"]:
            raise ValueError("Log repair predecessor changed: " + row["destination"])
    return rows


def predecessor(root, relative, data):
    from visual_skill_revision import predecessor as visual_predecessor
    data = visual_predecessor(root, relative, data)
    from historical_link_revision import predecessor as historical_predecessor
    from readme_revision import file
    data = historical_predecessor(root, relative, data)
    for row in records(root):
        if row["destination"] != relative:
            continue
        previous = file(root, row["previous"]).read_bytes()
        if hashlib.sha256(previous).hexdigest() != row["previous_sha256"]:
            raise ValueError("Log repair predecessor changed: " + relative)
        active = file(root, relative).read_bytes()
        if active == data and hashlib.sha256(data).hexdigest() in (row["previous_sha256"], row["replaced_sha256"]):
            raise ValueError("Log repair predecessor downgrade: " + relative)
        if hashlib.sha256(data).hexdigest() == row["sha256"]:
            return previous
    return data


def original_branch(root, relative, data):
    """Only the separately reviewed project terminal has an available-original branch."""
    from historical_link_revision import predecessor as historical_predecessor
    from windows_design_revision import predecessor as windows_predecessor
    data = windows_predecessor(root, relative, data)
    data = historical_predecessor(root, relative, data)
    return relative == "sdd/project.md" and any(
        row["destination"] == relative and row["chain_base"] == "original"
        and hashlib.sha256(data).hexdigest() == row["sha256"]
        for row in records(root)
    )


def fixture_paths(root):
    """Explicit retained inputs needed by isolated succession consumers."""
    from historical_link_revision import fixture_paths as historical_paths
    from windows_design_revision import fixture_paths as windows_paths
    return [REGISTRY, "docs/validation/visual-skills-20261116/succession.json", *[row["previous"] for row in records(root)], *historical_paths(root), *windows_paths(root)]


def excluded_reference(root, source, target):
    """Only absent exact historical/product targets in explicitly declared copies."""
    from governance_support import product_record
    from instruction_revision import governance_copy
    if not governance_copy(root) or not target.is_relative_to(root):
        return False
    if target.exists() or symlinked(root, target):
        return False
    relative = target.relative_to(root).as_posix()
    if not (relative.startswith("application/") or product_record(Path(relative))):
        return False
    return any(row["source"] == source and relative in row["excluded_targets"]
               for row in origin_records(root))


def symlinked(root, target):
    """Inspect lexical path components before resolve can hide a symlink."""
    return any(part.is_symlink() for part in (target, *target.parents) if part.is_relative_to(root))
