# Modelo de `sdd/tasks/<ID>.review.md`

pt-BR, frases curtas, tabelas onde comparam, `arquivo:linha` em toda afirmação. O leitor
principal é o dono da task: cada correção deve ser executável sem reinterpretar. Rodadas
são acrescentadas ao final; nada anterior é alterado; `C<n>` nunca é reutilizado.

```markdown
# <ID> — Parecer externo

## Revisão r1 — AAAA-MM-DD

**Parecer:** <APROVADA | APROVADA COM RESSALVAS | REPROVADA | INCONCLUSIVA | aceite da fase N recomendado | aceite pendente>.
<1 a 3 frases com o motivo determinante.>

### Escopo

1. **Objetivo** — …
2. **Requisitos** — …
3. **Restrições** — somente leitura; escrita só neste parecer; …
4. **Critérios** — …
5. **Entrega** — … Regra de conclusão: …

Skills lidas: `<SKILL.md>` — contribuição. Contexto: <quem revisou e por que é independente>.
Snapshot: `HEAD <sha>`; registro da task SHA-256 `<64 hex>` no início e no fim.

### Correções

#### C1 · alta · <título curto> — ✔ exp
- **Onde:** `caminho:linha`
- **Problema:** entrada → saída observada e impacto.
- **Regra violada:** gate da etapa N / POL-xx / GOV-xx / `<SKILL.md>`.
- **Evidência:** comando, saída ou experimento.
- **Ação:** o que o dono da task deve mudar.
- **Aceite da correção:** como a próxima revisão vai verificar.

### Critérios reconferidos

| AC | SHA-256 do critério | Método, material e oráculo | Resultado | Estado |
|---|---|---|---|---|

Reprodução: `LC_ALL=C`; SHA-256 completo sobre bytes sem transformação; saída de vários
comandos = concatenação dos stdout na ordem.

| Caminho | SHA-256 |
|---|---|

### Métricas

| M01 | M02 | M03 | M04 | M05 | M06 | M07 | … | M20 | Média |

### Seguimento da revisão anterior (a partir de r2)

| Correção | Estado | Evidência |
|---|---|---|

### Comandos e limites

Comandos exatos e exit codes; o que não foi executado e por quê.
```
