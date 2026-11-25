# AUDIT-AUTORIDADE-20261124 — Referência da auditoria aponta para a autoridade da constituição

- Data de abertura: 2026-11-24
- Rota: Local — troca de duas linhas numa referência da skill de auditoria; reversível, sem gate, checker ou autorização alterados
- Revisão atual: r2
- Spec(s): NOT APPLICABLE — rota Local; nenhuma capacidade de produto muda
- Estado: concluída

## 1. Prompt

Pedido original (literal): "Sim, corrigiria a referência da skill. Ela cria uma hierarquia
própria. No Ox, o AGENTS.md é o ponto de entrada, a constituição define a autoridade e o workflow
é o contrato de execução. Basta substituir as duas linhas por “Consulte a seção Governança do
processo da constituição do Ox”, com link direto."

### 1 - Objetivos

A referência `ox-governance.md` da skill `codex-task-audit` deixa de declarar uma ordem de
autoridade própria (constituição > AGENTS.md > workflow > skills), que diverge da cadeia da
constituição, e passa a apontar para a seção que a define. Público: quem audita tasks do Ox com
essa skill. Insumos: `sdd/constitution.md#governança-do-processo` e a referência atual.

### 2 - Requisitos

- Substituir as linhas 3–4 de `.claude/skills/codex-task-audit/references/ox-governance.md` pela
  linha
  `Consulte a seção [Governança do processo](../../../../sdd/constitution.md#governança-do-processo) da constituição do Ox.`
- Nenhum `.md` da skill declara ordem de autoridade.

### 3 - Restrições

- NÃO alterar o restante da referência, os outros arquivos da skill, a constituição, o workflow
  nem o AGENTS.md.
- NÃO implementar o registro do perfil delegado sugerido no mesmo pedido: muda o contrato do
  registro (workflow e template) e é task nova.
- NÃO fazer commit nem verificação completa.
- Permissões: editar a referência e criar este registro e `sdd/tasks/AUDIT-AUTORIDADE-20261124/`.

### 4 - Critérios de Aceitação

- AC-01: a abertura da referência é só a linha pedida e nenhum `.md` da skill tem `` `x` > `y` `` nem "Em divergência" | método: `bash sdd/tasks/AUDIT-AUTORIDADE-20261124/check.sh` | esperado: as linhas AC-01 com `ok` e exit 0
- AC-02: o link resolve para `sdd/constitution.md`, para um título existente, e a seção contém a cadeia de autoridade | método: `bash sdd/tasks/AUDIT-AUTORIDADE-20261124/check.sh` | esperado: as linhas AC-02 com `ok` e exit 0
- AC-03: o diff da referência contra HEAD remove só as duas linhas antigas e adiciona só a nova | método: `bash sdd/tasks/AUDIT-AUTORIDADE-20261124/check.sh` | esperado: as linhas AC-03 com `ok` e exit 0

### 5 - Entrega

- Arquivos/saídas: a referência; este registro; `sdd/tasks/AUDIT-AUTORIDADE-20261124/check.sh` e
  `mutations.sh`.
- Regra de conclusão: a task está concluída quando AC-01…AC-03 estiverem APPROVED
  ou NOT APPLICABLE e a seção 9 estiver preenchida.

## 2. Esclarecimentos

| Q | Pergunta | Resposta do usuário | AC/etapa afetados |
|---|---|---|---|

Suposições: `SUPOSIÇÃO: a substituição é literal; a frase "esta lista só diz onde olhar" sai junto,
porque está numa das duas linhas.`

## 3. Especificação

NOT APPLICABLE — rota Local

## 4. Plano

Skills lidas:

| SKILL.md | Motivo | Contribuição |
|---|---|---|
| `.codex/skills/prompt/SKILL.md` | etapas 1–2 | cinco divisões, guardrails em NÃO, AC em uma linha com método e esperado, suposição rotulada, regra de conclusão |
| `.codex/skills/technical-documentation/SKILL.md` | etapa 7, documentação afetada | uma explicação canônica com link no lugar da regra copiada; conferir link e identificador no destino |

## 5. Itens de trabalho

NOT APPLICABLE — rota Local

## 6. Coerência

NOT APPLICABLE — rota Local

## 7. Execução

| Item | Arquivos alterados | Teste executado | Exit | Observação |
|---|---|---|---|---|
| Referência | `.claude/skills/codex-task-audit/references/ox-governance.md` | `bash sdd/tasks/AUDIT-AUTORIDADE-20261124/check.sh` | 0 | linhas 3–4 trocadas por uma; 7 checks `ok` |
| Oráculo | `sdd/tasks/AUDIT-AUTORIDADE-20261124/check.sh`, `sdd/tasks/AUDIT-AUTORIDADE-20261124/mutations.sh` | `bash sdd/tasks/AUDIT-AUTORIDADE-20261124/mutations.sh` | 0 | numa cópia de HEAD: falha sem a correção, com âncora inexistente, com ordem de autoridade no `SKILL.md`, com outra linha alterada e com a seção sem a cadeia; passa com a correção (6 de 6) |
| Links e scripts da skill | — | `python3 tools/governance/scripts/check-ox.py`; `python3 -I .claude/skills/codex-task-audit/scripts/test_scripts.py` | 0; 0 | links locais com âncora `PASS`; 14 testes OK |

Falhas e tentativas abandonadas: a primeira execução de `python3 tools/governance/scripts/run-tests.py`
saiu com 1: `test_real_repository_passes` reprovou porque o `check-ox` leu como link a linha citada
neste registro, cujo caminho é relativo à skill. A citação passou para código (entre crases) e a
reexecução saiu com 0.

## 8. Validação

| Input | Caminho ou saída | Papel | SHA-256 |
|---|---|---|---|
| I-01 | `.claude/skills/codex-task-audit/references/ox-governance.md` | material | `3a291386305647cc490cdb8f809698820b324fbf6a1abb047c8a68d5b4c84c6e` |
| I-02 | `.claude/skills/codex-task-audit/SKILL.md` | material | `5fd17ab55787a23c9e768e0b5ab9643528c5288391bcc745e39a59a88af9ab01` |
| I-03 | `.claude/skills/codex-task-audit/references/metrics.md` | material | `b2f5bcac00fcceeadc83e7037a69afd6499375fcf97ce90f0fafcbc00315cef3` |
| I-04 | `.claude/skills/codex-task-audit/references/report-template.md` | material | `c66a649c7e085626e461afec88261e211b325c43ba4fc041f83ec20bfad3ff60` |
| I-05 | `sdd/tasks/AUDIT-AUTORIDADE-20261124/check.sh` | oráculo | `9478d71708f729de7c765c9e1f575cc2088bd1d0f8ed8146e64c69b232750d4a` |
| I-06 | `sdd/constitution.md` | oráculo | `ac86e4dc1f9af10da34c5bca1c53dce8a4d7f7a952b432f7f16bfe0bd64947d6` |

| AC | Critério (SHA-256) | Método executado | Inputs | Resultado observado | Estado |
|---|---|---|---|---|---|
| AC-01 | `8c79f5ef124840dffbdef47e34d9f7c1c5a86ddd10054bc62fb7866327e4ce60` | `bash sdd/tasks/AUDIT-AUTORIDADE-20261124/check.sh` | I-01, I-02, I-03, I-04, I-05 | linhas 1–5 da referência: título, vazia, `Consulte a seção [Governança do processo](../../../../sdd/constitution.md#governança-do-processo) da constituição do Ox.`, vazia, "## Por seção do registro da task…"; nos 4 `.md` da skill, nenhuma linha com `` `x` > `y` `` nem "Em divergência"; as 2 linhas AC-01 `ok`; exit 0 | APPROVED |
| AC-02 | `0019d8eca011a6fe56f4279c94efa9c85854ab42dec844be17c80f9a8a2c0880` | `bash sdd/tasks/AUDIT-AUTORIDADE-20261124/check.sh` | I-01, I-05, I-06 | o link resolve para `sdd/constitution.md`; `governança-do-processo` é o slug de "## Governança do processo", cuja seção contém "**Cadeia de autoridade:**"; as 3 linhas AC-02 `ok`; exit 0 | APPROVED |
| AC-03 | `ca19557c83ed741316b86ee406164c72a8684620be658b9283c594db0c19106a` | `bash sdd/tasks/AUDIT-AUTORIDADE-20261124/check.sh` (`git diff -U0 HEAD` da referência, HEAD `10d9570`) | I-01, I-05 | removidas exatamente as linhas "As regras estão no SDD; …" e "`sdd/constitution.md` > `AGENTS.md` > …"; adicionada só a linha nova; as 2 linhas AC-03 `ok`; exit 0 | APPROVED |

Contexto do validador: mesmo contexto — rota Local (etapa 8, passo 1)

## 9. Fechamento

- Documentação: `.claude/skills/codex-task-audit/references/ox-governance.md`, que é a própria
  entrega; nenhum outro `.md` da skill declara ordem de autoridade (AC-01).
- `sdd/project.md`: sem mudança — "Nenhuma task aberta" continua valendo depois do fechamento, e a
  task não altera escopo de produto nem estado de capacidade.
- Inputs da seção 8 alterados no fechamento: nenhum.
- Checks de governança: `python3 sdd/tools/validate.py --root .` exit 0;
  `python3 tools/governance/scripts/run-tests.py` exit 0 (257 testes, 1 pulado), depois da falha
  registrada na seção 7; `python3 tools/governance/scripts/check-ox.py` exit 0;
  `python3 sdd/tools/sddtask.py evidence --task AUDIT-AUTORIDADE-20261124 --check --require-all`
  exit 0 (0 problemas em 9 verificações).
- Pendências: registrar o perfil do orquestrador efetivamente criado e a referência ao evento de
  criação → muda o contrato do registro (workflow e template), fora desta task → task nova na
  rota Completa, quando pedida; commit e verificação completa → exigem pedido explícito
  (AGENTS.md).
- Estado final: concluída

## Revisão r2 — 2026-11-24 — Base fixa do AC-03

Motivo: o `check.sh` da r1 comparava a referência com HEAD. Com a correção commitada, esse diff
fica vazio e o AC-03 falha, o que foi observado numa cópia descartável: as 2 linhas AC-03 deram
`FALHA` e o exit foi 1. A comparação passa a usar o commit-base `10d9570`. O `mutations.sh` também
passa a montar a cópia a partir dele, porque, a partir de HEAD, o caso "sem a correção" passaria a
conter a correção.

### 1. Prompt

Pedido original (literal): "Há um ajuste antes do commit se o AC-03 precisar ser reproduzível
depois. O check.sh compara a referência com HEAD. Quando a correção entrar em HEAD, esse diff
ficará vazio e o AC-03 falhará. Fixar a comparação no commit-base já registrado, 10d9570, preserva
a checagem."

- AC-03: o diff da referência contra o commit-base `10d9570` remove só as duas linhas antigas e adiciona só a nova, inclusive com a correção já commitada | método: `bash sdd/tasks/AUDIT-AUTORIDADE-20261124/check.sh` e `bash sdd/tasks/AUDIT-AUTORIDADE-20261124/mutations.sh` | esperado: as linhas AC-03 com `ok` e exit 0; no `mutations.sh`, 0 casos divergentes de 7 e exit 0

O texto dos AC-01 e AC-02 não muda. Eles são reobservados porque citam o `check.sh` como input.
Restrições: NÃO alterar a referência da skill nem os critérios AC-01 e AC-02; NÃO fazer commit.

### 7. Execução

| Item | Arquivos alterados | Teste executado | Exit | Observação |
|---|---|---|---|---|
| Base fixa | `sdd/tasks/AUDIT-AUTORIDADE-20261124/check.sh`, `sdd/tasks/AUDIT-AUTORIDADE-20261124/mutations.sh` | `bash sdd/tasks/AUDIT-AUTORIDADE-20261124/check.sh`; o mesmo com base `0000…0000`; `bash sdd/tasks/AUDIT-AUTORIDADE-20261124/mutations.sh` | 0; 2; 0 | base padrão `10d9570ba57d98597491b2372e3e310dd46a7851`, que pode ser trocada por argumento; base ausente sai com 2 antes de comparar; 7 de 7 casos ok, o último com a correção commitada na cópia |

Falhas e tentativas abandonadas: nenhuma

### 8. Validação

| Input | Caminho ou saída | Papel | SHA-256 |
|---|---|---|---|
| I-07 | `sdd/tasks/AUDIT-AUTORIDADE-20261124/check.sh` | oráculo | `501eadb2f4d0aaf9df15271151c0101ba70ec5083b7c270e685e6c3d775d811f` |
| I-08 | `sdd/tasks/AUDIT-AUTORIDADE-20261124/mutations.sh` | oráculo | `f36e935166405f0f763a4a7e12303a001755f7fa9d680666ec5b483faea4d1c1` |

| AC | Critério (SHA-256) | Método executado | Inputs | Resultado observado | Estado |
|---|---|---|---|---|---|
| AC-01 | `8c79f5ef124840dffbdef47e34d9f7c1c5a86ddd10054bc62fb7866327e4ce60` | `bash sdd/tasks/AUDIT-AUTORIDADE-20261124/check.sh` | I-01, I-02, I-03, I-04, I-07 | as linhas 1–5 da referência são as mesmas da r1; nos 4 `.md` da skill, nenhuma linha com `` `x` > `y` `` nem "Em divergência"; as 2 linhas AC-01 `ok`; exit 0 | APPROVED |
| AC-02 | `0019d8eca011a6fe56f4279c94efa9c85854ab42dec844be17c80f9a8a2c0880` | `bash sdd/tasks/AUDIT-AUTORIDADE-20261124/check.sh` | I-01, I-06, I-07 | o link resolve para `sdd/constitution.md`; `governança-do-processo` é o slug de "## Governança do processo", cuja seção contém "**Cadeia de autoridade:**"; as 3 linhas AC-02 `ok`; exit 0 | APPROVED |
| AC-03 | `4029da1886970221fe9216e026cd579dec585ac4af6938c06d0518ddd98a31e7` | `bash sdd/tasks/AUDIT-AUTORIDADE-20261124/check.sh` (`git diff -U0 10d9570ba57d…` da referência) e `bash sdd/tasks/AUDIT-AUTORIDADE-20261124/mutations.sh` | I-01, I-07, I-08 | removidas exatamente as linhas "As regras estão no SDD; …" e "`sdd/constitution.md` > `AGENTS.md` > …"; adicionada só a linha nova; as 2 linhas AC-03 `ok`; exit 0. No `mutations.sh`, 0 casos divergentes de 7 e exit 0: falha sem a correção e nas 4 mutações, passa com a correção e passa com a correção commitada sobre a base, cujo diff contra HEAD é vazio | APPROVED |

Contexto do validador: mesmo contexto — rota Local (etapa 8, passo 1)

### 9. Fechamento

- Documentação: sem impacto — a revisão muda só os oráculos da task.
- `sdd/project.md`: sem mudança.
- Inputs da seção 8 alterados no fechamento: nenhum.
- Checks de governança: `python3 sdd/tools/validate.py --root .` exit 0;
  `python3 tools/governance/scripts/run-tests.py` exit 0 (257 testes, 1 pulado);
  `python3 tools/governance/scripts/check-ox.py` exit 0;
  `python3 sdd/tools/sddtask.py evidence --task AUDIT-AUTORIDADE-20261124 --check --require-all`
  exit 0 (0 problemas em 11 verificações; I-05, o `check.sh` da r1, fica sem referência).
- Pendências: as da r1.
- Estado final: concluída
