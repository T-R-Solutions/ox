# Tarefas — PROMPT-WORKFLOW-20261119

- T001: registrar pedido, prompt, análise e plano; raiz/orquestrador.
- T002: implementar contrato e compatibilidade limitada; implementador, depende T001.
- T003: revisar independentemente e corrigir achados; revisor, depende T002.
- T004: executar checks exigidos e validar critérios independentemente; depende T003.
- T005: registrar disposição documental, resultado e pendências nos logs; depende T004.

Documentação revisada: AGENTS, workflow, procedimento de agentes, skill prompt,
ponte e perfil, project, evidence e ADR de contratos vivos. Atualizações efetivas e
limitações serão consolidadas no report.md; os logs .ai mantêm o histórico local.

## Retomada da revisão 2 — 23 de novembro de 2026 UTC

T001, T002 e T003 preservados com os mesmos inputs históricos. O prompt da retomada
foi anexado pela raiz antes da execução. T004 executou check-ox e a suíte integral
serialmente, ambos com exit 0 e inputs estáveis. A suíte concluiu 296 execuções,
incluindo os seis casos do contrato de prompt, sem falhas, erros ou skips. A
validação independente recebe os resultados atuais antes do aceite final.

T005 em fechamento documental. O report.md registra trabalho, evidências e limites;
a raiz é a única escritora dos logs .ai e task_finalizada.md. AC-03 permanece
dependente da anexação do resultado e da conferência independente de conteúdo e
preservação dos prefixos. Nenhum reparo material foi necessário na retomada.

## Aceite final — 23 de novembro de 2026 UTC

T004 concluída com os cinco critérios aprovados independentemente. T005 teve a
disposição documental registrada, os três logs efetivamente acrescidos pela raiz
e seus prefixos/conteúdo verificados pelo validador. O check-ox documental final
passou com exit 0, stderr vazio e inputs estáveis. A raiz registra a confirmação
final que resolve a pendência histórica de AC-03. Não resta implementação, teste,
revisão ou critério de aceite pendente no escopo autorizado.
