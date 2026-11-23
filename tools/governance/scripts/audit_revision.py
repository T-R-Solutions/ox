"""Exact audited successors and captured Markdown origins; no inferred exemptions."""

import hashlib
import json
import re
from pathlib import Path, PurePosixPath

BASE = "docs/validation/audit-correction-20261117"
REGISTRY = BASE + "/succession.json"
REVIEWED = "fc5127b589f98df748aef6caa01fc392fae8649ccb8378b4a6216a6461085709"
ORIGINS = BASE + "/succession-origins.json"
ORIGINS_REVIEWED = "6df31f101bcf69e4e42a909073d0d0e5ace852b1241f068c8c520e80e487e697"
PREVIOUS_ORIGINS = "docs/validation/governance-link-repair-20261115/origins.json"
PREVIOUS_REVIEWED = "efc3c2288e631619efefb77caa2618b3675b2e435898f13f1eee6b571cfc8fd0"
BRIDGE = BASE + "/succession-project-bridge.json"
BRIDGE_REVIEWED = "74e2ae057055b9c9196f74e657c317307f581ee9b32a8c22edd41309e4528f0e"
# The literal inventories below bind scope independently of editable JSON.
DESTINATIONS = frozenset(['.codex/skills/api-testing/references/portable-sources.md', '.codex/skills/application-security/references/portable-sources.md', '.codex/skills/commit-governance/SKILL.md', '.codex/skills/database-engineering/SKILL.md', '.codex/skills/iced-engineering/SKILL.md', '.codex/skills/performance-engineering/SKILL.md', '.codex/skills/prompt/references/portable-sources.md', '.codex/skills/reliability-engineering/references/portable-sources.md', '.codex/skills/rust/SKILL.md', '.codex/skills/rust/references/examples.md', '.codex/skills/rust/references/portable-sources.md', '.codex/skills/rust/references/sources.md', '.codex/skills/software-architecture/references/portable-sources.md', '.codex/skills/software-delivery/SKILL.md', '.codex/skills/software-evolution/SKILL.md', '.codex/skills/software-testing/SKILL.md', '.codex/skills/tool-output-engineering/references/tool-parsers-and-fallbacks.md', 'AGENTS.md', 'DESIGN.md', 'NOTICE', 'README.md', 'docs/README.md', 'docs/architecture/application.md', 'docs/decisions/scripts-toolbox-native.md', 'docs/design/components.md', 'docs/design/font-provenance.json', 'docs/design/reference-coverage.md', 'docs/design/surfaces.md', 'docs/design/windows-apps-analysis.md', 'docs/development/codex-agents.md', 'docs/development/governance.md', 'docs/development/sharing.md', 'docs/licensing/review.md', 'docs/security/trust-boundaries.md', 'scripts/README.md', 'sdd/README.md', 'sdd/chain/database-engineering.md', 'sdd/chain/software-evolution.md', 'sdd/evidence.md', 'sdd/features/README.md', 'sdd/features/product-visual-workbench/converge.md', 'sdd/features/scripts-task-closure/traceability.json', 'sdd/features/technical-acceptance/traceability.json', 'sdd/project.md', 'sdd/templates/README.md', 'sdd/workflow.md'])
PAIRS = {'docs/validation/desktop-navigation-20261117/before/DESIGN.md': 'DESIGN.md', 'docs/validation/desktop-navigation-20261117/before/application/README.md': 'application/README.md', 'docs/validation/desktop-navigation-20261117/before/application/crates/ox-ui/assets/identity/README.md': 'application/crates/ox-ui/assets/identity/README.md', 'docs/validation/desktop-navigation-20261117/before/docs/design/components.md': 'docs/design/components.md', 'docs/validation/desktop-navigation-20261117/before/docs/design/surfaces.md': 'docs/design/surfaces.md', 'docs/validation/desktop-navigation-20261117/before/sdd/features/product-visual-workbench/converge.md': 'sdd/features/product-visual-workbench/converge.md', 'docs/validation/desktop-navigation-20261117/before/sdd/features/product-visual-workbench/plan.md': 'sdd/features/product-visual-workbench/plan.md', 'docs/validation/desktop-navigation-20261117/before/sdd/features/product-visual-workbench/spec.md': 'sdd/features/product-visual-workbench/spec.md', 'docs/validation/desktop-navigation-20261117/before/sdd/features/product-visual-workbench/tasks.md': 'sdd/features/product-visual-workbench/tasks.md', 'docs/validation/desktop-navigation-20261117/before/sdd/project.md': 'sdd/project.md', 'docs/validation/enterprise-visual-20261116/before/DESIGN.md': 'DESIGN.md', 'docs/validation/enterprise-visual-20261116/before/application/README.md': 'application/README.md', 'docs/validation/enterprise-visual-20261116/before/docs/design/components.md': 'docs/design/components.md', 'docs/validation/enterprise-visual-20261116/before/docs/design/reference-coverage.md': 'docs/design/reference-coverage.md', 'docs/validation/enterprise-visual-20261116/before/docs/design/surfaces.md': 'docs/design/surfaces.md', 'docs/validation/enterprise-visual-20261116/before/sdd/features/product-visual-workbench/converge.md': 'sdd/features/product-visual-workbench/converge.md', 'docs/validation/enterprise-visual-20261116/before/sdd/features/product-visual-workbench/plan.md': 'sdd/features/product-visual-workbench/plan.md', 'docs/validation/enterprise-visual-20261116/before/sdd/features/product-visual-workbench/spec.md': 'sdd/features/product-visual-workbench/spec.md', 'docs/validation/enterprise-visual-20261116/before/sdd/features/product-visual-workbench/tasks.md': 'sdd/features/product-visual-workbench/tasks.md', 'docs/validation/enterprise-visual-20261116/before/sdd/project.md': 'sdd/project.md'}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def path(value):
    if (not isinstance(value, str) or not value or "\\" in value
            or PurePosixPath(value).is_absolute()
            or any(part in ("", ".", "..") for part in value.split("/"))
            or any(ord(char) < 32 or ord(char) == 127 for char in value)):
        raise ValueError("Unsafe audit succession path: " + repr(value))
    return value


def keys(value, expected, label):
    if not isinstance(value, dict) or set(value) != set(expected):
        raise ValueError("Unexpected audit " + label + " schema")


def digest(value):
    if not isinstance(value, str) or not re.fullmatch("[a-f0-9]{64}", value):
        raise ValueError("Invalid audit succession digest")


def authenticated(root, name, expected):
    from readme_revision import file

    path(name)
    raw = file(root, name).read_bytes()
    if sha(raw) != expected:
        raise ValueError("Audit succession content changed: " + name)
    return raw


def records(root):
    from readme_revision import unique

    doc = json.loads(authenticated(root, REGISTRY, REVIEWED), object_pairs_hook=unique)
    keys(doc, ("schema_version", "revision", "records"), "successor registry")
    if (type(doc["schema_version"]) is not int or doc["schema_version"] != 1
            or doc["revision"] != "audit-correction-20261117-001"
            or not isinstance(doc["records"], list)):
        raise ValueError("Unexpected audit successor revision")
    rows = {}
    for row in doc["records"]:
        keys(row, ("destination", "sha256", "previous", "previous_sha256"), "successor row")
        name = path(row["destination"])
        if (name not in DESTINATIONS or name in rows
                or path(row["previous"]) != BASE + "/before/" + name + ".bin"):
            raise ValueError("Unexpected audit successor inventory")
        digest(row["sha256"])
        digest(row["previous_sha256"])
        if row["sha256"] == row["previous_sha256"]:
            raise ValueError("Audit successor must change content")
        authenticated(root, row["previous"], row["previous_sha256"])
        rows[name] = row
    if rows.keys() != DESTINATIONS:
        raise ValueError("Unexpected audit successor inventory")
    return rows


def predecessor(root, relative, data):
    """One reviewed live terminal maps to its preimage; unknown data never maps."""
    from claude_analysis_revision import predecessor as correction_predecessor
    from readme_revision import file

    data = correction_predecessor(root, relative, data, strict=False)
    if relative not in DESTINATIONS:
        return data
    row = records(root)[relative]
    live = correction_predecessor(root, relative, file(root, relative).read_bytes(), strict=False)
    if sha(live) == row["previous_sha256"]:
        raise ValueError("Audit predecessor downgrade: " + relative)
    if sha(live) != row["sha256"]:
        return data  # Never normalize an unknown terminal; errors() rejects it.
    if sha(data) == row["sha256"]:
        return authenticated(root, row["previous"], row["previous_sha256"])
    return data


def errors(root):
    from claude_analysis_revision import predecessor as correction_predecessor
    from governance_support import product_record
    from instruction_revision import governance_copy
    from readme_revision import file

    result = []
    copy_mode = governance_copy(root)
    for name, row in records(root).items():
        try:
            if copy_mode and product_record(Path(name)):
                if (root / name).exists() or (root / name).is_symlink():
                    raise ValueError("Excluded product audit record present: " + name)
                continue
            live = correction_predecessor(root, name, file(root, name).read_bytes())
            if sha(live) != row["sha256"]:
                raise ValueError("Audit current changed: " + name)
            predecessor(root, name, live)
        except ValueError as error:
            result.append(str(error))
    return result


def project_bridge(root, relative, data):
    """Bridge the exact already-drifted Windows preimage to its pinned OSV terminal."""
    from readme_revision import unique

    if relative != "sdd/project.md":
        return data
    doc = json.loads(authenticated(root, BRIDGE, BRIDGE_REVIEWED), object_pairs_hook=unique)
    keys(doc, ("schema_version", "revision", "destination", "sha256", "previous", "previous_sha256"),
         "project bridge")
    if (type(doc["schema_version"]) is not int or doc["schema_version"] != 1
            or doc["revision"] != "audit-project-bridge-001"
            or doc["destination"] != "sdd/project.md"
            or doc["sha256"] != "97f5a391e32e49cf6bfa5c1b28622cb27c8ab10a3b7119520347646e2ac8cb28"
            or doc["previous_sha256"] != "7ecff339f506d569c0210a1aa5f060f970fb1c051c9bb38a934dd385093a5de8"
            or doc["previous"] != BASE + "/before/sdd/project-osv.md.bin"):
        raise ValueError("Unexpected audit project bridge")
    previous = authenticated(root, doc["previous"], doc["previous_sha256"])
    # A bridge is an intermediate normalization only. The new live terminal must
    # independently authenticate before older bytes can traverse this stage.
    from claude_analysis_revision import predecessor as correction_predecessor
    from readme_revision import file

    live = correction_predecessor(root, relative, file(root, relative).read_bytes(), strict=False)
    row = records(root)[relative]
    if sha(live) != row["sha256"]:
        return data
    return previous if sha(data) == doc["sha256"] else data


def origin_records(root, previous):
    from governance_support import product_record
    from instruction_revision import governance_copy
    from readme_revision import file, unique

    doc = json.loads(authenticated(root, ORIGINS, ORIGINS_REVIEWED), object_pairs_hook=unique)
    keys(doc, ("schema_version", "revision", "previous_registry", "records"), "origin registry")
    if (type(doc["schema_version"]) is not int or doc["schema_version"] != 1
            or doc["revision"] != "audit-origins-20261117-001"
            or doc["previous_registry"] != {"path": PREVIOUS_ORIGINS, "sha256": PREVIOUS_REVIEWED}
            or not isinstance(doc["records"], list)):
        raise ValueError("Unexpected audit origin revision")
    authenticated(root, PREVIOUS_ORIGINS, PREVIOUS_REVIEWED)
    old_sources = {row["source"] for row in previous}
    seen = set()
    copy_mode = governance_copy(root)
    for row in doc["records"]:
        keys(row, ("source", "origin", "sha256", "excluded_targets"), "origin row")
        source, origin = path(row["source"]), path(row["origin"])
        digest(row["sha256"])
        if source in seen or source in old_sources or PAIRS.get(source) != origin:
            raise ValueError("Unexpected audit origin inventory")
        seen.add(source)
        authenticated(root, source, row["sha256"])
        if not isinstance(row["excluded_targets"], dict):
            raise ValueError("Invalid audit excluded targets")
        for target, expected in row["excluded_targets"].items():
            path(target)
            digest(expected)
            if not (target.startswith("application/") or product_record(Path(target))):
                raise ValueError("Unexpected audit excluded target")
            if copy_mode:
                candidate = root / target
                if candidate.exists() or any(p.is_symlink() for p in (candidate, *candidate.parents)
                                             if p.is_relative_to(root)):
                    raise ValueError("Excluded historical target present: " + target)
        if not copy_mode or not (origin.startswith("application/") or product_record(Path(origin))):
            file(root, origin)
    if seen != set(PAIRS):
        raise ValueError("Unexpected audit origin inventory")
    return doc["records"]


def fixture_paths(root):
    """Explicit new dependencies for old isolated succession consumers."""
    from claude_analysis_revision import fixture_paths as correction_paths
    from governance_support import product_record
    from instruction_revision import governance_copy

    copy_mode = governance_copy(root)
    return [*correction_paths(root), REGISTRY, ORIGINS, PREVIOUS_ORIGINS, BRIDGE,
            BASE + "/before/sdd/project-osv.md.bin",
            *[row["previous"] for row in records(root).values()],
            *[name for name in DESTINATIONS if not (copy_mode and product_record(Path(name)))],
            *PAIRS,
            *[origin for origin in set(PAIRS.values())
              if not (copy_mode and (origin.startswith("application/") or product_record(Path(origin))))]]
