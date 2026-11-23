# Tarefas

- T001: Inventariar Ec e Ox, registrar destinos e preservar alterações existentes.
- T002: Centralizar catálogo, políticas e parâmetros; migrar consumidores ativos.
- T003: Verificar seleção, rejeições e regressões; atualizar documentação e registrar limites.

Fechamento documental e resultados: docs/validation/scripts-centralization-20261113/report.md.

T001–T003 concluídas no escopo de configuração: 43 testes (um skip opt-in), cinco retestes focados, ShellCheck/Ruff/Bandit nativos e governança. Evidências operacionais históricas não foram renovadas. Documentos revisados e disposição por superfície estão no relatório.

- T004 (concluída no escopo de interface/configuração): Igualar interface e padrões do Ec, verificar planos,
  rejeições, compatibilidade e execução controlada; atualizar consumidores e
  documentação, preservando as observações anteriores.

T004: 53 testes dos scripts (um skip opt-in), 33 testes de sucessão e sete de
compatibilidade passaram. Dez testes focados cobriram CLI, ambiente, agregação e
redação Trivy. Oito ferramentas nativas aceitaram políticas e fixtures; Clippy
passou em workspace mínimo. Não foi executada a suíte completa do produto.
Fechamento documental: AGENTS.md, README.md, application/README.md,
scripts/README.md, docs/development/governance.md, sdd/project.md e os artefatos
desta feature revisados/atualizados. Constituição/arquitetura e wrapper Toolbox
revisados, sem mudança de fronteira do produto ou contrato do wrapper direto.
Relatório e limitações: docs/validation/scripts-defaults-20261113/report.md.

- T005 (estado, evidências e fechamento no relatório de reparo): Corrigir o planejamento legado sem ferramentas, revisar todos os achados dos linters e regras locais, investigar Geiger e renovar RustSec por aquisição/revisão real; executar regressões e atualizar documentação/evidências afetadas. Relatório: docs/validation/complete-repair-20261113/report.md.

- T006 (concluída no escopo AC-06/AC-07): Alinhar descoberta dos plugins Cargo e parâmetros Geiger
  ao Ec, isolar o ambiente dos testes e corrigir a portabilidade das evidências
  sem retirar a feature dos checks. Critérios AC-06/AC-07; decisões D-07/D-08.
  Preservar os registros anteriores e atualizar guia, rastreabilidade e evidências
  afetadas antes do fechamento. Registro:
  docs/validation/ec-cargo-parity-20261113/report.md.

T006: 59 testes de scripts passaram (um skip opt-in); sete verificações de
governança, incluindo as cinco falhas anteriores de distribuição, passaram.
ShellCheck, Ruff e Bandit nativos passaram sem achados. A cópia independente
validou os vínculos atuais e rejeitou fonte alterada/ausente. A primeira suíte
preservou a falha do teste antigo de prioridade; a expectativa foi sucedida pelo
contrato PATH primeiro solicitado, sem remover a cobertura. Não houve novo
`automate.sh run --scope complete` nem aceitação gráfica/do produto.

Fechamento documental T006: scripts/README.md e spec/plan/tasks/traceability/evidence
desta feature atualizados; evidências compostas anteriores de scripts-centralization
e dependency-hygiene preservadas sem renovar hashes. Constituição, arquitetura,
sdd/project.md, contrato Toolbox e política de dependências revisados, sem mudança
de produto/versões/instalação. Critérios antigos afetados continuam INCONCLUSIVE;
AC-06/AC-07 têm observações próprias. Comandos, entradas, falhas intermediárias,
limites e validação documental final ficam no relatório e nos JSONs do registro
existente docs/validation/ec-cargo-parity-20261113/.

- T007 (implementada e verificada; parecer independente no registro): Corrigir a seleção persistente do Geiger após recorrência
  em ox-run-Fwke2bPi. Declarar executável e identidade no catálogo, rejeitar
  ausência/drift sem fallback, preservar descoberta dos demais plugins e
  verificar adaptador real com PATH original. Atualizar documentação e evidências
  afetadas; revisão e validação em contextos independentes. Escopo autorizado:
  reparo local sem instalação global, downloads, rotação, commits ou full run.
  Registro: docs/validation/geiger-selection-20261115/report.md.

T007: adaptador Geiger real aprovou16membros com PATH original e seleção local
explícita (exit0);68testes de scripts passaram com um skip opt-in. Após ajuste
isolado de literal em fixture, nove testes e ShellCheck/Ruff/Bandit passaram
novamente. Snapshots anteriores preservados; reexame delimitado e parecer
independente registrados, sem renovação dos hashes nem aceite global da feature.
Fechamento documental: scripts/README.md e spec/plan/tasks/evidence atualizados;
autoridades revisadas e limitações no relatório. Nenhum full run ou instalação.

- T008 (implementada e verificada no escopo delimitado; parecer final no registro): Confrontar claude_analisys.md com os contratos atuais, corrigir
  defeitos confirmados de scripts/ e seus oráculos, registrar disposição de todos
  os IDs, executar regressões focadas e obter revisão/validação independentes.
  Atualizar scripts/README.md e artefatos/evidências afetados, preservando histórico.
  Registro: docs/validation/claude-analysis-20261117/report.md.

T008: 132 testes de scripts, com um skip opt-in, passaram; a primeira execução
registrou 17 erros no consumidor JSON, corrigido e reexecutado. Após revisão
semântica independente, somente 17 bindings existentes foram atualizados; cinco
testes de catálogo/rejeição passaram novamente. Quatro regressões detectaram os
defeitos nas preimages. A suíte consumidora de governança passou 16 testes, e os
sucessores documentais tiveram 6+7+6 testes focados aprovados. ShellCheck central
não executou por restrição de escrita e pedido de escalonamento abortado; nenhum
scanner completo, download, commit ou publicação. Fixtures Rust/YARA preparadas
permanecem UNVERIFIED quanto ao casamento nativo. Fechamento documental: guias de
scripts/regras/fixtures e artefatos desta feature atualizados, com disposição de
cada ID, contratos preservados e entradas/limites no report. Revisão independente
não tem achados abertos; a validação independente e estados finais são registrados
em evidence.json/converge.md e docs/validation/claude-analysis-20261117/validation.md.

## Correções da análise combinada — 2026-11-17

- T090: corrigir defeitos confirmados e atualizar evidência afetada conforme
  [relatório](../../../docs/validation/claude-remediation-20261117/report.md).
  Verificações focadas e limites constam no relatório; aceite amplo não renovado.
