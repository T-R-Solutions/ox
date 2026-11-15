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
