# ADR — governança independente, revisão 001

Estado: adotada em 2026-10-26 pelo pedido explícito de aplicar as correções v1.1.
Escopo: governança e distribuição local; não publicação ou implementação do produto.

## Decisão e consequências

Os estudos são planejamento externo, sem autoridade operacional implícita. Adota-se registro de IDs locais POL/GOV em docs/constitution.md, com cobertura em src/fixtures/normative-coverage.json. O mapeamento abaixo é histórico, não conjunto de gates. SDD 1.3.0 permanece byte a byte. Perfil revisão governance-externalization-001 conserva os mesmos 29 nomes e classes; futuras mudanças exigem nova revisão/ADR, não edição silenciosa de contagens.

Alternativas rejeitadas: repor estudos, copiar todo seu conteúdo com outro nome ou aceitar apenas estrutura. Cada uma conserva dependência ou produz aprovação insuficiente. Novo pacote precisa de execução isolada e mutações. Reabrir se houver falha, mudança de perfil, norma ou ferramenta.

AC-01 da adoção deixa de exigir originais/árvore externa; passa a verificar integridade local da biblioteca. AC-03 passa a cobrir autoridades locais. REQ-01/03 e respectivos plan/tasks são revisados. Nenhum E-* anterior é reutilizado como execução nova; previous-features.tar.gz conserva bytes anteriores. A feature original permanece no validador. Aprovações dependentes de inputs alterados são invalidadas até nova observação, inclusive as das skills. Os 36 cenários técnicos não mudam.

Backup completo anterior em /tmp/ox-before-externalization-zj4erab3/before.tar.gz (temporário, fora do pacote); restaurar somente em diretório vazio. Scripts de adoção, autoria, documentação, preparação de avaliações e auditoria da pasta-pai foram retirados; outputs históricos são observações, nunca comandos atuais. originals.json é substituído por metadados de retirada; originals.tar.gz é retirado intacto. A baseline copiada de skills/SDD permanece necessária para comparar recursos e núcleo. Outros archives são inspecionados recursivamente, sem reescrever seus hashes.

## Disposição individual dos 72 IDs históricos

O detalhamento vigente pertence às autoridades indicadas, e não ao primeiro parágrafo das regras antigas. Referências GOV/POL remetem à constituição. Os seis comportamentos GUI ficam futuros, sem aprovação funcional. EVD-002 é alterada para respeitar checklist opcional e automação opcional do SDD.

| ID anterior | Disposição | Autoridade atual | Motivo | Teste/evidência necessária |
|---|---|---|---|---|
| INT-001 | incorporada | `docs/constitution.md` (GOV-02 / POL-10) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| INT-002 | incorporada | `docs/constitution.md` (GOV-02 / POL-10) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| INT-003 | incorporada | `docs/constitution.md` (GOV-02 / POL-10) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| INT-004 | incorporada | `docs/constitution.md` (GOV-02 / POL-10) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| INT-005 | incorporada | `docs/constitution.md` (GOV-02 / POL-10) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| AGT-001 | incorporada | `AGENTS.md` (GOV-03) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| AGT-002 | incorporada | `AGENTS.md` (GOV-03) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| AGT-003 | incorporada | `AGENTS.md` (GOV-03) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| AGT-004 | incorporada | `AGENTS.md` (GOV-03) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| AGT-005 | incorporada | `AGENTS.md` (GOV-03) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| AGT-006 | incorporada | `AGENTS.md` (GOV-03) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| AGT-007 | incorporada | `AGENTS.md` (GOV-03) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| SDD-001 | incorporada | `sdd/workflow.md` (GOV-02) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| SDD-002 | incorporada | `sdd/workflow.md` (GOV-02) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| SDD-003 | incorporada | `sdd/workflow.md` (GOV-02) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| SDD-004 | incorporada | `sdd/workflow.md` (GOV-02) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| SDD-005 | incorporada | `sdd/workflow.md` (GOV-02) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| SDD-006 | incorporada | `sdd/workflow.md` (GOV-02) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| SDD-007 | incorporada | `sdd/workflow.md` (GOV-02) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| SPC-001 | incorporada | `sdd/workflow.md` (GOV-02) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| SPC-002 | incorporada | `sdd/workflow.md` (GOV-02) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| SPC-003 | incorporada | `sdd/workflow.md` (GOV-02) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| SPC-004 | incorporada | `sdd/workflow.md` (GOV-02) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| SPC-005 | incorporada | `sdd/workflow.md` (GOV-02) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| PLN-001 | incorporada | `sdd/workflow.md` (GOV-04) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| PLN-002 | incorporada | `sdd/workflow.md` (GOV-04) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| PLN-003 | incorporada | `sdd/workflow.md` (GOV-04) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| PLN-004 | incorporada | `sdd/workflow.md` (GOV-04) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| PLN-005 | incorporada | `sdd/workflow.md` (GOV-04) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| TSK-001 | incorporada | `sdd/workflow.md` (GOV-05) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| TSK-002 | incorporada | `sdd/workflow.md` (GOV-05) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| TSK-003 | incorporada | `sdd/workflow.md` (GOV-05) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| TSK-004 | incorporada | `sdd/workflow.md` (GOV-05) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| CHK-001 | incorporada | `sdd/workflow.md` (GOV-05) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| CHK-002 | incorporada | `sdd/workflow.md` (GOV-05) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| CHK-003 | incorporada | `sdd/workflow.md` (GOV-05) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| CNV-001 | incorporada | `sdd/evidence.md` (GOV-05) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| CNV-002 | incorporada | `sdd/evidence.md` (GOV-05) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| CNV-003 | incorporada | `sdd/evidence.md` (GOV-05) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| CNV-004 | incorporada | `sdd/evidence.md` (GOV-05) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| CNV-005 | incorporada | `sdd/evidence.md` (GOV-05) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| CHN-001 | incorporada | `sdd/chain/README.md` (GOV-04) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| CHN-002 | incorporada | `sdd/chain/README.md` (GOV-04) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| CHN-003 | incorporada | `sdd/chain/README.md` (GOV-04) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| CHN-004 | incorporada | `sdd/chain/README.md` (GOV-04) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| CHN-005 | incorporada | `sdd/chain/README.md` (GOV-04) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| CHN-006 | incorporada | `sdd/chain/README.md` (GOV-04) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| CHN-007 | incorporada | `sdd/chain/README.md` (GOV-04) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| AUT-001 | incorporada | `docs/constitution.md` (POL-05 / POL-06 / POL-10) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| AUT-002 | incorporada | `docs/constitution.md` (POL-05 / POL-06 / POL-10) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| AUT-003 | incorporada | `docs/constitution.md` (POL-05 / POL-06 / POL-10) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| AUT-004 | incorporada | `docs/constitution.md` (POL-05 / POL-06 / POL-10) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| AUT-005 | incorporada | `docs/constitution.md` (POL-05 / POL-06 / POL-10) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| AUT-006 | incorporada | `docs/constitution.md` (POL-05 / POL-06 / POL-10) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| EVD-001 | incorporada | `sdd/evidence.md` (GOV-05 / GOV-06) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| EVD-002 | alterada | `sdd/evidence.md` (GOV-05 / GOV-06) | Checklist e automação opcionais conforme SDD | check-ox, SDD e revisão semântica da correspondência |
| EVD-003 | incorporada | `sdd/evidence.md` (GOV-05 / GOV-06) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| EVD-004 | incorporada | `sdd/evidence.md` (GOV-05 / GOV-06) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| EVD-005 | incorporada | `sdd/evidence.md` (GOV-05 / GOV-06) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| EVD-006 | incorporada | `sdd/evidence.md` (GOV-05 / GOV-06) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| EVD-007 | incorporada | `sdd/evidence.md` (GOV-05 / GOV-06) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| EVD-008 | incorporada | `sdd/evidence.md` (GOV-05 / GOV-06) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| RET-001 | incorporada | `AGENTS.md` (GOV-03) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| RET-002 | incorporada | `AGENTS.md` (GOV-03) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| RET-003 | incorporada | `AGENTS.md` (GOV-03) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| RET-004 | incorporada | `AGENTS.md` (GOV-03) | Invariante condensada no contrato local; pesquisa deixa de ser autoridade | check-ox, SDD e revisão semântica da correspondência |
| GUI-001 | alterada | `docs/architecture/context.md` (GOV-07) | Requisito futuro, sem implementação | Feature product-* e teste real futuro |
| GUI-002 | alterada | `docs/architecture/context.md` (GOV-07) | Requisito futuro, sem implementação | Feature product-* e teste real futuro |
| GUI-003 | alterada | `docs/architecture/context.md` (GOV-07) | Requisito futuro, sem implementação | Feature product-* e teste real futuro |
| GUI-004 | alterada | `docs/architecture/context.md` (GOV-07) | Requisito futuro, sem implementação | Feature product-* e teste real futuro |
| GUI-005 | alterada | `docs/architecture/context.md` (GOV-07) | Requisito futuro, sem implementação | Feature product-* e teste real futuro |
| GUI-006 | alterada | `docs/architecture/context.md` (GOV-07) | Requisito futuro, sem implementação | Feature product-* e teste real futuro |

A incorporação integral por referência ao documento externo foi retirada. Nenhum ID histórico integra a cobertura vigente ou preserva sua aprovação antiga.
