# New dependent-evidence review: governance-reconciliation

Only check-ox.py and test_governance.py changed among the prior bound inputs. Exact predecessor is retained in previous/. Inspected the diff: unconditional technical-state rejection is replaced by reviewed execution gates; legacy history still requires UNVERIFIED while current states use the new gate. Other profile, recovery, metadata, package and product assertions are preserved. The new helper and tests are additional observed inputs.

Profile/catalog, predecessor recovery and metadata bytes remain unchanged. The complete suite passed 42 tests (including the original integrity/mutation tests plus eight new contract tests). No speedup is claimed. The independent export manifest matches copied bytes, excludes application/, and passes SDD full/structure, check-ox, maintenance recovery and the eight focused technical tests under the source-access isolation harness. Full suite ran on the source tree, including its independent-copy tests; it was not rerun in the final export. This supports the existing scoped governance/metadata criteria without changing their definitions.

The receipt postdates the frozen export and is not claimed inside it. No commit, publication, new product behavior or sandbox effectiveness is accepted.
