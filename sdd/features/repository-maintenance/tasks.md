# Tarefas: manutenção do repositório

- [x] T001 [REQ-01, AC-01, D-01, R-01]: inventariar fontes e artefatos; remover duplicação comprovada e placeholder vazio, com recibo e verificação.
- [x] T002 [REQ-02, AC-02, D-02, R-02]: atualizar fechamento documental, templates e integração de skills; depende de T001.
- [x] T003 [REQ-03, AC-03, D-03, R-03]: centralizar destinos e migrar logs elegíveis com manifesto; depende de T002.
- [x] T004 [REQ-04, AC-04, D-04, R-04]: implementar retenção por ciclo de vida e testar limites/falhas; depende de T003.
- [x] T005 [REQ-05, AC-05, D-05, R-05]: consolidar documentação, sucessão e evidências, executar regressões e medir resultado; depende de T004.

T001/T002: disposição documental e revisão dos três exemplos em
`docs/validation/repository-maintenance-20261109/report.md`, etapas 1 e 2.

T003: migração e exceções registradas em migration.json/report.md; caminhos públicos
preservados e implementação do resolver inspecionada. Testes funcionais na T004.

T004: guia local-artifacts e report atualizados; 20 cenários de filesystem e
seis de sucessão executados, com saídas preservadas na evidência desta entrega.

T004 — revisão sucessora: 23 casos incluem FIFO em lock/recibo, erro de leitura
e proveniência no recibo. Guia local-artifacts atualizado; versões anteriores
de código, oráculo, tarefas e evidências preservadas em before-final-hardening.

T005: README.md, docs/README.md, scripts/README.md, guia local-artifacts,
workflow/templates/integração, projeto, convergência e evidências revisados.
Relatório final distingue as duas falhas documentais corrigidas, suas reexecuções,
23 testes finais do coletor, seis de sucessão e o teste opt-in não executado.
Sem mudanças de Rust/Cargo; revisão final dos metadados não altera resultados
operacionais preservados. Métodos e limites em report.md e native-summary.json.

## Sucessor de retenção — solicitação de 11/11/2026

- [x] T006 — Inventariar `.local`, remover backups e trabalhos antigos; mover caches e referências originais sem duplicação. Inventário inicial: ~45 GB, principalmente build (~37 GB) e checks (~6,1 GB). Após limpeza: ~4,1 MB de logs, antes da rotação final. Fontes alteradas preexistentes preservadas.
- [x] T007 — Substituir liberação por cópia pela retenção de duas datas; executar snapshots em temporário, publicar somente diagnósticos e descartar trabalho. Atualizar consumidores e fixtures de caminhos.
- [x] T008 — Consolidar resultados finais: 39 testes (38 aprovados, um opt-in ignorado), sete cenários de retenção; entrada real sdd-structure e diff-check com exit 0. Governança global inconclusiva por hashes históricos obsoletos, sem reaceitação. Documentos revisados/atualizados: AGENTS.md (Cargo), scripts/README.md, docs/development/local-artifacts.md, decisão repository-maintenance, project/spec/plan/tasks. README raiz e arquitetura revisados: não descrevem o layout interno alterado; sem mudança do produto. Evidências históricas não foram reaceitas.

Revisão de 13/11/2026: catálogo e políticas migrados por scripts-centralization. Evidências dependentes arquivadas e marcadas UNVERIFIED, sem renovar hashes. Revisados scripts/README.md, caminhos e contratos; resultados atuais no relatório scripts-centralization-20261113.
