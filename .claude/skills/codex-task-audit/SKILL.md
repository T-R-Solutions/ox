---
name: codex-task-audit
description: Revisão independente, completa e exaustiva, em nível enterprise, de uma task do Ox registrada em sdd/tasks/<ID>.md (normalmente executada pelo Codex CLI). Use quando o usuário pedir para analisar, revisar, auditar ou dar parecer sobre uma task. Confronta prompt, critérios, especificação, plano, itens, matriz, execução e validação do registro com o diff não commitado e com os bytes atuais, aplica as regras de sdd/ e das skills de .codex/skills (lógica, alternativas, testes de caminho feliz e infeliz, fragmentação, legado, segurança, governança, veracidade) e grava o parecer em sdd/tasks/<ID>.review.md.
---

# Revisão de task do Ox

| Arquivo | Dono | Conteúdo |
|---|---|---|
| `sdd/tasks/<ID>.md` | executor da task (Codex) | prompt, plano, itens, matriz, execução, validação, fechamento |
| `sdd/tasks/<ID>.review.md` | **você** | parecer, em revisões acrescentadas ao final |

Você não é o implementador: relato, checkbox, hash ou "exit 0" do registro é **pista**,
nunca prova (POL-06, GOV-05). Confira o artefato real.

## Limites de atuação

- **Somente leitura no produto e no registro da task.** Escrita permitida: apenas
  `sdd/tasks/<ID>.review.md`. Não edite o registro da task, código, testes, SDD ou skills;
  correções são pedidas no parecer e feitas pelo dono da task.
- O parecer é preservado: cada rodada é uma seção `## Revisão rN — <data>` acrescentada
  ao final; nunca reescreva bytes anteriores (o registro da task pode citar o SHA-256
  do parecer como input).
- Experimentos que exigem alteração rodam em cópia no scratchpad.
- Não faça commit, stage, push, download nem a verificação completa via Toolbox sem
  pedido explícito. Checks focados (unittest, `cargo test/clippy --offline`) são permitidos.
- Registre o `git status` e o SHA-256 do registro da task no início e no fim; se mudarem
  durante a revisão, declare no parecer.

## Procedimento

### 1. Delimitar

Use a skill `prompt` (`.codex/skills/prompt/SKILL.md`) para escrever o escopo do parecer
com as cinco divisões do [workflow](../../../sdd/workflow.md#1-prompt): objetivo,
requisitos, restrições, critérios e entrega. Escolha a task: a indicada pelo usuário ou,
na falta, a de `Estado: aberta` alterada mais recentemente em `sdd/tasks/`.

### 2. Ler as autoridades e as skills aplicáveis

`sdd/constitution.md`, `sdd/project.md` e `sdd/workflow.md` (inclui o mapa de skills e os
papéis dos agentes). Pelo [mapa de skills](../../../sdd/workflow.md#skills), leia os `SKILL.md` cujo domínio a task
toca (ex.: `rust`, `iced-engineering`, `software-testing`, `application-security`) e use
as regras deles como critério. Registre no parecer as skills **realmente lidas** e a
contribuição de cada uma. O que conferir por seção: [governança Ox](references/ox-governance.md).

### 3. Inventário mecânico

```bash
python3 -I .claude/skills/codex-task-audit/scripts/task_inventory.py --root . [--task <ID>] > <scratch>/inventory.json
python3 -I .claude/skills/codex-task-audit/scripts/task_inventory.py --root . [--task <ID>] --format md
```

Usa o parser único `sdd/tools/sddtask.py` **do checkout que contém esta skill** (o código
do `--root` auditado nunca é executado) e chama o Git com `--no-optional-locks` (não
regrava `.git/index`). Evidência vigente inclui as revisões `## Revisão rN` (vale a mais
recente por AC). Entrega: divisões do prompt presentes; ACs
sem método, sem esperado ou `PENDENTE`; REQ sem AC e AC sem REQ; **frescor** (SHA-256 do
critério e de cada input da seção 8 recalculados sobre os bytes atuais: `fresh`, `stale`,
`malformed`, `missing`, `unverifiable`; referência a input inexistente, input ou
observação duplicados, AC decidido sem inputs); arquivos alterados no Git que a seção 7 não cita e
caminhos citados sem mudança; revisões já existentes no parecer. Exit 2: registro
ausente, inválido ou fora de repositório. Rode também
`sdd/tools/validate.py --root . --task <ID> --matrix` e
`sdd/tools/sddtask.py evidence --task <ID> --check --require-all` e registre os exit codes.
Testes do script: `python3 -I .claude/skills/codex-task-audit/scripts/test_scripts.py -v`.

### 4. Conferir registro × realidade

- **Prompt (seção 1):** cada AC tem condição, método e esperado mensuráveis; guardrails
  explícitos; regra de conclusão verificável; nenhum termo subjetivo sem métrica.
- **Matriz (seções 3–6):** a matriz `REQ → D → T → AC` é derivada das seções 3–5 por
  `validate.py --matrix`; confira se as decisões e os itens fazem sentido técnico, não só
  se os IDs fecham.
- **Execução (seção 7) × diff:** `git diff HEAD` e não rastreados; todo arquivo alterado
  aparece; todo teste citado existe e roda.
- **Validação (seção 8):** reproduza os métodos; recalcule os hashes; confira papéis
  (`material`, `oráculo`, `configuração`) e se o verificador rodou em contexto independente.
- **Fechamento (seção 9):** documentação, `project.md`, reobservação de inputs alterados e
  `Estado:` do cabeçalho.

### 5. Coletar evidências próprias

- Rode os checks focados que a task toca (em background, logs no scratchpad):
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools/governance/tests -v`,
  `... -s scripts/tests -v`, e em `application/`:
  `CARGO_HOME=$PWD/../.cache/ox/cargo-home cargo test --workspace --locked --offline` e
  `cargo clippy --workspace --all-targets --locked --offline -- -D warnings`.
- Sinais de dívida no diff:
  `python3 -I .claude/skills/codex-task-audit/scripts/diff_signals.py --root . --paths <caminhos>`.
  Sinal ≠ defeito: confirme lendo.
- Leia o código alterado linha a linha nos trechos de lógica. Para cada defeito relevante,
  confirme com experimento pequeno (cópia no scratchpad, entrada adversarial, teste de
  sensibilidade: o teste falha se a correção for revertida?).

Em task grande, distribua por superfície entre subagentes independentes, entregando
este SKILL.md, as referências, o registro da task e a lista exata de caminhos. Eles não
rodam suítes pesadas; você fornece os logs. Reconfira pessoalmente toda correção
crítica ou alta antes de publicá-la.

### 6. Avaliar pelas métricas

Aplique M01–M20 de [métricas](references/metrics.md) (0–4 ou N/A, com `arquivo:linha`).
Cada problema vira uma correção `C<n>` com severidade (crítica, alta, média, baixa, info),
grau de verificação (`✔ exp`, `✔ run`, `✔ lido`, `rev`, `estimativa`), regra violada
(gate do workflow, POL/GOV/RQ, skill) e ação concreta para o dono da task.

### 7. Veredito

- **APROVADA:** todos os ACs decididos e sustentados; nenhuma correção ≥ média.
- **APROVADA COM RESSALVAS:** ACs sustentados; correções médias ou baixas sem risco.
- **REPROVADA:** AC REJECTED ou sem sustentação, correção crítica ou alta, alegação falsa
  material, hash que não confere, ou teste que não protege o que diz.
- **INCONCLUSIVA:** evidência insuficiente (diga o que faltou).

Para uma fase de task aberta, use "aceite da fase recomendado" ou "aceite pendente". O
veredito é independente e não altera estados no registro da task.

### 8. Escrever `sdd/tasks/<ID>.review.md`

Siga [o modelo](references/report-template.md). Arquivo inexistente: crie com a revisão
r1. Arquivo existente: leia a última revisão, verifique cada `C<n>` aberto
(CORRIGIDO, PENDENTE, REGREDIU), acrescente a nova revisão ao final e continue a
numeração de `C<n>`.

### 9. Fechamento

Registre o que não foi feito (Toolbox, inspeção visual nativa) e por quê. Confira que o
SHA-256 do registro da task não mudou durante a revisão. Responda ao usuário com o
veredito, as correções abertas por severidade, as 5 mais graves e o caminho do parecer.

## Armadilhas recorrentes (verifique sempre)

- AC marcado APPROVED com hash truncado, sem critério vinculado ou sem oráculo.
- Matriz redigida à mão na seção 6 em vez da saída de `validate.py --matrix`.
- Seção 7 citando arquivo ou teste que não existe no diff ou na árvore.
- Critério reescrito ou enfraquecido entre revisões sem nova observação.
- Testes que passam por motivo errado (qualquer exit≠0 vira sucesso; fixture feita à mão;
  assert só de presença de string).
- "Revisão independente" feita no mesmo contexto do implementador.
- Correção que adiciona camada nova sem remover a antiga (fragmentação/legado).
- Regra do SDD copiada para skill, AGENTS ou outro documento (duplicação de autoridade).
- Artefatos de execução versionados por engano (`__pycache__`, `.log`, binários grandes).
- Escopo maior que o autorizado no prompt da task ou em `sdd/project.md`.
