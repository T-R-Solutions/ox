# <ID> — <título curto>

- Data de abertura: <AAAA-MM-DD>
- Rota: <Local | Completa> — <motivo em uma linha>
- Revisão atual: r1
- Spec(s): <`sdd/specs/<capacidade>.md` | NOT APPLICABLE — motivo>
- Estado: <aberta | concluída | incompleta | bloqueada>

<!-- Gerado por `sddtask.py new`; regras em sdd/workflow.md. -->

## 1. Prompt

Pedido original (literal): "<texto do usuário>"

### 1 - Objetivos

<…>

### 2 - Requisitos

- <…>

### 3 - Restrições

- NÃO <…>
- Permissões: <…>

### 4 - Critérios de Aceitação

- AC-01: <condição> | método: <…> | esperado: <…>

### 5 - Entrega

- Arquivos/saídas: <…>
- Regra de conclusão: a task está concluída quando AC-01…AC-n estiverem APPROVED
  ou NOT APPLICABLE e a seção 9 estiver preenchida.

## 2. Esclarecimentos

| Q | Pergunta | Resposta do usuário | AC/etapa afetados |
|---|---|---|---|

Suposições: <`SUPOSIÇÃO: …` | nenhuma>

## 3. Especificação

Motivação: <…>

- REQ-01: <…>
- AC-01 → REQ-01

Cenários rejeitados: <entrada → comportamento>

## 4. Plano

| Decisão | REQ | Escolha | Alternativa descartada e motivo |
|---|---|---|---|
| D-01 | REQ-01 | | |

Skills lidas:

| SKILL.md | Motivo | Contribuição |
|---|---|---|
| `.codex/skills/prompt/SKILL.md` | etapas 1–2 | <…> |

ADR: <`docs/decisions/<nome>.md` | NOT APPLICABLE — motivo>

## 5. Itens de trabalho

| Item | D | Arquivos (dono) | Depende de | Teste | Pronto quando | Skill |
|---|---|---|---|---|---|---|
| T-01 | D-01 | | — | | | |

## 6. Coerência

Matriz (`validate.py --matrix`): exit <n>

Conflitos com POL/GOV/RQ: <nenhum | conflito e ADR>

## 7. Execução

| Item | Arquivos alterados | Teste executado | Exit | Observação |
|---|---|---|---|---|

Falhas e tentativas abandonadas: <… | nenhuma>

## 8. Validação

| Input | Caminho ou saída | Papel | SHA-256 |
|---|---|---|---|

| AC | Critério (SHA-256) | Método executado | Inputs | Resultado observado | Estado |
|---|---|---|---|---|---|

Contexto do validador: <independente | mesmo contexto — motivo>

## 9. Fechamento

- Documentação: <caminhos | sem impacto: motivo>
- `sdd/project.md`: <atualizado | sem mudança>
- Inputs da seção 8 alterados no fechamento: <nenhum | ACs reobservados>
- Checks de governança: <comandos e exits | NOT APPLICABLE — motivo>
- Pendências: <item → motivo → retomada | nenhuma>
- Estado final: <concluída | incompleta | bloqueada>
