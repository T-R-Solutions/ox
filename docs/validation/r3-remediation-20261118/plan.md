# Plan and decisions

## Entry and capabilities

Root triage classified material integrity/evidence/compatibility changes.
Coordinator: ec_orquestrador_alta. Observed profile spawn and messages work.
Four tree slots include root/coordinator/reviewer/validator. No close capability
is exposed; interruption is not assumed to release slots. Coordinator owns
implementation and common documents; reviewer and validator retain independent
contexts and write only their respective reports. Root owns Rust/native/opt-in
verification records under root-checks without source edits.

## Selected method

Primary software-evolution, actual entry .codex/skills/software-evolution/SKILL.md,
bridge sdd/chain/software-evolution.md version 1; entry has no semantic version.
Consulted transition-decisions.md. Contribution: characterize live/historical/copy
consumers, compare scoped replacement with retaining hash layers, define cutover
and negative tests before removing old active-input assumptions.

## Work sequence and risks

T001 preserve baseline and run the complete governance suite on independent inputs.
T002 inspect all live-document consumers and record ADR/contract decision.
T003 implement coherent succession and fixture fixes, with focused regressions.
T004 independent review, complete verification and independent validation.
T005 reconcile dispositions/documentation and append complete activity record.

RISK-01: treating mutable content as historical proof; retain historical bindings.
RISK-02: broad exemptions hide normative changes; use negative mutation oracles.
RISK-03: false copy mode; keep receipt/context conflict rejection.
RISK-04: absent tools/datasets/native environment; block required observations.
RISK-05: concurrent edits; coordinator is sole product/governance writer.

Baseline /tmp/ox-r3-baseline-20261118 contains copied observed inputs, excluding
target, __pycache__ and .git. Initial shutil copy rejected FIFO fixtures; completed
by recreating the six named pipes without reading them, then copying application.
The independent copy is execution input, not acceptance of final checkout.
Identity manifest and initial Git status are retained beside this plan.

Supporting methods: independent reviewer consulted autonomous-verification-engineering/SKILL.md for oracle separation; root executor consulted software-testing/SKILL.md for native/ignored tests. These are actual consultations, without claimed semantic versions. ADR: docs/decisions/governance-authority-contracts.md. User separately authorized OSV database refresh during execution; other central changes remain excluded.

Root also consulted workspace-integrity-engineering/SKILL.md for actual external input drift. Six application files changed outside this team; root-checks/external-input-changes.json records the observed identities without attributing authorship. Prior Cargo/native observations remain tied to their recorded inputs.

## Baseline retention and current execution

The complete baseline was moved to /tmp/ox-r3-baseline-holder-20261118/source after
the first run exposed an invalid extraction-parent environment. Subsequent complete
baseline attempts failed under filesystem quota. Following an approved host cleanup,
163 exact baseline source preimages were retained under baseline-sources and checked
against the original manifest; baseline-release.json records their identities. Only
our operational temporary snapshot was removed, not live or historical repository
content. A later copy-11 approval wait was cancelled before execution; it is distinct
from that successful cleanup. Source changes are paused during governance-final-01.
Root current-ui-* records repeat Cargo/design checks after external UI edits and
retain input comparisons. These results are not native or global task acceptance.

The completed 257-test candidate exposed an additional transitive source pin: the
readme integration oracle itself was frozen by log-repair history. The selected
design therefore uses the existing ledger module for both live authority contracts
and a single schema-2 active succession registry, with preimages/review/decision
bindings as versioned data. The historical registry remains immutable. The root
controller and independent reviewer explicitly assessed the trust-model limitation
before implementation; see the ADR and review.md. No new per-task Python adapter
or current-registry hash constant was introduced.

## Integration continuation after the first complete-run interruption

The first exact complete run ended with exit 143 without a completed suite or
runner finalization. Root reported no intentional termination; cause is unknown.
Its 1057 observed source/config inputs were unchanged. Raw partial artifacts and
results are retained in root-checks. This is not acceptance or a completed suite.
Operational streams for later runs must stay outside the distributed checkout
until completion, then be preserved; this avoids active logs changing a copied
corpus. No history is removed from distribution to hide findings.

Package/helper implementation and exact independent reviews are now integrated
through two additional records in the same active succession registry. The outer
ZIP budget changes to a finite trusted source inventory while nested payload
limits remain. The exact IDE product record boundary affects ZIP, exports and
copies, not checkout feature gates. See package-integration and the package ADR.
A fixture that assumed no existing helper transition failed correctly on a
version duplicate; the fixture now derives the next version and retains its
historical-predecessor and unknown-input oracles. The subsequent 34 focused tests
passed, including both named R3-2 regressions. Full final verification is pending.

Root owns application/crates/ox-app/tests/desktop.rs and the two native review
scripts, with proposals and actual isolated GUI attempts outside the checkout.
Coordinator additionally owns application/Cargo.toml, Cargo.lock, the local
cryoglyph vendor, application/tools/test_vendor_layout.py and its documentation.
The exact lru 0.18.5 download was separately authorized by the user; only that
archive was acquired and its checksum verified. The vendor proposal's two real
Opengrep findings led to two safe conversions and actual layout tests, without
policy suppression. Independent reviewer accepted runner 05 and its source binding;
independent validator checked observed inputs/artifact IDs. These observations do
not accept final checkout behavior or GPU runtime.

Additional actual skill consultations by the coordinator: software-delivery entry
and references/build-inputs-and-trust.md (package trust/boundary); application-security
entry and references/controls.md dependency section (observed advisory/exposure and
bounded acquisition); rust entry, references/validation-and-maintenance.md and
concurrency-and-safety.md unsafe gate (typed layout proof and offline optional-path
compatibility). All entries live under .codex/skills/<name>/SKILL.md; each selected
SDD bridge has bridge_version 1, no skill semantic version claimed.

performance-engineering/SKILL.md, bridge_version 1, and measurement-and-diagnosis.md /
changes-and-comparisons.md were consulted after a measured checker bottleneck.
Three preservation_digest(README) observations invoked the active registry 132 times
and historical ledger 180 times; the profiled 2.909 s included 1.914 s in active registry
validation. This microprofile localizes repeated work, not whole-suite throughput.
Any optimization must preserve content/path validation and independent review;
the observed historical-public ERRORs still require their own actual diagnosis.

## Retomada após calibração

Integração histórica300s, diagnósticoOSV específico e checker apósrestauração foram revisados independentemente; calibrações02/03 e preimages em historical-budget-integration. Três limpos140–142s,600s só tetoexperimental. Nova evidência nativa288,6MB altera corpus, por isso classe final real novamente.

Consulta efetiva adicional: .codex/skills/technical-documentation/SKILL.md e references/evaluation-cases.md, visual-quality.md; ponte técnica vigente bridge_version1. Contribuição: separar parsing/render/inspeção, capturar fontes finais em cópia externa e preservar renders04Nov; nunca alegar leitura humana/hostMarkdown porpreviewlocal. Ferramentas exatas docs/assets/tooling.json reconstruídas do cache por Bun --offline --ignore-scripts após aprovaçãohost; nenhuma aquisição de browser nessa etapa.

RustSec commit472a4c9a... autorizado explicitamente: geração nova18Nov/validade23Nov em cachelocal, predecessora preservada. Não há alteração daTTL/dadosantigos/Toolboxcentral. Cargo/vendor-layout integrado0; próximasexecuções não dependem de fontesRust adicionais do coordenador.

Consulta efetiva adicional: `.codex/skills/technical-documentation/references/mermaid.md`, junto da entrada já registrada (bridge_version 1), para confrontar fontes Mermaid, exportações SVG e renderização final das duas figuras corrigidas; não substitui inspeção visual nem os gates de preservação.

Independent reviewer actually consulted `.codex/skills/application-security/SKILL.md`
and `references/controls.md` (existing bridge_version 1) for the two native-driver
static-source bindings. Contribution: argv/shell, private PATH/provider, fixture
state and baseline matching boundaries; no new suppression or transitive scanner
coverage claim. The accepted two-hash delta is retained in
`static-native-binding-integration/`; real scanner execution remains separate.

## Delimitação após o preflight Clippy do catálogo

O comando obrigatório mais estrito revelou falhas reais ainda impeditivas. A raiz recebeu responsabilidade apenas por uma proposta fora do checkout para `application/crates/ox-ui/src/desktop/hint.rs`, `desktop/icons.rs`, `design.rs` e `desktop.rs`: nomes de parâmetros, decomposição local da pintura, conversões/arredondamento caracterizados e empréstimo do evento de drag. Integração depende de revisão independente e reobservação proporcional; não há autorização para redesign ou implementação geral da Parte 2.

O coordenador é responsável pela proposta isolada do grafo Cargo. A hipótese de regressão LRU foi refutada: o backend std já está selecionado. PNG 0.18.1 conserva uma dependência direta sem uso executável de miniz 0.8, enquanto seu codec usa fdeflate/flate2. A proposta preserva todos os membros publicados e remove somente essa aresta dos dois manifestos; deve demonstrar pixels, roundtrip, rejeições e integração dos assets. A suíte upstream não está integralmente disponível no pacote/cache e não será artificialmente reduzida.

Indexmap 2.13.1 é somente candidato para avaliação de compatibilidade com hashbrown 0.16. Aquisição específica ainda não autorizada neste registro; os dados exatos estão em `/tmp/ox-r3-dependency-dedup-proposal/proposal.json`. A versão anterior pode perder correções posteriores: fonte real, uso das APIs, scanners e compilação all-features devem ser examinados antes de adoção. Downgrade de flate2 foi recusado como proposta porque retiraria correções reais de streams. Nenhuma mudança de política ou allowlist é proposta.

Os pares nativos de expansão/responsividade do binário 39d517… podem sustentar critérios delimitados daquele snapshot. Mudanças de pintura/eventos que gerem novo binário exigem novas observações pertinentes; a aprovação humana permanece vinculada ao conjunto visual que o mantenedor realmente viu.

O mantenedor respondeu **“Manter sem download”** à aquisição exata de indexmap. A proposta anterior permanece histórica; nenhum pacote foi adquirido. Revisão independente concordou em preservar o impedimento hashbrown: não há resolução somente por lock/cache para as faixas incompatíveis observadas, e um fork de indexmap com backend anterior ampliaria manutenção e riscos sem provas suficientes. Não haverá nova solicitação da mesma aquisição nem exceção de Clippy. Os reparos locais UI/PNG já delimitados e as verificações integrais autorizadas continuam; o impedimento exige resultado incompleto enquanto permanecer.


## Checkpoint de interrupção solicitada — 2026-11-19

Estado **INCOMPLETO**: o usuário informou desligamento do computador em30min; a
execução foi encerrada controladamente para preservar resultados. Não é timeout
técnico nem conclusão da tarefa. Full03 foi interrompida para o desligamento informado pelo usuário: SIGINT2 recebido em2026-11-19T18:43:40.550436Z, término18:43:40.776806Z, exit130,31793.396s. Os1428inputs observados antes/depois não diferiram; supervisor/helper mantiveram SHA. A governança ficou parcial, sem resumo agregado; nenhuma fase posterior ou suíte integral foi aprovada por essa tentativa.

[Checkpoint e retomada](shutdown-checkpoint-20261119/checkpoint.md) registram os
lançadores preservados, inputs, processos e etapas pendentes. [Observações nativas
atuais](root-checks/native-ui03/report.md) continuam vinculadas aos próprios inputs.
O último gate ANTES deste checkpoint/anexação terminou1 com118estados pendentes
em19features, sem erro de bindings/freshness; freshness após append não observada.
Clippy do catálogo101/hashbrown, direitosAC05 e demais critérios pendentes não foram
dispensados. GUIconsumer final, quickskills, opt-in real final, pacote/export/demo,
discovergovernança explícito da raiz emS1 e guardasS2 continuam não executados.
O registro append-only de atividade documenta trabalho/interrupção, não aceite.
Nenhuma tarefa T003/T004/T005 é marcada concluída por este checkpoint.
