# Ox SDD feature index

Features remain directly under `sdd/features/`. Each feature owns its requirements,
scope, criteria and evidence. Read its spec, plan, tasks and latest convergence
record before resuming. A directory or completed task list does not establish
acceptance. [Workflow](../workflow.md) defines the local and full routes;
[evidence.md](../evidence.md) defines the five states and content bindings.

## Ox product

| Feature | Scope and current interpretation |
| --- | --- |
| `product-foundation` | Governance transition into implementation; does not implement product engines |
| `product-bootstrap` | Virtual workspace, 16 crates and minimal Iced shell |
| `product-plugin-host` | Local Unix host, protocol negotiation, grants, failures and controlled shutdown |
| `product-agent-runtime` | Direct-child supervision, attempts, events, cancellation and deadline |
| `product-verification-engine` | Local oracle, byte snapshots, history and invalidation in memory |
| `product-local-task-ui` | Controlled task and explicit verification integrated into the desktop |
| `product-f0-gate` | Foundation gate; historical acceptance applies only to its observed inputs, with current states in evidence.json |
| `product-visual-workbench` | Desktop destinations, bounded recent-project metadata and project entry; general persistence and real agents remain separate |
| `product-local-persistence` | Proposed independent delivery after F0 and before F3/MVP; implementation awaits authorization |

F0's historical report at `docs/validation/f0-resumption-20261103/report.md`
supersedes earlier open conclusions only for the identified inputs and corpus.
It does not authorize F1 or persistence implementation. Real agents, full engines,
SDK and distribution remain future scopes. See the
`application/README.md` and
`docs/architecture/application.md` for the current implementation.

Product paths above are repository-root references. Product implementation and
operational records are excluded from the governance-only export, so this portable
index lists their names without requiring them as link targets.

## Governance and library

| Feature | Purpose |
| --- | --- |
| [adoption-governance](adoption-governance/spec.md) | Historical adoption of the library and authorities |
| [governance-externalization](governance-externalization/spec.md) | Historical removal of external-study dependencies |
| [governance-layout](governance-layout/spec.md) | Governance tools/configuration layout; application placement subsequently adopted in the bootstrap ADR |
| [maintenance-001](maintenance-001/spec.md) | Preservation, recovery and sharing |
| [governance-reconciliation](governance-reconciliation/spec.md) | Reconcile active governance with historical preservation |
| [technical-acceptance](technical-acceptance/spec.md) | Criterion and evidence semantics |
| [skill-ui-metadata-inventory](skill-ui-metadata-inventory/spec.md) | Skill metadata inventory |
| [skill-consumer-validation](skill-consumer-validation/converge.md) | Executable bounded consumers for nine specializations; independent from product acceptance |
| [readme-skill-integration](readme-skill-integration/converge.md) | README method import and governance integration; README preservation repair recorded separately |
| [technical-documentation-visuals](technical-documentation-visuals/spec.md) | Source-grounded documentation and visual authoring method |
| [scripts-task-closure](scripts-task-closure/converge.md) | Initial automation integration; retirement and automatic invocation decisions have explicit successors |
| [scripts-security-quality](scripts-security-quality/converge.md) | Retain stack-relevant security/quality capabilities, local rules and governance-copy consumers |
| [scripts-shell-refactor](scripts-shell-refactor/converge.md) | Bash entry and shared modules; Python retained only for tests within scripts/ |
| [scripts-toolchain-config](scripts-toolchain-config/converge.md) | Explicit native/toolbox configuration; Trivy/OSV/Grype toolbox ownership successor, real Docker acceptance pending |
| [scripts-security-preparation](scripts-security-preparation/converge.md) | Separate dataset acquisition/import, offline checks, rule tests and portable toolbox discovery; see current evidence for operational limits |

Additional governance features:

| Feature | Purpose |
| --- | --- |
| [configuration-cohesion](configuration-cohesion/spec.md) | Authority integration, gates, bounded documentary succession and independent acceptance |
| `dependency-hygiene` (full checkout only) | Reviewed dependencies and explicit local verification inputs |
| [history-scanner-correction](history-scanner-correction/spec.md) | Preserve scanner diagnostics and bound historical-source corrections |
| [repository-maintenance](repository-maintenance/spec.md) | Local artifact paths and the later two-date retention contract |
| [scripts-centralization](scripts-centralization/spec.md) | Declarative automation catalog, discovery and execution defaults |
| [scripts-toolbox-native](scripts-toolbox-native/spec.md) | Native Toolbox scanner contracts, datasets and consumer integration |
| [terminal-progress](terminal-progress/spec.md) | Terminal progress, publication and diagnostic projections |
| [visual-skill-refinement](visual-skill-refinement/spec.md) | Visual method refinement with independent source review |
| [windows-design-baseline](windows-design-baseline/spec.md) | VS 2026 baseline provenance and Windows guidance adaptation |

The twelve `skill-*` features cover nine engineering specializations plus consumer
validation, UI metadata and native visual methods:

| Feature | Purpose |
| --- | --- |
| [skill-agent-runtime-engineering](skill-agent-runtime-engineering/spec.md) | Runtime supervision method |
| [skill-agent-usage-accounting](skill-agent-usage-accounting/spec.md) | Usage provenance and reconciliation method |
| [skill-autonomous-verification-engineering](skill-autonomous-verification-engineering/spec.md) | Criterion and evidence gate method |
| [skill-code-context-engineering](skill-code-context-engineering/spec.md) | Snapshot-bound indexing and retrieval method |
| [skill-code-knowledge-graph-engineering](skill-code-knowledge-graph-engineering/spec.md) | Evidence-backed graph method |
| [skill-iced-engineering](skill-iced-engineering/spec.md) | Iced state, task and widget method |
| [skill-plugin-protocol-engineering](skill-plugin-protocol-engineering/spec.md) | Versioned plugin contract method |
| [skill-tool-output-engineering](skill-tool-output-engineering/spec.md) | Conservative output transformation method |
| [skill-workspace-integrity-engineering](skill-workspace-integrity-engineering/spec.md) | Workspace preservation method |
| `skill-native-visual-method` (full checkout only) | Native visual handoff and verification method |

Consumer-validation and UI-metadata entries are listed above. Their methods are
indexed in the [bridge catalog](../chain/README.md). Technical criteria and
consumer observations do not approve product modules.

Historical results retain their original bytes and scope. Changed inputs require
new observations or an explicit undecided state, not renewed historical hashes.
Do not move features to evade checks. Documentation maintenance follows the local
route when contracts and authorization remain unchanged.
