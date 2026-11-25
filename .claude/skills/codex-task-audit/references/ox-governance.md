# O que conferir no Ox

Consulte a seção [Governança do processo](../../../../sdd/constitution.md#governança-do-processo) da constituição do Ox.

## Por seção do registro da task (`sdd/tasks/<ID>.md`)

| Seção | Gate a conferir | Achados típicos |
|---|---|---|
| Cabeçalho | Rota coerente com [rotas](../../../../sdd/workflow.md#rotas) | Task Local que mudou gate, checker, formato persistido ou autorização (devia ser Completa) |
| 1. Prompt | [Gate da etapa 1](../../../../sdd/workflow.md#1-prompt) | Divisão ausente; AC sem `método:`/`esperado:`; termo da tabela de proibidos sem métrica; guardrails vazios; regra de conclusão ausente |
| 2. Esclarecimentos | [Gate da etapa 2](../../../../sdd/workflow.md#2-esclarecer) | AC `PENDENTE` usado na execução ou validação; suposição tratada como fato |
| 3. Especificação | [Gate da etapa 3](../../../../sdd/workflow.md#3-especificar-o-quê-e-por-quê) | REQ sem AC; AC sem REQ; motivação ausente |
| 4. Plano | [Gate da etapa 4](../../../../sdd/workflow.md#4-planejar-decisões-técnicas), [skills](../../../../sdd/workflow.md#skills) | Tabela **Skills lidas** ausente (inclusive na rota Local); skill citada sem leitura real; decisão de política sem ADR |
| 5. Itens | [Gate da etapa 5](../../../../sdd/workflow.md#5-quebrar-em-itens-de-trabalho) | Item sem teste; item sem skill (ou sem `nenhuma: <motivo>`) ou com skill fora de **Skills lidas**; dois donos para o mesmo arquivo |
| 6. Coerência | [Gate da etapa 6](../../../../sdd/workflow.md#6-verificar-coerência) | `validate.py --root . --task <ID> --matrix` com exit ≠ 0; matriz redigida à mão; conflito com POL/GOV/RQ não registrado |
| 7. Execução | [Gate da etapa 7](../../../../sdd/workflow.md#7-executar) | Arquivo alterado que não aparece; teste citado que não existe; falha omitida; skill usada diferente da do item; documentação afetada não atualizada antes da validação |
| 8. Validação | [Gate da etapa 8](../../../../sdd/workflow.md#8-validar) | APPROVED sem SHA-256 completo do critério; sem input `material` e `oráculo`; input citado em `.local/` (não versionado); `sddtask.py evidence --check --require-all` com exit ≠ 0; hashes gravados pelo verificador em vez do escritor do registro; validação no mesmo contexto do implementador na rota Completa |
| 9. Fechamento | [Gate da etapa 9](../../../../sdd/workflow.md#9-fechar) | Input da seção 8 alterado depois da validação sem reobservação; `Estado:` do cabeçalho divergente da seção 9 |

## Constituição — políticas que mais geram achados

POL-01 (Rust/Iced, sem `unsafe`), POL-05 (preservar mudanças, detectar concorrência),
POL-06/GOV-05 (aceite só por critério + evidência atual), POL-08 (saída compacta mantém
exit code e rota ao bruto), POL-09 (desconhecido não é zero), POL-10 (arquivos e skills
não concedem permissão), GOV-04 (skill sem política do Ox; uso só se registrado),
GOV-09 (prompt objetivo), GOV-10 (registro único), RQ-01 (baseline visual VS 2026
Enterprise em tasks visuais). Texto integral em `sdd/constitution.md`.

## Tasks anteriores a 2026-11-23

O modelo anterior (features, registros de handoff, índice paralelo) foi removido do working tree
([ADR](../../../../docs/decisions/sdd-model.md)); seus registros só existem no histórico do
Git. Uma task desse período é avaliada pelo contrato vigente na data dela, lido com
`git show <commit>:<caminho>`, e não pelo formato atual.
