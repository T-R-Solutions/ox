# Modelo de `.ai/task_analyzed.md`

Escreva em pt-BR, frases curtas, tabelas onde comparam. Cite `arquivo:linha`. O
leitor principal é o Codex: cada correção deve ser executável sem reinterpretar.

O arquivo tem um bloco de topo (único trecho reescrito a cada rodada) e rodadas
acrescentadas ao final. Rodadas anteriores nunca são alteradas; `C<n>` nunca é
reutilizado.

```markdown
# Análise da task — <título do task_planning.md>

<!-- task-analyzed:status -->
**Estado atual (rodada N, AAAA-MM-DD):** <VEREDITO>
Correções abertas: <c> crítica · <a> alta · <m> média · <b> baixa · <i> info.
Abertas por prioridade: C3, C7, C1, …

| Rodada | Data | Veredito | Novas | Corrigidas | Pendentes |
|---|---|---|---|---|---|
| 1 | AAAA-MM-DD | REPROVADA | 9 | — | 9 |
<!-- /task-analyzed:status -->

# Rodada 1 — <título> — AAAA-MM-DD

## Cabeçalho

- Branch `<branch>`, base `<sha curto>` (<data>).
- Entradas: `.ai/task_planning.md` sha256 `<…>`; `.ai/task_completed.md` sha256 `<…>`.
- Árvore: <n> arquivos alterados fora de `.ai/`; estado igual no início e no fim? <sim/não>.
- Método: skill `codex-task-audit`; skills/autoridades lidas e contribuição
  (ex.: `.codex/skills/rust/SKILL.md` — regra de erros sem `unwrap`).
- Limites: <o que não foi executado e por quê>.

## Veredito

<VEREDITO> — 2 a 4 frases com o motivo determinante.

## Matriz de critérios de finalização

| # | Critério (planning, linha) | Alegado (completed) | Observado | Estado | Correções |
|---|---|---|---|---|---|
| K1 | … (L12) | "testes passam" | `cargo test` 41/41 ✔ run | ATENDIDO | — |
| K2 | … (L13) | `[x]` | sem teste do erro de I/O | PARCIAL | C2 |

## Plano × execução

- Planejado e não feito: …
- Feito fora do plano: … (autorizado em `sdd/project.md`? sim/não)
- Alterado e não relatado: …
- Critérios enfraquecidos/reinterpretados: …

## Alegações × observado

| Alegação | Onde (completed, linha) | Observado por mim | Confere? |

## Métricas

| M01 | M02 | M03 | M04 | M05 | M06 | M07 | … | M20 | Média |
Uma linha por métrica relevante com nota < 4 citando `C<n>`.

## Correções e refatorações necessárias

### C1 · alta · <título curto> — ✔ exp
- **Onde:** `caminho/arquivo.rs:120-134`
- **Problema:** o que está errado e o impacto observado (entrada → saída).
- **Regra violada:** critério K2 / `.codex/skills/software-testing/SKILL.md` / POL-05.
- **Evidência:** comando, saída ou experimento.
- **Ação:** o que o Codex deve mudar (refatorar, corrigir, testar, remover).
- **Aceite da correção:** como a próxima rodada vai verificar (teste que deve
  existir e falhar sem a correção, comando e resultado esperado).

## Seguimento da rodada anterior (a partir da rodada 2)

| Correção | Estado | Evidência |
|---|---|---|
| C1 | CORRIGIDO | `tests/x.rs:40` falha com a correção revertida ✔ exp |
| C4 | PENDENTE | trecho inalterado ✔ lido |

## Apêndice — comandos e resultados

Comandos exatos, exit codes, contagens, caminhos dos logs no scratchpad.
```
