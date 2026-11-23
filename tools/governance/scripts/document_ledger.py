"""Historical terminal recovery with section-bound live authority contracts.

The immutable ledger authenticates history, not the whole current authority file.
Projection is only for historical comparisons; it never refreshes SDD evidence.
"""

import hashlib
import json
import re
from contextlib import contextmanager
from contextvars import ContextVar
from pathlib import PurePosixPath
from types import MappingProxyType

BASE = "docs/validation/claude-remediation-20261117"
REGISTRY = BASE + "/document-ledger.json"
REVIEWED = "611a0a1caae00f69294c97cc061885752424bcf6a0297bff6d8b3e9b8b3eacd9"
DESTINATIONS = frozenset({
    '.codex/skills/iced-engineering/SKILL.md',
    '.codex/skills/software-delivery/SKILL.md',
    '.codex/skills/rust/references/examples.md',
    '.codex/skills/iced-engineering/references/native-visual-contract.md',
    "AGENTS.md", "sdd/workflow.md", "sdd/project.md",
    "tools/governance/scripts/governance_support.py",
    ".codex/skills/prompt/SKILL.md", "DESIGN.md", "docs/design/surfaces.md",
    "sdd/features/product-visual-workbench/converge.md", "scripts/README.md",
})

AUTHORITY_TERMINALS = "docs/validation/r3-remediation-20261118/historical-terminals"
AUTHORITIES = frozenset({"AGENTS.md", "sdd/workflow.md", "sdd/project.md"})
SUCCESSION_REGISTRY = "config/governance/succession.json"
PROJECT_CONTRACT_VERSION = b"<!-- ox:project-contract=2 -->\n"
GOVERNANCE_CLOSURE_TITLE = "Governance suite before task closure"
GOVERNANCE_CLOSURE = """In Ox, changes to AGENTS.md, SDD or skills require the complete governance suite:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools/governance/tests -v
```

Run it in addition to check-ox before declaring the affected task complete.
Record the commands, observed inputs, results, errors and any unexecuted checks.
A partial selection, skip, timeout or unavailable mandatory check does not satisfy
this requirement. This rule does not require the full scanner pipeline for other
tasks and does not authorize downloads, central maintenance, commits or publication."""

# Explicit additive normative contracts; history and existing sections stay bound.
# Decision: docs/decisions/prompt-execution-contract.md
PROMPT_CONTRACTS = {
    "AGENTS.md": (
        "Prompt-driven task entry",
        "b4d40f0201daa62d08f083f817e0199dc0d6b117268a8a83d0a8863f7342fa32",
    ),
    "sdd/workflow.md": (
        "Prompt execution contract",
        "53c64028bd18264b11c27ada5fc76c6403e2f6d0a3b36e7c53686c02f46421aa",
    ),
}


def sections(data):
    """Read actual level-two headings, rejecting ambiguity and incomplete fences."""
    text = data.decode("utf-8")
    result = {}
    title = ""
    lines = []
    fence = None
    comment = False
    for line in text.splitlines(keepends=True):
        stripped = line.lstrip(" ")
        indentation = len(line) - len(stripped)
        if not comment and fence is None and indentation <= 3 and stripped.startswith("<!--"):
            comment = "-->" not in stripped
        elif comment:
            comment = "-->" not in stripped
        elif fence is not None:
            if indentation <= 3 and re.fullmatch(re.escape(fence[0]) + "{" + str(fence[1]) + r",}\s*", stripped):
                fence = None
        else:
            marker = re.match(r" {0,3}(`{3,}|~{3,})", line)
            heading = re.match(r" {0,3}##(?:[ \t]+|$)(.*?)[ \t]*\n?$", line)
            if marker:
                if marker[1][0] == "`" and "`" in line[marker.end():]:
                    raise ValueError("Invalid authority fence info")
                fence = (marker[1][0], len(marker[1]))
            elif heading:
                if title in result:
                    raise ValueError("Duplicate authority section: " + title)
                result[title] = "".join(lines).strip()
                title = re.sub(r"[ \t]+#+[ \t]*$", "", heading[1]).strip()
                if not title:
                    raise ValueError("Empty authority section")
                lines = []
                continue
            elif re.fullmatch(r" {0,3}-+[ \t]*\n?", line) and lines and lines[-1].strip():
                raise ValueError("Noncanonical setext authority heading")
        lines.append(line)
    if fence is not None or comment:
        raise ValueError("Unterminated authority fence/comment")
    if title in result:
        raise ValueError("Duplicate authority section: " + title)
    result[title] = "".join(lines).strip()
    return result


def validate_authority(relative, live, terminal):
    """Validate protected sections before resolving a historical terminal.

    Project state/history prose is contextual, while Authorities and Features
    and methods carry the current governance contract. Historical observations
    remain authenticated in snapshots, independently of that live prose.
    """
    if relative == "sdd/project.md":
        # An explicit format version prevents historic whole documents from
        # masquerading as the new mutable-context contract. It is not permission.
        if len(re.findall(rb"<!--\s*ox:project-contract\b", live)) != 1 or not live.startswith(
                b"# Ox project context\n" + PROJECT_CONTRACT_VERSION):
            raise ValueError("Project contract version downgrade/missing")
        live = live.replace(PROJECT_CONTRACT_VERSION, b"", 1)
    expected, actual = sections(terminal), sections(live)
    protected = (set(expected) if relative != "sdd/project.md"
                 else {"", "Authorities", "Features and methods"})
    for title in protected:
        body = expected[title]
        if actual.get(title) != body:
            raise ValueError("Authority protected section changed/missing: " + relative + ": " + title)
    if relative == "sdd/project.md":
        summaries = [title for title in actual if title.startswith("Current summary — ")]
        history = "Historical project context and authorization records"
        if (len(summaries) != 1 or not actual[summaries[0]] or history not in actual
                or list(actual).index(summaries[0]) >= list(actual).index(history)):
            raise ValueError("Invalid project current/history structure")
        return terminal
    added = actual.keys() - expected.keys()
    if relative == "sdd/workflow.md":
        if actual.get(GOVERNANCE_CLOSURE_TITLE) != GOVERNANCE_CLOSURE:
            raise ValueError("Missing/changed governance closure contract")
        added = added - {GOVERNANCE_CLOSURE_TITLE}
    if relative in PROMPT_CONTRACTS:
        title, expected_digest = PROMPT_CONTRACTS[relative]
        body = actual.get(title)
        if body is None or sha(body.encode("utf-8")) != expected_digest:
            raise ValueError("Missing/changed prompt execution contract: " + relative)
        added = added - {title}
    if added:
        raise ValueError("Unknown authority section: " + relative)
    return terminal


def sha(data):
    return hashlib.sha256(data).hexdigest()



_OBSERVATION = ContextVar("document_ledger_observation", default=None)


def _immutable(value):
    if isinstance(value, dict):
        return MappingProxyType({key: _immutable(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(_immutable(item) for item in value)
    return value


class _ObservationState:
    """Immutable data plus a shared lifetime revoked by the owning scope."""

    __slots__ = ("active", "payload")

    def __init__(self, payload):
        self.active = True
        self.payload = payload

    def matches(self, root):
        return (self.active and self.payload["lexical_root"] == root.absolute()
                and self.payload["root"] == root.resolve())


def _cached(root, kind):
    current = _OBSERVATION.get()
    if current is not None and current.matches(root):
        return current.payload[kind]
    return None


def _observation_inputs(root, historical, active):
    """Every file read to validate the two cached registry results, transitively."""
    names = {REGISTRY, SUCCESSION_REGISTRY}
    names.update(row["previous"] for row in historical.values())
    rows = [row for chain in active.values() for row in chain]
    names.update(row[field]["path"] for row in rows for field in ("before", "decision", "review"))
    if any(row["anchor"] == "log-repair-20261115" for row in rows):
        from instruction_revision import REGISTRY as instruction_registry
        from log_repair_revision import REGISTRY as log_registry
        from log_repair_revision import records as log_records
        names.update((instruction_registry, log_registry))
        names.update(row["previous"] for row in log_records(root))
    if any(row["anchor"] == "instruction-governance-20261114" for row in rows):
        from instruction_revision import DECISION as instruction_decision
        from instruction_revision import REGISTRY as instruction_registry

        names.update((instruction_registry, instruction_decision))
    return names


def _observation_bytes(root, names):
    from readme_revision import file

    return {name: file(root, name).read_bytes() for name in sorted(names)}


@contextmanager
def observation(root):
    """Reuse validated history within one operation, rechecking paths and bytes.

    There is no persistent cache or cached decision about a live document. The
    caller must not publish a result until the context exits successfully. Reads
    before/after do not provide an atomic snapshot against hostile concurrent
    writers that restore a transient modification. Outside this explicit scope,
    every call keeps its original fresh validation behavior.
    """
    canonical = root.resolve()
    current = _OBSERVATION.get()
    if current is not None and current.matches(root):
        try:
            yield
        finally:
            if not current.active:
                raise ValueError("Borrowed document observation expired before exit")
        return
    # Do not expose partially validated state, including to a nested other root.
    historical = records(root)
    active = succession_records(root)
    names = _observation_inputs(root, historical, active)
    before = _observation_bytes(root, names)
    # The first validation discovers the read set; bind the validated results to
    # stable observed bytes before allowing reuse. No stat/mtime identity shortcut.
    historical = records(root)
    active = succession_records(root)
    if names != _observation_inputs(root, historical, active) or before != _observation_bytes(root, names):
        raise ValueError("Document succession inputs changed before observation")
    state = _ObservationState(MappingProxyType({
        "root": canonical, "lexical_root": root.absolute(),
        "historical": _immutable(historical), "active": _immutable(active)}))
    token = _OBSERVATION.set(state)
    try:
        yield
    finally:
        # Revoke copies retained by copy_context(), not just this context token.
        state.active = False
        _OBSERVATION.reset(token)
        # file() reopens each path and checks lexical parents/symlinks even on
        # an exception. A rejection here cannot be swallowed by strict=False.
        if before != _observation_bytes(root, names):
            raise ValueError("Document succession inputs changed during observation")


def succession_records(root):
    """Validate versioned declarations, not the identity/authority of their author.

    Historical anchors remain authenticated. New transitions require independent
    review and trusted version control; internally consistent JSON is not approval.
    """
    cached = _cached(root, "active")
    if cached is not None:
        return cached
    from readme_revision import file, unique

    def path(value):
        if (not isinstance(value, str) or not value or "\\" in value
                or PurePosixPath(value).is_absolute()
                or any(part in {"..", ".git"} for part in PurePosixPath(value).parts)
                or str(PurePosixPath(value)) != value):
            raise ValueError("Unsafe succession path")
        return value

    def digest(value):
        if not isinstance(value, str) or not re.fullmatch(r"[a-f0-9]{64}", value):
            raise ValueError("Invalid succession digest")
        return value

    def bound(binding):
        if not isinstance(binding, dict) or set(binding) != {"path", "sha256"}:
            raise ValueError("Invalid succession binding")
        data = file(root, path(binding["path"])).read_bytes()
        if sha(data) != digest(binding["sha256"]):
            raise ValueError("Succession bound artifact changed: " + binding["path"])
        return data

    doc = json.loads(file(root, SUCCESSION_REGISTRY).read_bytes(), object_pairs_hook=unique)
    if (not isinstance(doc, dict) or set(doc) != {"schema_version", "transitions"}
            or type(doc["schema_version"]) is not int or doc["schema_version"] != 2
            or not isinstance(doc["transitions"], list)):
        raise ValueError("Invalid succession registry schema")
    chains = {}
    for row in doc["transitions"]:
        if (not isinstance(row, dict) or set(row) != {
                "path", "version", "anchor", "before", "after_sha256", "decision", "review"}
                or type(row["version"]) is not int):
            raise ValueError("Invalid succession transition")
        name = path(row["path"])
        if name in AUTHORITIES:
            raise ValueError("Live authorities use section contracts, not byte successions")
        chain = chains.setdefault(name, [])
        if row["version"] != len(chain) + 1:
            raise ValueError("Succession version gap/duplicate: " + name)
        before = bound(row["before"])
        after = digest(row["after_sha256"])
        if after == sha(before) or after in {r["before"]["sha256"] for r in chain}:
            raise ValueError("Succession cycle/downgrade: " + name)
        if chain:
            if row["anchor"] != chain[0]["anchor"] or sha(before) != chain[-1]["after_sha256"]:
                raise ValueError("Broken succession continuity: " + name)
        elif row["anchor"] == "log-repair-20261115":
            from log_repair_revision import records as historical_records
            anchors = {r["destination"]: r["sha256"] for r in historical_records(root)}
            if anchors.get(name) != sha(before):
                raise ValueError("Succession historical anchor mismatch: " + name)
        elif row["anchor"] == "document-ledger-20261117":
            anchor = records(root).get(name)
            if anchor is None or anchor["next_sha"] != sha(before):
                raise ValueError("Succession historical anchor mismatch: " + name)
        elif row["anchor"] == "instruction-governance-20261114":
            # Metadata-only authentication avoids a predecessor -> ledger cycle.
            from instruction_revision import records as instruction_records

            anchors = {r["destination"]: r["sha256"] for r in instruction_records(root)}
            if anchors.get(name) != sha(before):
                raise ValueError("Succession historical anchor mismatch: " + name)
        else:
            raise ValueError("Unknown succession historical anchor")
        bound(row["decision"])
        review = json.loads(bound(row["review"]), object_pairs_hook=unique)
        if (not isinstance(review, dict) or set(review) != {
                "schema_version", "role", "reviewer", "verdict", "path",
                "before_sha256", "after_sha256", "decision_sha256", "scope", "limitations"}
                or type(review["schema_version"]) is not int or review["schema_version"] != 1
                or review["role"] != "independent-review" or review["verdict"] != "accepted"
                or not isinstance(review["reviewer"], str) or not review["reviewer"].strip()
                or review["path"] != name or review["before_sha256"] != sha(before)
                or review["after_sha256"] != after
                or review["decision_sha256"] != row["decision"]["sha256"]
                or not isinstance(review["scope"], str) or not review["scope"].strip()
                or not isinstance(review["limitations"], list)
                or any(not isinstance(value, str) for value in review["limitations"])):
            raise ValueError("Succession review binding mismatch: " + name)
        chain.append(row)
    return chains


def succession_predecessor(root, relative, data, *, strict=True):
    from readme_revision import file

    chain = succession_records(root).get(relative)
    if not chain:
        return data
    live = file(root, relative).read_bytes()
    downgrades = {row["before"]["sha256"] for row in chain}
    anchor = chain[0]["anchor"]
    if anchor == "instruction-governance-20261114":
        from instruction_revision import records as instruction_records

        downgrades.update(row["previous_sha256"] for row in instruction_records(root)
                          if row["destination"] == relative)
    elif anchor == "log-repair-20261115":
        from log_repair_revision import records as log_records

        downgrades.update(row[key] for row in log_records(root)
                          if row["destination"] == relative
                          for key in ("previous_sha256", "replaced_sha256"))
    elif anchor == "document-ledger-20261117":
        downgrades.add(records(root)[relative]["prev_sha"])
    if sha(live) in downgrades:
        raise ValueError("Succession live downgrade against current registry: " + relative)
    if sha(live) != chain[-1]["after_sha256"]:
        if strict:
            raise ValueError("Succession current changed: " + relative)
        return data
    if data == live:
        return file(root, chain[0]["before"]["path"]).read_bytes()
    return data


def records(root):
    cached = _cached(root, "historical")
    if cached is not None:
        return cached
    from readme_revision import file, unique

    raw = file(root, REGISTRY).read_bytes()
    if sha(raw) != REVIEWED:
        raise ValueError("Document ledger changed")
    doc = json.loads(raw, object_pairs_hook=unique)
    if (not isinstance(doc, dict) or set(doc) != {"schema_version", "records"}
            or type(doc["schema_version"]) is not int or doc["schema_version"] != 1
            or not isinstance(doc["records"], list)):
        raise ValueError("Invalid document ledger schema")
    rows = {}
    for row in doc["records"]:
        if (not isinstance(row, dict)
                or set(row) != {"path", "prev_sha", "next_sha", "previous", "task"}
                or not isinstance(row["path"], str)
                or row["path"] not in DESTINATIONS or row["path"] in rows
                or row["task"] != "claude-remediation-20261117"
                or row["previous"] != BASE + "/predecessors/" + row["path"] + ".bin"
                or any(not isinstance(row[k], str) or not re.fullmatch(r"[a-f0-9]{64}", row[k])
                       for k in ("prev_sha", "next_sha"))
                or row["prev_sha"] == row["next_sha"]):
            raise ValueError("Invalid document ledger row")
        if sha(file(root, row["previous"]).read_bytes()) != row["prev_sha"]:
            raise ValueError("Document ledger predecessor changed: " + row["path"])
        rows[row["path"]] = row
    if rows.keys() != DESTINATIONS:
        raise ValueError("Invalid document ledger scope")
    return rows


def predecessor(root, relative, data, *, strict=True):
    from readme_revision import file

    data = succession_predecessor(root, relative, data, strict=strict)
    if relative not in DESTINATIONS:
        return data
    row = records(root).get(relative)
    if row is None:
        return data
    live = succession_predecessor(root, relative, file(root, relative).read_bytes(), strict=strict)
    if sha(live) == row["prev_sha"]:
        raise ValueError("Document ledger predecessor downgrade: " + relative)
    if relative in AUTHORITIES:
        # Historical authentication is unconditional, including non-strict callers.
        terminal = file(root, AUTHORITY_TERMINALS + "/" + relative + ".bin").read_bytes()
        if sha(terminal) != row["next_sha"]:
            raise ValueError("Authority historical terminal changed: " + relative)
        try:
            validate_authority(relative, live, terminal)
        except ValueError:
            if strict:
                raise
            return data
        if data == live:
            data = terminal
        live = terminal
    if sha(live) != row["next_sha"]:
        if strict:
            raise ValueError("Document ledger current changed: " + relative)
        return data
    if sha(data) == row["next_sha"]:
        return file(root, row["previous"]).read_bytes()
    return data


def fixture_paths(root):
    transitions = [row for chain in succession_records(root).values() for row in chain]
    anchor_inputs = []
    if any(row["anchor"] == "log-repair-20261115" for row in transitions):
        from instruction_revision import REGISTRY as instruction_registry
        from log_repair_revision import REGISTRY as log_registry
        from log_repair_revision import records as log_records
        anchor_inputs = [instruction_registry, log_registry,
                         *[row["previous"] for row in log_records(root)]]
    if any(row["anchor"] == "instruction-governance-20261114" for row in transitions):
        from instruction_revision import DECISION as instruction_decision
        from instruction_revision import REGISTRY as instruction_registry
        from instruction_revision import records as instruction_records

        # These predecessors are validated by their existing consumers, not by
        # the metadata-only anchor. Carry them for independent consumer fixtures.
        anchor_inputs.extend((instruction_registry, instruction_decision))
        anchor_inputs.extend(row["previous"] for row in instruction_records(root))
    return [REGISTRY, SUCCESSION_REGISTRY,
            *anchor_inputs,
            *[name for row in transitions for name in (
                row["path"], row["before"]["path"], row["decision"]["path"], row["review"]["path"])],
            *[AUTHORITY_TERMINALS + "/" + name + ".bin" for name in AUTHORITIES],
            *[name for row in records(root).values()
                       for name in (row["path"], row["previous"])]]
