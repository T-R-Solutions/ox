# Tarefas: camada visual nativa

- [x] T001 — Inventariar referências, conciliar DESIGN.md em inglês e mapear funcionalidades. Documentar decisões e limites antes do código.
- [x] T002 — Implementar tokens, temas, densidades, componentes e navegação nativa. Revisar contratos e documentação correspondente.
- [ ] T003 — Integrar tarefa local e compor telas previstas com disponibilidade explícita. Preservar efeitos e atualizar mapa de integração.
- [ ] T004 — Executar verificações Rust, contraste e jornadas gráficas pertinentes; corrigir regressões observadas e registrar limitações.
- [ ] T005 — Atualizar guias/SDD/AGENTS, registrar inputs e evidências atuais, comparar preimages e declarar estados por critério.

Registro: T001 revisou DESIGN, inventário, matriz de candidatas e mapa de superfícies; T002 atualizou contratos de componentes, método nativo e AGENTS. T003/T004/T005 permanecem abertas onde aplicáveis: conferir converge.md e review.md para cenários sem evidência e reconciliação documental pendente. Nenhum aceite integral declarado.

- [x] T006 — Catalogar membros dos pacotes e rastrear requisitos v3/v4; registrar incorporações, duplicatas e limites.
- [x] T007 — Implementar bancada demonstrativa com arquivos, abas, inspeção e ferramentas; compor relações e papéis de agentes.
- [x] T008 — Verificar seleção/teclado, Rust e composição nativa; atualizar DESIGN, AGENTS, mapas e evidências preservando predecessores.

T006/T007: documentação atualizada em reference-coverage.md, reference-clauses.json, components.md, surfaces.md e DESIGN §17; inventário por bytes não equivale a inspeção visual individual. T008 mantém a aceitação ampla aberta; ensaios executados e condições de retomada no relatório da integração.

T008: concluída a verificação delimitada desta integração (12 testes Rust, dois ensaios Wayland, Clippy/fmt, contraste e governança). T003–T005 da entrega ampla continuam abertas; não houve aceite geral de X11/AT ou backends futuros.

## Tela inicial — 14/11/2026

- [x] T009 — Analisar DESIGN e imagens reais R4/R12; delimitar fluxo e donos no plano.
- [x] T010 — Implementar seleção de diretório e retomada real de sessão em S01, com layout adaptável e foco.
- [x] T011 — Executar testes focados e jornada nativa; revisar código e capturas em contexto independente, corrigindo achados.
- [x] T012 — Atualizar documentação/evidências afetadas e validar critérios delimitados sem renovar aceite histórico.

Registro da entrega: `docs/validation/start-screen-20261114/report.md`. T009 revisou
DESIGN, surfaces, reference-coverage, ADR visual-workbench e imagens R4/R12.

T010/T011: formulário/estado/foco implementados em desktop.rs/views.rs; 14 testes
Rust finais passaram e sessões Wayland wide/narrow observaram validação, retomada,
erro, execução/verificação, temas/densidade e foco. Revisão independente sem achados
abertos no candidato; limites e inputs no relatório. T012 concluída após revisão e validação independentes delimitadas. A documentação de project/spec/plan/surfaces/reference-coverage/application
README foi atualizada; DESIGN/arquitetura permanecem aplicáveis sem contrato novo.

T012: documentação atualizada antes do encerramento; validação ec_validador_alta
confrontou arquivos e 83 hashes finais, logs e capturas reais. SC-01–04 aprovados
no escopo documentado; AC-01–06 amplos continuam INCONCLUSIVE. Corrigido P1 de foco
do botão validar em 640×480 com detalhes, reobservado em native-narrow-final.

## Seletor de pasta — 14/11/2026

- [x] T013 — Comparar integrações e registrar contratos, riscos, critérios e donos.
- [x] T014 — Implementar diálogo assíncrono, identidade/cancelamento e testes de estado/bytes.
- [x] T015 — Exercitar diálogo real e regressão; revisar fontes e capturas independentemente.
- [x] T016 — Atualizar documentação/evidências afetadas e validar o escopo delimitado.

Registro: docs/validation/folder-picker-20261114/report.md. Critérios amplos preservados.

T013/T014: comparação e adaptador concluídos, documentação de uso/superfície atualizada.
22 testes atuais passaram; implementação e revisão fonte identificadas no relatório.
T015/T016 aguardam replay gráfico concluído pelo executor raiz. A contraprova CLI
foi corrigida; a sessão isolada exige diagnóstico de portais/startupGTK. Probe5
mostra diálogo real, mas foi terminado pelo harness e não prova confirmação/cancelamento.
Retomar com captura/foco/confirmar/cancelar, ausência de PID e artefato real; depois
reabrir revisão/validação independentes e finalizar os bindings/checker da feature.

T015 concluída: native-wide-empty e native-narrow-verified passaram sequencialmente;
diálogo GTK real, cancelar/confirmar, foco640 com detalhes, ausência do processo e
artefato real observados. Revisão independente final sem achados. Os ensaios anteriores
são históricos; os overrides GTK pertencem ao harness e não ao produto. T016 aguarda
apenas parecer documental final, com limites explícitos no relatório.

T016 concluída: FP-01–04 aprovados por validador independente no escopo delimitado;
revisão final sem achados, documentação atualizada antes do encerramento. Checker
freshness/convergência passou; aprovação ampla mantém exit1 pelos seis ACs anteriores
INCONCLUSIVE. Critérios, hashes, histórico de falhas e limites no relatório final.
