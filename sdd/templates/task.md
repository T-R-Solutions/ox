# <ID> — <título curto>

- Data de abertura: <AAAA-MM-DD>
- Rota: <Local | Completa> — <motivo em uma linha>
- Revisão atual: r1
- Spec(s): <`sdd/specs/<capacidade>.md` ou NOT APPLICABLE — motivo>
- Estado: <aberta | concluída | incompleta | bloqueada>

<!-- Uma seção por etapa de sdd/workflow.md. Etapa que não se aplica:
"NOT APPLICABLE — <motivo>". Apague este comentário ao instanciar. -->

## 1. Prompt

Pedido original (literal): "<texto do usuário>"

### 1 - Objetivos

<resultado pretendido, público, insumos>

### 2 - Requisitos

- <comportamento ou entregável concreto>

### 3 - Restrições

- NÃO <o que não fazer>
- Preservar <o que não pode mudar>
- Permissões: <o que o pedido autoriza e o que não autoriza>

### 4 - Critérios de Aceitação

- AC-01: <condição observável> | método: <comando ou inspeção> | esperado: <resultado>
- AC-02: <condição> | PENDENTE: Q-1  <!-- só enquanto a pergunta Q-1 estiver aberta -->

### 5 - Entrega

- Arquivos/saídas: <lista>
- Regra de conclusão: a task está concluída quando AC-01…AC-n estiverem APPROVED
  ou NOT APPLICABLE com motivo, e a seção 9 estiver preenchida.

## 2. Esclarecimentos

| Q | Pergunta | Resposta do usuário | AC/etapa afetados |
|---|---|---|---|
| Q-1 | | | |

Suposições: `SUPOSIÇÃO: <texto>`

## 3. Especificação

Motivação (por quê): <texto>

- REQ-01: <comportamento ou invariante>
- AC-01 → REQ-01

Cenários rejeitados: <entrada inválida → comportamento esperado>

## 4. Plano

| Decisão | REQ | Escolha | Alternativa descartada e motivo |
|---|---|---|---|
| D-01 | REQ-01 | | |

Skills lidas (obrigatória em toda rota com registro; no mínimo `prompt`):

| SKILL.md | Motivo | Contribuição |
|---|---|---|

ADR: <`docs/decisions/<nome>.md` ou NOT APPLICABLE — motivo>

## 5. Itens de trabalho

| Item | D | Arquivos (dono) | Depende de | Teste | Pronto quando | Skill |
|---|---|---|---|---|---|---|
| T-01 | D-01 | | — | | | <`nome` registrado em Skills lidas, ou `nenhuma: <motivo>`> |

## 6. Coerência

`python3 sdd/tools/validate.py --root . --task <ID> --matrix`: exit <n> (matriz derivada das
seções 3–5; não redigir à mão).

Conflitos com POL/GOV/RQ: <nenhum | conflito e ADR>

## 7. Execução

| Item | Arquivos alterados | Teste executado | Exit | Observação |
|---|---|---|---|---|

Falhas e tentativas abandonadas: <texto ou "nenhuma">

## 8. Validação

| Input | Caminho ou saída | Papel | SHA-256 |
|---|---|---|---|
| I-01 | `<caminho relativo à raiz; log citado fica em sdd/tasks/<ID>/, nunca em .local/>` | material | `<64 hex>` |

| AC | Critério (SHA-256) | Método executado | Inputs | Resultado observado | Estado |
|---|---|---|---|---|---|
| AC-01 | `<64 hex da linha do AC>` | <comando> | I-01 | <resultado> | <estado> |

Hashes: o verificador devolve as linhas sem hashes; quem escreve o registro roda
`python3 sdd/tools/sddtask.py evidence --task <ID> --write` e depois `--check --require-all`.
Não calcular à mão.

Papéis: `material`, `oráculo`, `configuração`. Todo AC decidido cita ao menos um
`material` e um `oráculo`; se o método não tiver oráculo separado, a célula Inputs diz
`sem oráculo separado: <motivo>`. Método e resultado nunca ficam vazios. Célula de caminho com exatamente um
`caminho` entre crases (ou um link) é conferida por bytes; outra forma é registrada como
não verificável. IDs `I-n` são únicos no registro inteiro. Observação substituída: mover
a linha para uma subseção `### … (obsoletas)` com o motivo.

Contexto do validador: <independente | mesmo contexto — motivo>

## 9. Fechamento

- Documentação: <caminhos atualizados na etapa 7 | sem impacto: motivo>
- `sdd/project.md`: <atualizado na etapa 7 | sem mudança>
- Inputs da seção 8 alterados no fechamento: <nenhum (`evidence --check --require-all` exit 0) | ACs reobservados>
- Checks de governança: <comandos e exit codes | NOT APPLICABLE — motivo>
- Pendências: <item → motivo → passo de retomada | nenhuma>
- Estado final: <concluída | incompleta | bloqueada>

<!-- Depois do fechamento, correções entram ao final, sem alterar o que está acima:

## Revisão r2 — <AAAA-MM-DD>

Motivo: <correção pedida>

### 8. Validação

(mesmas tabelas; novos IDs I-n; por AC vale a observação da revisão mais recente)
-->
