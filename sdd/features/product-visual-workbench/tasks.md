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

## Boas-vindas e projetos — 14/11/2026

- [x] T017 — Analisar baseline/autoridades e registrar proposta, contratos, autorização e donos.
- [x] T018 — Implementar histórico limitado/concorrência/recuperação e criação exclusiva de diretório; testar invariantes e preservar preimages. Dono backend: desktop/project_store.rs.
- [x] T019 — Integrar página inicial, recentes e criação, seletor existente, teclado e preferências. Dono UI: desktop.rs/views.rs/workbench.rs e testes focados.
- [x] T020 — Exercitar Rust/jornadas gráficas e capturas comparáveis, revisão independente e correções. Raiz: harness/capturas; revisor independente: leitura.
- [x] T021 — Atualizar documentação/evidências afetadas e validar independentemente WC-01–06. Coordenador: documentação; validador: leitura/parecer independente.

T017: autoridades, histórico de persistência, fontes Desktop/Controller e baseline real
inspecionados. Nova autorização registrada em project.md e spec; decisões/limites no
plan. Referência identificada pelo usuário como IntelliJ IDEA, captura inspecionada e
hash registrado no spec. Organização inspira o fluxo; reprodução idêntica não alegada.

T018 implementado e verificado: backend std-only, testes de filesystem/concorrência
e integração Cargo passaram; revisão fonte independente não encontrou outro achado
no store/criação exclusiva. Atualizados plan/spec, application/README, surfaces e
architecture para formato limitado, recuperação e fronteira D5/D6. Evidência detalhada
em welcome-projects-20261114/backend-implementation.md e rust-observation.json.
Aceite gráfico/global não inferido. T019 permanece aberto devido ao P1 R-WC-01
(Enter em input após foco mouse podia criar pasta); correção/replay em andamento.

T019 implementado e corrigido: TrackedInput sincroniza clique/foco lógico e os
inputs nome/pai/draft consomem Enter sem efeitos;41 testes unitários,4 integrações
e1 contrato shell passaram, Clippy/build/fmt passaram. Revisão independente resolveu
R-WC-01 após fonte, regressão real de widgets e native-input-enter-fixed-pointer.
As primeiras tentativas GUI tinham clique perdido antes do binding Wayland; essa
interpretação foi corrigida explicitamente no relatório, preservando registros.
Documentação revisada/atualizada: application/README, surfaces, architecture,
project/spec/plan e report; contratos de confirmação permanecem iguais. T020/T021
continuam pendentes da jornada completa e validação independente.

T020 concluído:41 unitários+4 integrações+1 contrato, Clippy/build/fmt e geração de
tokens passaram; sessões nativas finais wide/small/recovery e replay de foco passaram
com binf2674…. Capturas comparáveis e artefatos reais inspecionados; revisor independente
sem achados pendentes. Guias/contratos/relatório atualizados com limites e contraprovas.
T021 aguarda somente gate documental final do validador independente e bindings.

T021 concluído em15/11/2026: ec_validador_alta independente aprovou WC01–06 após
inspeção dos documentos finais,208 bindings, logs/capturas/artefatos reais e checks.
Freshness/convergência passou; require-approved retorna1 somente pelos seis ACs
amplos anteriores INCONCLUSIVE. Documentos revisados/atualizados enumerados no
report; DESIGN e tokens/fontes preservados com justificativa concreta. Transcrição
final altera apenas estado/documentos de fechamento, com recheck dos hashes afetados.
Sem commits, publicação, instalações ou scanners completos.

## Identidade da página inicial — 16/11/2026

- [x] T022 — Integrar a identidade definitiva, refatorar S01 com adaptação de largura,
  preservar fluxos/IDs existentes e executar verificações Rust/nativas focadas.
  Dono: raiz, UI/assets/manifests e documentação. Critérios, comandos/inputs/resultados
  e disposição documental em welcome-identity-20261116/report.md. Não renova o aceite
  amplo WC-06 nem os estados históricos da feature.

## Reformulação desktop enterprise — 16/11/2026

- [x] T023 — Registrar escopo, critérios EV-01–04, decisão, riscos, skills e donos; preservar baseline atual.
- [x] T024 — Reformular shell/componentes e S01/S02/workbench/preferências; dono ec_implementador, fontes ox-ui e assets.
- [x] T025 — Executar Rust/capturas/jornadas focadas e revisão independente; corrigir achados afetados.
- [x] T026 — Atualizar documentação, registrar inputs/limites e validar independentemente a entrega delimitada.

T024 implementada: composição ocupando janela, seções/menus/chrome compartilhados,
ícones nativos e footer compacto. Captura preliminar encontrou header expansível;
correção e regressão de geometria passaram. Logs finais: enterprise-visual-20261116/
final-implementation-checks.json (42 unitários,4 integração,1 shell,Clippy/build0).
Documentos DESIGN/surfaces/reference-coverage/components/application README foram
atualizados para contratos efetivos. T025/T026 aguardam observação nativa final
e pareceres independentes; resultados históricos não são renovados.

T025/T026 concluídas em17/11 após final03: testes42+4+1,Clippy/build0 e ensaios
nativos estáveis em640×480,1440×900,2560×1080; abertura real sem tarefa, temas,
densidade Compacta e foco/rolagem observados. Revisão independente sem achados
pendentes e validador independente aprovou EV-01–04 delimitados. Documentação
final revisada enumerada no report; preferências exibem tema/densidade e Details
opcionais. ACs amplos continuam INCONCLUSIVE, WC UNVERIFIED; limites AT/X11,
escalas/matriz integral e replay Details permanecem explícitos. Sem commit.

## Navegação desktop — 17/11/2026

- [x] T027 — Registrar feedback, escopo DN-01–05, riscos/capacidades, donos e preservar baseline.
- [x] T028 — Implementar chrome compacto, ícones semânticos e sidebar arrastável/recolhível com teclado; dono implementador, fontes ox-ui.
- [x] T029 — Observar pointer drag/hover/rail/foco nativos, executar regressões e corrigir revisão independente.
- [x] T030 — Atualizar contratos/documentação e validar independentemente os inputs finais.

T028–T030 concluídas: chrome compacto/hoverSettings,27ícones, ausência mascote e
sidebar arrastável/rail implementados.46unit+4integration+1shell/testbuild0;Clippy
final02 precede remoção literal do rodapé272. Final03 nativo1366×768/640×480
observou dragminmax/soltura/Escape/resize/teclado/rail/foco e temas; review sem
achados, validador independente DN01–05 APPROVED delimitados. Docs revisados e
limites/corpus anômalo excluído em desktop-navigation-20261117/report.md.
Estados amplos AC/WC e históricos preservados. Sem commit.

## Correção da entrada de projetos — 17/11/2026

- [x] T031 — Ajustar engrenagem compartilhada, ordem das ações e área principal
  de projetos; dono raiz, desktop.rs/views.rs/icons.rs. Verificar foco/clique,
  layout nativo largo/estreito e regressões Rust; atualizar documentação afetada.
  Critérios PE-01–04, inputs observados, resultados e limites registrados em
  project-entry-20261117/report.md. Sem clonagem real, commit ou scanner completo.

Direção visual 2026-11-17: especificação/plano revisados para VISUAL STUDIO 2026
ENTERPRISE. Nenhuma tarefa nativa foi executada por esta sucessão documental;
critérios anteriores exigem os próprios inputs e observações.

## Continuação local: barra lateral e configurações — 2026-11-17

Dono: raiz, desktop.rs/views.rs e documentação afetada. Objetivo SS-01–03:
fixar barra/Plugins, isolar Configurações e implementar Salvar/Voltar na sessão.
Dependências: composição Iced existente e mensagens de navegação; sem efeito
persistente novo. Verificações e disposição documental no relatório
../../../docs/validation/sidebar-settings-20261117/report.md.

Concluído no escopo SS-01–03: implementação, testes focados, Clippy, build e
observação nativa em 1366×768 e 640×480. Relatório registra inputs, resultados,
limitações e documentação revisada/atualizada; não renova os gates amplos.

## Correção da auditoria — 17/11/2026

AF-T01/AF-T03: mensagem de término local em pt-BR e foco preservando papéis/estados; contratos, regressões e observação nativa em docs/validation/audit-followup-20261117/. Aceite amplo dos ACs permanece INCONCLUSIVE; fechamento delimitado depende da validação independente desse registro.

Fechamento AF-T01/AF-T03: regressões Rust e observação nativa delimitada concluídas; revisão/validação AF01–05 APPROVED no suplemento. Critérios amplos continuam INCONCLUSIVE.

## Correções da análise combinada — 2026-11-17

- T090: corrigir defeitos confirmados e atualizar evidência afetada conforme
  [relatório](../../../docs/validation/claude-remediation-20261117/report.md).
  Verificações focadas e limites constam no relatório; aceite amplo não renovado.
