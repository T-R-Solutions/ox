# Quality-refinement documentary review

Scope: product-f0-gate AC-01..04 including authorized proposal adjustments. Method:
compare the maintainer's proposal/review with revised contracts, constitution,
existing ADRs and preserved predecessor; inspect each expected observation and
limitation. Byte comparisons and existing negative tests supplement semantic review.
Input identities are in inputs-final.json and the successor evidence envelope.

| Criterion | Observation and reason | Result | Limit |
|---|---|---|---|
| AC-01 | All 36 recorded scenarios match their nine feature specs, APPROVED records and checked T004 tasks. Declared inputs remain unchanged; no skill/product approval transfer. | APPROVED | Documentary consistency of inherited consumer evidence; no new consumer evaluation |
| AC-02 | Seven F0 rows retain authority, scope, method/oracle, inputs, evidence, verdict and action. Q01–Q13 specify total/changed coverage with numerator/denominator, zero-denominator handling, owned exceptions, critical paths, defect reproduction, existing-UI states/input/visual checks, measurements then budgets, actual cancellation/stale rejection, threats/denied effects and dependency review. D1–D4 retain deferrals/obligations; D5 identifies proposed ADR succession and controlled promotion. | APPROVED | Proposal completeness, not adopted gate, product coverage, numeric budgets/accessibility matrix or tooling adoption |
| AC-03 | Persistence ADR and all six feature artifacts remain byte-identical. Technology-neutral fault corpus, paired snapshot/SQLite evaluation, results-first choice and separate grants remain intact. Q12 separates future durability from current truthful claims. | APPROVED | Storage AC-01..07 remain UNVERIFIED; no experiment or technology selection |
| AC-04 | Eight predecessor files preserved with original hashes; dependency map identifies only this feature's old observation. Six changed inputs among 120 prior bindings; 85 protected inputs unchanged. Correct global checks reject stale inputs/new missing AC-04 binding. Eight existing tests cover false approval, states, mutations, missing files, borrowing and unrelated changes. | APPROVED | Declared/enumerated inputs only; no authenticity/completeness guarantee or product execution |

Semantic counterexamples: percentage without denominator/snapshot/critical paths is
insufficient under Q02/Q03; fix-only passing tests are insufficient under Q04;
baseline without adopted budgets is insufficient under Q08; API denial without
observed prohibited effects is insufficient under Q09; storage deferral cannot
waive truthful volatile-history claims under Q12. Version ranges or ADR adoption
alone cannot approve an upgrade. Screenshots cannot replace real input/backend
observation. Zed frame budgets and full WCAG conformance are not transferred.
These are contract review controls, not executed product failure injections.

Expected rules derive from the requested refinements and POL-04/05/06/10 plus
GOV-05/06, not from whichever implementation passes. F0 remains four INCONCLUSIVE
and three UNVERIFIED rows; expanded Q01–Q13 are operationally UNVERIFIED.

Initial --features calls incorrectly supplied the feature rather than its parent
directory, so they checked no feature. Their exit zero is excluded from acceptance
and retained in initial-checks.json. Correct global structure and stale-evidence
checks are recorded separately. The old envelope's seven diagnostics are expected
invalidation, not product failures or waived checks. Eight existing evidence tests
did execute; their scope is governance only.

Official Cargo CI/dependency, Zed checklist, Iced 0.14 Task and WCAG 2.2 references
were consulted in this conversation. They do not mandate the proposed monthly
cadence, 80% target or adoption. No latest-release or verified-MSRV claim is made.

This is a new semantic review of changed documentary requirements. Earlier envelope
and bytes remain under before/ with original digests. Final global freshness,
links/policy and whitespace checks are in checks-final.json. No Cargo/GUI replay,
dependency upgrade, coverage/performance measurement or product acceptance occurred.
