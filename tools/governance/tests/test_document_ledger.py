"""Hermetic exact-document gate tests; no mutable checkout fixture inputs."""
import json
import os
import shutil
import sys
import tempfile
import unittest
from contextvars import copy_context
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import document_ledger as ledger


class DocumentLedgerTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        active = self.root / ledger.SUCCESSION_REGISTRY
        active.parent.mkdir(parents=True)
        active.write_text('{"schema_version":2,"transitions":[]}\n')
        patcher = patch.object(ledger, "DESTINATIONS", frozenset({"AGENTS.md"}))
        patcher.start()
        self.addCleanup(patcher.stop)
        authority_patcher = patch.object(ledger, "AUTHORITIES", frozenset())
        authority_patcher.start()
        self.addCleanup(authority_patcher.stop)
        self.name = "AGENTS.md"
        self.old = b"old exact contract\n"
        self.new = b"new reviewed contract\n"
        self.previous = ledger.BASE + "/predecessors/AGENTS.md.bin"
        row = dict(path=self.name, prev_sha=ledger.sha(self.old),
                   next_sha=ledger.sha(self.new), previous=self.previous,
                   task="claude-remediation-20261117")
        for name, data in ((self.name, self.new), (self.previous, self.old)):
            p = self.root / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(data)
        self.document = dict(schema_version=1, records=[row])
        self.install(self.document)

    def install(self, doc):
        data = json.dumps(doc).encode()
        (self.root / ledger.REGISTRY).write_bytes(data)
        patcher = patch.object(ledger, "REVIEWED", ledger.sha(data))
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_exact_buffer_maps_and_unknown_buffer_never_maps(self):
        self.assertEqual(ledger.predecessor(self.root, self.name, self.new), self.old)
        other = self.new + b"unknown"
        self.assertEqual(ledger.predecessor(self.root, self.name, other), other)

    def test_mutation_and_downgrade_reject_with_specific_reason(self):
        p = self.root / self.name
        for data, reason in ((self.new + b"mutation", "current changed"),
                             (self.old, "predecessor downgrade")):
            p.write_bytes(data)
            with self.subTest(reason=reason), self.assertRaisesRegex(ValueError, reason):
                ledger.predecessor(self.root, self.name, data)
        p.write_bytes(self.new)
        self.assertEqual(ledger.predecessor(self.root, self.name, self.new), self.old)

    def test_registry_rehash_cannot_hide_source_mutation(self):
        (self.root / self.name).write_bytes(b"unknown")
        doc = json.loads(json.dumps(self.document))
        doc["records"][0]["next_sha"] = ledger.sha(b"unknown")
        (self.root / ledger.REGISTRY).write_text(json.dumps(doc))
        with self.assertRaisesRegex(ValueError, "ledger changed"):
            ledger.predecessor(self.root, self.name, b"unknown")

    def test_preimage_mutation_rejected(self):
        (self.root / self.previous).write_bytes(b"unknown")
        with self.assertRaisesRegex(ValueError, "predecessor changed"):
            ledger.records(self.root)

    def test_live_and_metadata_symlinks_rejected(self):
        for name in (self.name, self.previous, ledger.REGISTRY):
            target = self.root / name
            original = target.read_bytes()
            alias = self.root / "alias"
            alias.write_bytes(original)
            target.unlink()
            target.symlink_to(alias)
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, "symlinked"):
                ledger.predecessor(self.root, self.name, self.new)
            target.unlink()
            target.write_bytes(original)

    def test_authenticated_malformed_rows_still_reject(self):
        for mode in ("duplicate", "escape", "extra", "bool", "digest", "missing"):
            doc = json.loads(json.dumps(self.document))
            if mode == "duplicate":
                doc["records"].append(doc["records"][0])
            elif mode == "escape":
                doc["records"][0]["previous"] = "../outside"
            elif mode == "extra":
                doc["records"][0]["path"] = "unreviewed.md"
            elif mode == "bool":
                doc["schema_version"] = True
            elif mode == "missing":
                doc["records"] = []
            else:
                doc["records"][0]["next_sha"] = "bad"
            self.install(doc)
            with self.subTest(mode=mode), self.assertRaisesRegex(ValueError, "Invalid document ledger"):
                ledger.records(self.root)


class InstructionAnchorTests(unittest.TestCase):
    """Authenticate an instruction terminal; synthetic reviews grant no permission."""

    install = DocumentLedgerTests.install

    def setUp(self):
        DocumentLedgerTests.setUp(self)
        import instruction_revision as instruction

        self.instruction = instruction
        self.name = "sdd/features/example/converge.md"
        self.initial = b"# Current projection\nAC-01: UNVERIFIED\n"
        self.current = self.initial + b"AC-02: UNVERIFIED\n"
        self.previous = "test/instruction-previous.bin"
        self.history = b"# Historical convergence\n"
        self.write(self.previous, self.history)
        self.write(instruction.DECISION, b"Synthetic historical decision\n")
        document = {"decision_sha256": ledger.sha((self.root / instruction.DECISION).read_bytes()),
                    "records": [{"destination": self.name, "sha256": ledger.sha(self.initial),
                                 "previous": self.previous, "previous_sha256": ledger.sha(self.history)}]}
        raw = json.dumps(document).encode()
        self.write(instruction.REGISTRY, raw)
        pin = patch.object(instruction, "REVIEWED", ledger.sha(raw))
        pin.start()
        self.addCleanup(pin.stop)
        # Isolate the new seam from unrelated historical adapters/agent profiles.
        # Real unmocked consumer/copy scenarios remain required separately.
        for target in ("visual_skill_revision.predecessor", "log_repair_revision.predecessor"):
            adapter = patch(target, side_effect=lambda _root, _name, data: data)
            adapter.start()
            self.addCleanup(adapter.stop)
        for target, value in (("log_repair_revision.original_branch", False),
                              ("instruction_revision.agent_errors", [])):
            adapter = patch(target, return_value=value)
            adapter.start()
            self.addCleanup(adapter.stop)
        self.rows = []
        self.add_version(self.initial, self.current)

    def write(self, name, data):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def add_version(self, before, after):
        version = len(self.rows) + 1
        base = f"test/version-{version}"
        decision = self.write(base + ".md", b"Synthetic transition decision\n")
        review = {"schema_version": 1, "role": "independent-review", "reviewer": "synthetic-fixture",
                  "verdict": "accepted", "path": self.name, "before_sha256": ledger.sha(before),
                  "after_sha256": ledger.sha(after), "decision_sha256": ledger.sha(decision.read_bytes()),
                  "scope": "Synthetic consistency fixture, not real authorization.", "limitations": []}
        review_path = self.write(base + ".json", json.dumps(review).encode())
        before_path = self.write(base + ".bin", before)
        self.rows.append({"path": self.name, "version": version,
                          "anchor": "instruction-governance-20261114",
                          "before": {"path": str(before_path.relative_to(self.root)), "sha256": ledger.sha(before)},
                          "after_sha256": ledger.sha(after),
                          "decision": {"path": str(decision.relative_to(self.root)), "sha256": ledger.sha(decision.read_bytes())},
                          "review": {"path": str(review_path.relative_to(self.root)), "sha256": ledger.sha(review_path.read_bytes())}})
        self.write(ledger.SUCCESSION_REGISTRY, json.dumps({"schema_version": 2, "transitions": self.rows}).encode())
        self.path = self.write(self.name, after)

    def test_initial_terminal_projects_and_both_instruction_consumers_agree(self):
        self.assertEqual(ledger.predecessor(self.root, self.name, self.current), self.initial)
        self.assertEqual(self.instruction.predecessor(self.root, self.name, self.current), self.history)
        self.assertEqual(self.instruction.errors(self.root), [])
        unknown = self.current + b"unknown supplied buffer"
        self.assertEqual(self.instruction.predecessor(self.root, self.name, unknown), unknown)

    def test_initial_anchor_is_terminal_not_older_predecessor(self):
        for wrong in (self.history, b"unregistered before"):
            self.rows = []
            self.add_version(wrong, self.current)
            with self.assertRaisesRegex(ValueError, "historical anchor mismatch"):
                ledger.succession_records(self.root)

    def test_second_version_changes_only_data_and_rejects_old_live_endpoints(self):
        protocol = Path(ledger.__file__).read_bytes()
        after = self.current + b"AC-03: UNVERIFIED\n"
        self.add_version(self.current, after)
        self.assertEqual(self.instruction.predecessor(self.root, self.name, after), self.history)
        self.assertEqual(self.instruction.errors(self.root), [])
        self.assertEqual(Path(ledger.__file__).read_bytes(), protocol)
        for old in (self.current, self.initial, self.history):
            self.path.write_bytes(old)
            for strict in (False, True):
                with self.subTest(old=old, strict=strict), self.assertRaises(ValueError):
                    ledger.predecessor(self.root, self.name, old, strict=strict)
            self.assertTrue(self.instruction.errors(self.root))

    def test_metadata_and_bindings_are_required_even_for_non_strict_callers(self):
        names = [self.instruction.REGISTRY, self.instruction.DECISION,
                 *[self.rows[0][key]["path"] for key in ("before", "decision", "review")]]
        for name in names:
            path = self.root / name
            original = path.read_bytes()
            for mode in ("changed", "missing", "symlink"):
                for strict in (False, True):
                    with self.subTest(name=name, mode=mode, strict=strict):
                        path.unlink()
                        if mode == "changed":
                            path.write_bytes(original + b"corrupt")
                        elif mode == "symlink":
                            target = self.write("test/same-bytes.bin", original)
                            path.symlink_to(target)
                        try:
                            with self.assertRaises(ValueError):
                                ledger.predecessor(self.root, self.name, self.current, strict=strict)
                        finally:
                            if path.exists() or path.is_symlink():
                                path.unlink()
                            path.write_bytes(original)

    def test_historical_preimage_is_still_checked_by_its_original_consumer(self):
        (self.root / self.previous).write_bytes(b"corrupt history")
        self.assertEqual(ledger.predecessor(self.root, self.name, self.current), self.initial)
        with self.assertRaisesRegex(ValueError, "Instruction predecessor changed"):
            self.instruction.predecessor(self.root, self.name, self.current)
        self.assertTrue(self.instruction.errors(self.root))

    def test_observation_tracks_instruction_decision_and_fixtures_include_dependencies(self):
        required = {self.instruction.REGISTRY, self.instruction.DECISION, self.previous}
        self.assertTrue(required.issubset(set(ledger.fixture_paths(self.root))))
        path = self.root / self.instruction.DECISION
        original = path.read_bytes()
        try:
            with self.assertRaises(ValueError):
                with ledger.observation(self.root):
                    self.assertEqual(ledger.predecessor(self.root, self.name, self.current), self.initial)
                    path.write_bytes(original + b"corrupt")
                    ledger.predecessor(self.root, "ordinary.md", b"ordinary", strict=False)
        finally:
            path.write_bytes(original)
        self.assertEqual(ledger.predecessor(self.root, self.name, self.current), self.initial)


class AuthorityContractTests(unittest.TestCase):
    """Real historical bindings, independent positive and adversarial inputs."""

    def setUp(self):
        source = Path(__file__).resolve().parents[3]
        temporary = tempfile.TemporaryDirectory(prefix="ox-authority-contract-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        for name in ledger.fixture_paths(source):
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((source / name).read_bytes())
        self.name = "sdd/project.md"
        self.path = self.root / self.name
        self.original = self.path.read_bytes()

    def test_authorization_append_without_registry_or_code_update(self):
        expected = ledger.predecessor(self.root, self.name, self.original)
        registry = (self.root / ledger.REGISTRY).read_bytes()
        appended = self.original + "\n## Authorized experiment — 2026-11-18\n\nIsolated verification only.\n".encode()
        self.path.write_bytes(appended)
        self.assertEqual(ledger.predecessor(self.root, self.name, appended), expected)
        self.assertEqual((self.root / ledger.REGISTRY).read_bytes(), registry)
        unknown = appended + b"unknown buffer"
        self.assertEqual(ledger.predecessor(self.root, self.name, unknown), unknown)

    def test_protected_section_removal_mutation_and_duplicate_reject(self):
        for changed in (
            self.original.replace(b"## Authorities", b"## Lost authorities", 1),
            self.original.replace(b"permanent Ox policies", b"optional Ox policies", 1),
            self.original + b"\n## Authorities\nDuplicate.\n",
            self.original + b"\n```\n## Authorized hidden heading\n",
            self.original + b"\n<!--\n## Authorized hidden heading\n",
            self.original + b"\n## Authorized probe\n\n ## Authorities\nBypass.\n",
            self.original + b"\n## Authorized probe\n\n##\tAuthorities\nBypass.\n",
            self.original + b"\n## Authorized probe\n\n## Authorities ##\nBypass.\n",
            self.original + b"\n## Authorized probe\n\nAuthorities\n---\nBypass.\n",
            self.original + b"\n## Authorized probe\n\n    ```\n## Authorities\nBypass.\n",
            self.original + b"\n## Authorized probe\n\n    <!--\n## Authorities\nBypass.\n",
        ):
            self.path.write_bytes(changed)
            with self.subTest(input=changed[-90:]), self.assertRaises(ValueError):
                ledger.predecessor(self.root, self.name, changed)

    def test_current_summary_changes_without_registry_or_code_update(self):
        expected = ledger.predecessor(self.root, self.name, self.original)
        original_summary = next(title for title in ledger.sections(self.original)
                                if title.startswith("Current summary — "))
        changed = self.original.replace(original_summary.encode(),
                                        "Current summary — 2099-01-01".encode(), 1)
        changed = changed.replace(b"Current request:", b"Current request: routine update;", 1)
        self.assertNotEqual(changed, self.original)
        self.path.write_bytes(changed)
        self.assertEqual(ledger.predecessor(self.root, self.name, changed), expected)

    def test_historical_terminal_and_downgrade_still_reject(self):
        snapshot = self.root / ledger.AUTHORITY_TERMINALS / (self.name + ".bin")
        snapshot.write_bytes(snapshot.read_bytes() + b"corrupt")
        with self.assertRaisesRegex(ValueError, "historical terminal changed"):
            ledger.predecessor(self.root, self.name, self.original)
        row = ledger.records(self.root)[self.name]
        prior = (self.root / row["previous"]).read_bytes()
        self.path.write_bytes(prior)
        with self.assertRaisesRegex(ValueError, "predecessor downgrade"):
            ledger.predecessor(self.root, self.name, prior)

    def test_non_immediate_complete_project_downgrade_rejects(self):
        source = Path(__file__).resolve().parents[3]
        for previous in ("claude-analysis-20261117", "audit-correction-20261117"):
            old = (source / "docs/validation" / previous / "before/sdd/project.md.bin").read_bytes()
            self.path.write_bytes(old)
            with self.subTest(previous=previous), self.assertRaisesRegex(ValueError, "downgrade"):
                ledger.predecessor(self.root, self.name, old)

    def test_conflicting_or_unknown_contract_version_rejects(self):
        for version in (b"3", b"invalid", b"2"):
            changed = self.original + b"\n<!-- ox:project-contract=" + version + b" -->\n"
            self.path.write_bytes(changed)
            with self.subTest(version=version), self.assertRaisesRegex(ValueError, "contract version"):
                ledger.predecessor(self.root, self.name, changed)

    def test_fenced_or_commented_heading_does_not_duplicate_real_heading(self):
        self.assertEqual(set(ledger.sections(b"# A\n## B\n```\n## B\n```\n")), {"", "B"})
        self.assertEqual(set(ledger.sections(b"# A\n## B\n<!--\n## B\n-->\n")), {"", "B"})

    def test_historical_authentication_is_unconditional_for_non_strict_callers(self):
        snapshot = self.root / ledger.AUTHORITY_TERMINALS / (self.name + ".bin")
        original = snapshot.read_bytes()
        alias = self.root / "historical-alias.bin"
        alias.write_bytes(original)
        for mode in ("corrupt", "missing", "symlink", "parent-symlink"):
            moved = None
            if mode == "parent-symlink":
                moved = self.root / "historical-parent"
                snapshot.parent.rename(moved)
                snapshot.parent.symlink_to(moved, target_is_directory=True)
            else:
                snapshot.unlink()
                if mode == "corrupt":
                    snapshot.write_bytes(original + b"corrupt")
                elif mode == "symlink":
                    snapshot.symlink_to(alias)
            try:
                for strict in (False, True):
                    for data in (self.original, self.original + b"unknown supplied buffer"):
                        with self.subTest(mode=mode, strict=strict, unknown=data != self.original):
                            with self.assertRaises(ValueError):
                                ledger.predecessor(self.root, self.name, data, strict=strict)
            finally:
                if moved is not None:
                    snapshot.parent.unlink()
                    moved.rename(snapshot.parent)
                else:
                    if snapshot.exists() or snapshot.is_symlink():
                        snapshot.unlink()
                    snapshot.write_bytes(original)

    def test_unknown_live_contract_is_returned_only_for_non_strict_callers(self):
        changed = self.original.replace(b"## Authorities", b"## Lost authorities", 1)
        self.assertNotEqual(changed, self.original)
        self.path.write_bytes(changed)
        self.assertEqual(ledger.predecessor(self.root, self.name, changed, strict=False), changed)
        with self.assertRaisesRegex(ValueError, "protected section"):
            ledger.predecessor(self.root, self.name, changed)


class VersionedSuccessionTests(unittest.TestCase):
    """Data continuity and projection, without treating declarations as permission."""

    def setUp(self):
        source = Path(__file__).resolve().parents[3]
        temp = tempfile.TemporaryDirectory(prefix="ox-versioned-succession-")
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        for name in ledger.fixture_paths(source):
            p = self.root / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes((source / name).read_bytes())
        self.registry = self.root / ledger.SUCCESSION_REGISTRY
        self.document = json.loads(self.registry.read_bytes())
        first = self.document["transitions"][0]
        self.name = first["path"]
        self.row = [row for row in self.document["transitions"]
                    if row["path"] == self.name][-1]
        self.path = self.root / self.name
        self.live = self.path.read_bytes()
        self.before = (self.root / first["before"]["path"]).read_bytes()

    def install(self, doc):
        self.registry.write_text(json.dumps(doc))

    def test_exact_projection_and_unknown_buffers(self):
        self.assertEqual(ledger.predecessor(self.root, self.name, self.live), self.before)
        unknown = self.live + b"unknown caller buffer"
        self.assertEqual(ledger.predecessor(self.root, self.name, unknown), unknown)

    def test_live_drift_and_downgrade_against_current_registry(self):
        self.path.write_bytes(self.live + b"unreviewed")
        with self.assertRaisesRegex(ValueError, "current changed"):
            ledger.predecessor(self.root, self.name, self.path.read_bytes())
        self.path.write_bytes(self.before)
        for strict in (False, True):
            with self.subTest(strict=strict), self.assertRaisesRegex(ValueError, "downgrade"):
                ledger.predecessor(self.root, self.name, self.before, strict=strict)

    def test_bound_history_review_and_decision_cannot_silently_change(self):
        for field in ("before", "review", "decision"):
            p = self.root / self.row[field]["path"]
            original = p.read_bytes()
            for strict in (False, True):
                p.write_bytes(original + b"corruption")
                with self.subTest(field=field, strict=strict), self.assertRaisesRegex(ValueError, "artifact changed"):
                    ledger.predecessor(self.root, self.name, self.live, strict=strict)
                p.write_bytes(original)

    def test_schema_paths_versions_and_review_identity_reject(self):
        for mode in ("schema", "duplicate", "gap", "escape", "wrong-anchor", "review-mismatch"):
            doc = json.loads(json.dumps(self.document))
            row = doc["transitions"][0]
            if mode == "schema":
                doc["schema_version"] = True
            elif mode == "duplicate":
                doc["transitions"].append(dict(row))
            elif mode == "gap":
                row["version"] = 2
            elif mode == "escape":
                row["before"]["path"] = "../outside"
            elif mode == "wrong-anchor":
                row["anchor"] = "unknown"
            else:
                row["after_sha256"] = "a" * 64
            self.install(doc)
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                ledger.succession_records(self.root)
        self.install(self.document)

    def transition(self, name, before, after, anchor, version):
        """A test declaration is not a real independent acceptance record."""
        base = self.root / "docs/validation/test-version"
        base.mkdir(exist_ok=True)
        snapshot = base / (str(version) + "-before.bin")
        snapshot.write_bytes(before)
        review = json.loads((self.root / self.row["review"]["path"]).read_bytes())
        review.update(path=name, before_sha256=ledger.sha(before), after_sha256=ledger.sha(after))
        review["scope"] = "Synthetic consistency fixture; no real authorization claimed."
        record = base / (str(version) + "-review.json")
        record.write_text(json.dumps(review))
        return dict(path=name, version=version, anchor=anchor,
                    before={"path": str(snapshot.relative_to(self.root)), "sha256": ledger.sha(before)},
                    after_sha256=ledger.sha(after), decision=self.row["decision"],
                    review={"path": str(record.relative_to(self.root)), "sha256": ledger.sha(record.read_bytes())})

    def test_next_version_changes_data_without_changing_python_protocol(self):
        protocol = Path(ledger.__file__).read_bytes()
        after = self.live + b"\n# Routine reviewed fixture version.\n"
        row = self.transition(self.name, self.live, after, self.row["anchor"], self.row["version"] + 1)
        self.document["transitions"].append(row)
        self.install(self.document)
        self.path.write_bytes(after)
        self.assertEqual(ledger.predecessor(self.root, self.name, after), self.before)
        self.assertEqual(Path(ledger.__file__).read_bytes(), protocol)
        self.path.write_bytes(self.live)
        with self.assertRaisesRegex(ValueError, "downgrade"):
            ledger.predecessor(self.root, self.name, self.live)

    def test_existing_historical_destination_normalizes_both_live_and_input(self):
        name = "tools/governance/scripts/governance_support.py"
        p = self.root / name
        before = p.read_bytes()
        after = before + b"\n# Synthetic reviewed fixture transition.\n"
        chain = [row for row in self.document["transitions"] if row["path"] == name]
        version = chain[-1]["version"] + 1 if chain else 1
        row = self.transition(name, before, after, "document-ledger-20261117", version)
        self.document["transitions"].append(row)
        self.install(self.document)
        p.write_bytes(after)
        historical = ledger.records(self.root)[name]
        expected = (self.root / historical["previous"]).read_bytes()
        self.assertEqual(ledger.predecessor(self.root, name, after), expected)
        unknown = after + b"unknown supplied buffer"
        self.assertEqual(ledger.predecessor(self.root, name, unknown), unknown)


    def test_observation_reuses_only_immutable_history_and_keeps_live_judgment(self):
        expected = ledger.predecessor(self.root, self.name, self.live)
        with ledger.observation(self.root):
            rows = ledger.succession_records(self.root)
            self.assertIs(rows, ledger.succession_records(self.root))
            with self.assertRaises(TypeError):
                rows[self.name][0]["version"] = 99
            self.assertEqual(ledger.predecessor(self.root, self.name, self.live), expected)
            self.path.write_bytes(self.live + b"unreviewed live input")
            with self.assertRaisesRegex(ValueError, "current changed"):
                ledger.predecessor(self.root, self.name, self.path.read_bytes())
            unknown = b"unknown supplied input"
            self.assertEqual(ledger.predecessor(self.root, self.name, unknown, strict=False), unknown)
            self.path.write_bytes(self.live)
        self.assertIsNot(rows, ledger.succession_records(self.root))

    def test_observation_rechecks_every_kind_of_bound_evidence_on_exit(self):
        from instruction_revision import REGISTRY as instruction_registry
        from log_repair_revision import REGISTRY as log_registry
        from log_repair_revision import records as log_records

        names = [ledger.REGISTRY, ledger.SUCCESSION_REGISTRY, instruction_registry, log_registry,
                 self.row["before"]["path"], self.row["decision"]["path"], self.row["review"]["path"],
                 next(iter(ledger.records(self.root).values()))["previous"],
                 log_records(self.root)[0]["previous"]]
        for name in names:
            path = self.root / name
            original = path.read_bytes()
            for mode in ("changed", "missing", "symlink"):
                with self.subTest(name=name, mode=mode):
                    try:
                        with self.assertRaises(ValueError):
                            with ledger.observation(self.root):
                                path.unlink()
                                if mode == "changed":
                                    path.write_bytes(original + b"corrupt")
                                elif mode == "symlink":
                                    target = self.root / "identical-evidence.bin"
                                    target.write_bytes(original)
                                    path.symlink_to(target)
                                # strict=False may not turn the context-exit rejection into success.
                                ledger.predecessor(self.root, "ordinary.md", b"ordinary", strict=False)
                    finally:
                        if path.exists() or path.is_symlink():
                            path.unlink()
                        path.write_bytes(original)

    def test_observation_rechecks_lexical_parent_and_same_size_restored_mtime(self):
        docs = self.root / "docs"
        actual = self.root / "actual-docs"
        try:
            with self.assertRaisesRegex(ValueError, "symlinked"):
                with ledger.observation(self.root):
                    docs.rename(actual)
                    docs.symlink_to(actual, target_is_directory=True)
        finally:
            if docs.is_symlink():
                docs.unlink()
                actual.rename(docs)
        path = self.root / self.row["before"]["path"]
        original = path.read_bytes()
        stat = path.stat()
        try:
            with self.assertRaisesRegex(ValueError, "changed during observation"):
                with ledger.observation(self.root):
                    changed = bytes([original[0] ^ 1]) + original[1:]
                    self.assertEqual(len(changed), len(original))
                    path.write_bytes(changed)
                    os.utime(path, ns=(stat.st_atime_ns, stat.st_mtime_ns))
        finally:
            path.write_bytes(original)

    def test_observation_is_discarded_after_body_exception_and_next_call_is_fresh(self):
        with self.assertRaisesRegex(RuntimeError, "body failed"):
            with ledger.observation(self.root):
                raise RuntimeError("body failed")
        path = self.root / self.row["review"]["path"]
        original = path.read_bytes()
        try:
            path.write_bytes(original + b"corruption after previous operation")
            with self.assertRaisesRegex(ValueError, "artifact changed"):
                ledger.succession_records(self.root)
            with self.assertRaisesRegex(ValueError, "artifact changed"):
                with ledger.observation(self.root):
                    self.fail("Invalid new observation must never reach its body")
        finally:
            path.write_bytes(original)
        self.assertEqual(ledger.predecessor(self.root, self.name, self.live), self.before)

    def test_nested_observation_roots_never_share_validated_inputs(self):
        other_temp = tempfile.TemporaryDirectory(prefix="ox-other-ledger-")
        self.addCleanup(other_temp.cleanup)
        other = Path(other_temp.name)
        shutil.copytree(self.root, other, dirs_exist_ok=True)
        with ledger.observation(self.root):
            outer = ledger.succession_records(self.root)
            with ledger.observation(self.root):
                self.assertIs(outer, ledger.succession_records(self.root))
            with ledger.observation(other):
                self.assertIsNot(outer, ledger.succession_records(other))
            self.assertIs(outer, ledger.succession_records(self.root))
            p = other / self.row["review"]["path"]
            p.write_bytes(p.read_bytes() + b"other root corruption")
            with self.assertRaisesRegex(ValueError, "artifact changed"):
                with ledger.observation(other):
                    self.fail("Another root cannot borrow the valid outer state")
            self.assertIs(outer, ledger.succession_records(self.root))


    def test_copied_context_cannot_reuse_state_after_owner_exit(self):
        with ledger.observation(self.root):
            copied = copy_context()
            prior = ledger.succession_records(self.root)
        self.assertIsNot(prior, copied.run(ledger.succession_records, self.root))
        path = self.root / self.row["review"]["path"]
        original = path.read_bytes()
        path.write_bytes(original + b"corrupted after owning scope ended")
        try:
            with self.assertRaisesRegex(ValueError, "artifact changed"):
                copied.run(ledger.succession_records, self.root)

            def new_observation():
                with ledger.observation(self.root):
                    self.fail("Expired copied state must not authorize a new observation")

            with self.assertRaisesRegex(ValueError, "artifact changed"):
                copied.run(new_observation)
        finally:
            path.write_bytes(original)

    def test_symlink_root_cannot_borrow_the_canonical_roots_cache(self):
        temporary = tempfile.TemporaryDirectory(prefix="ox-ledger-alias-")
        self.addCleanup(temporary.cleanup)
        alias = Path(temporary.name) / "alias"
        alias.symlink_to(self.root, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlinked"):
            ledger.succession_records(alias)
        with ledger.observation(self.root):
            with self.assertRaisesRegex(ValueError, "symlinked"):
                ledger.succession_records(alias)
            with self.assertRaisesRegex(ValueError, "symlinked"):
                with ledger.observation(alias):
                    self.fail("Lexical alias must not enter the canonical root scope")


    def test_borrowed_scope_cannot_finish_after_its_owning_observation(self):
        for body_error in (None, RuntimeError("borrower body failed")):
            with self.subTest(body_error=body_error):
                with ledger.observation(self.root):
                    copied = copy_context()
                    borrowed = ledger.observation(self.root)
                    copied.run(borrowed.__enter__)
                    self.assertEqual(copied.run(ledger.predecessor, self.root, self.name, self.live), self.before)
                path = self.root / self.row["review"]["path"]
                original = path.read_bytes()
                try:
                    path.write_bytes(original + b"corruption after owning scope ended")
                    with self.assertRaisesRegex(ValueError, "Borrowed document observation expired"):
                        copied.run(borrowed.__exit__,
                                   type(body_error) if body_error else None, body_error, None)
                finally:
                    path.write_bytes(original)
