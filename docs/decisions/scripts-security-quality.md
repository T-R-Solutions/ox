# ADR — Preserve stack-relevant security and code quality

Adopted by the maintainer's explicit clarification following scripts-task-closure.

D-01: absence of adopted configuration is not evidence that a Rust/Python/security
capability is unnecessary. Reinstate compatible checks, generic report/exception
utilities, and wrappers. Replace foreign-product rules with bounded Ox rules.
This supersedes the predecessor retirement rationale for these capabilities only;
original inventory, decisions, logs and recovered bytes remain historical.
D-02: fixed named scopes security/quality and complementary checks. Full includes
baseline security/quality. No tools/data install or refresh during checks. Missing
mandatory prerequisites block; measurements are not acceptance gates. License
allowlists and risk exceptions are not invented to obtain green results.
D-03: scripts now has cross-module/wrapper/rule consumers, so explicitly include
its maintained subtree in governance copies. Keep runtime data and erase.md out;
no profile/catalog change, package generation or publication. Verify detached copy.
D-04: preserve exact authority preimages in a pinned successor before the earlier
closure normalization. Archive only observations affected by actual changed inputs;
no historical digest renewal or automatic product approval. Real missing scans are
UNVERIFIED; controlled executables validate adapter behavior only.

Rejected: deleting unconfigured security tools; restoring JVM/Tauri/foreign SQLx
policy; silently ignoring scanner failure; automatic downloads, commercial Qodana
requirements or reuse of the inherited unofficial Rust image. The official Qodana
linter matrix does not list Rust; standalone SARIF validation remains generic.
Revisit on scanner CLI/data schema, new supported stacks or licensing decisions.
