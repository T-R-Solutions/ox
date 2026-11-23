---
name: codex-task-audit
description: Análise independente, completa e exaustiva, em nível enterprise, da task que a IA Codex CLI planejou em .ai/task_planning.md e declarou concluída em .ai/task_completed.md no Ox. Use quando o usuário pedir para analisar, revisar, auditar ou dar parecer sobre a task do Codex. Compara plano e critérios de finalização com o relato e com o trabalho git não commitado, aplica as regras de .codex/skills e sdd/ (lógica, alternativas, testes de caminho feliz e infeliz, fragmentação, legado, segurança, governança, veracidade) e cria/atualiza .ai/task_analyzed.md com tudo o que precisa ser refatorado ou corrigido.
---

# Análise da task do Codex (`.ai/`)

Handoff entre as IAs:

| Arquivo | Autor | Conteúdo |
|---|---|---|
| `.ai/task_planning.md` | Codex, antes de implementar | plano da task e **critérios de finalização** |
| `.ai/task_completed.md` | Codex, ao concluir | tudo o que fez (arquivos, testes, comandos, resultados) |
| `.ai/task_analyzed.md` | **você** | parecer em rodadas com a lista de correções/refatorações |

Você não é o implementador: não confie em relato, checkbox marcado, hash ou "exit 0"
do Codex sem conferir o artefato real. Alegação do Codex é **pista**, nunca prova
(`docs/development/codex-agents.md`, POL-06, GOV-05). `.ai/` é ignorado pelo Git.

## Limites de atuação

- **Somente leitura no produto.** Não edite código, testes, SDD, skills, evidências
  nem os arquivos `.ai/` do Codex. Escrita permitida: `.ai/task_analyzed.md` e, como
  exige o `AGENTS.md`, uma **nova entrada ao final** de `task_finalizada.md`
  (append-only, nunca reescreva bytes anteriores).
- Experimentos que exigem alteração rodam em cópia no scratchpad, nunca na árvore.
- Não faça commit, stage, push, download, nem a verificação completa via Toolbox
  (`scripts/automate.sh run --scope complete`) sem pedido explícito. Checks focados
  documentados (unittest, `cargo test/clippy --offline`) são permitidos.
- A árvore pode estar sendo editada por outra sessão: registre `git status` e os
  sha256 dos arquivos `.ai/` no início e no fim; se algo mudar, declare na rodada.
- `claude_analysis.md` (raiz) é histórico do fluxo antigo: não escreva mais nele.

## Pré-condição

Se `.ai/task_planning.md` ou `.ai/task_completed.md` estiver ausente ou vazio, não
invente o plano nem o relato: registre uma rodada **INCONCLUSIVA** em
`.ai/task_analyzed.md` dizendo exatamente o que falta e pare. Se o planning não tiver
critérios de finalização identificáveis, isso já é uma correção (`alta`): sem
critério não há aceite (`sdd/evidence.md`).

## Procedimento

### 1. Ler as autoridades e as skills aplicáveis

`AGENTS.md`, `sdd/workflow.md` (rotas + contrato de fechamento), `sdd/evidence.md`
(cinco estados, schema 2), `docs/constitution.md` (POL/GOV), `docs/development/codex-agents.md`
(matriz de complexidade, revisão independente), `sdd/project.md` (escopo autorizado),
`.codex/skills/README.md`. Pelo catálogo, abra as skills de `.codex/skills/*/SKILL.md`
cujo domínio o plano ou o diff toca (ex.: `rust`, `iced-engineering`, `software-testing`,
`application-security`, `commit-governance`) e use as regras delas como critério de
revisão. Registre na rodada quais skills foram **realmente lidas** e o que cada uma
contribuiu — indicação não é consulta. Tasks visuais: `DESIGN.md`,
`docs/design/surfaces.md`. Detalhes: [governança Ox](references/ox-governance.md).

### 2. Inventário

```bash
python3 -I .claude/skills/codex-task-audit/scripts/task_inventory.py --root . > <scratch>/inventory.json
python3 -I .claude/skills/codex-task-audit/scripts/task_inventory.py --root . --format md
```

O script (exit 2 se `.ai/` estiver incompleto ou fora de repositório) entrega: título
e sha256 dos dois arquivos; critérios extraídos de títulos de critério/aceite/
finalização (com estado do checkbox); arquivos não commitados fora de `.ai/` e
`.claude/`; **alterados sem citação** em `task_completed.md` (escopo não relatado);
**citados sem mudança** (alegação a conferir; `NÃO EXISTE` é forte sinal de alegação
falsa); **planejados e não relatados**; e se `task_finalizada.md` foi alterado só por
acréscimo. A extração é heurística: leia os dois arquivos inteiros e corrija o que o
script não capturou. Testes do script: `python3 -I .claude/skills/codex-task-audit/scripts/test_scripts.py -v`
(rode se alterar os scripts).

### 3. Plano × relato × diff

Leia `task_planning.md` e `task_completed.md` integralmente e `git diff HEAD` (mais
os não rastreados) dos caminhos da task. Monte:

- **Matriz de critérios**: cada critério de finalização → o que o relato alega → o
  que você observou (diff, execução própria, experimento) → estado **ATENDIDO /
  PARCIAL / NÃO ATENDIDO / NÃO VERIFICÁVEL**. Checkbox `[x]` não é evidência.
- **Plano × execução**: passos planejados não executados; trabalho feito fora do
  plano (confira se o escopo de `sdd/project.md` o autoriza); critérios enfraquecidos
  ou reinterpretados no relato.
- **Alegações × observado**: contagem de testes, exits, arquivos, hashes, revisões.

### 4. Coletar evidências próprias

- Rode os checks focados (em background, em paralelo) e guarde logs no scratchpad:
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts/tests -v`,
  `... -s tools/governance/tests -v`, e em `application/`:
  `CARGO_HOME=$PWD/../.cache/ox/cargo-home cargo test --workspace --locked --offline`
  e `cargo clippy --workspace --all-targets --locked --offline -- -D warnings`.
  Rode só o que a task toca; compare com o que o Codex alegou.
- Sinais de dívida no diff:
  `python3 -I .claude/skills/codex-task-audit/scripts/diff_signals.py --root . --paths <caminhos da task>`
  (TODO/FIXME, depreciado, `#[allow]`, `#[ignore]`, `skip`, `unwrap/expect` fora de
  testes, supressões de scanner, caches/binários, arquivos grandes, funções novas sem
  teste). Sinal ≠ defeito: confirme lendo.
- Leia o código alterado **linha a linha** nos trechos de lógica; para docs/evidência,
  confira links, hashes (`sha256sum`) e alegações numéricas.
- Para cada defeito relevante, confirme com experimento pequeno e inofensivo (cópia em
  scratchpad, entrada adversarial, teste de sensibilidade: o teste falha se a correção
  for revertida?).

Em task grande, distribua por superfície (scripts/automação, governança/evidência,
UI Rust/Iced, skills/docs) entre subagentes independentes, entregando a cada um este
SKILL.md, as referências, os dois arquivos `.ai/` e a lista exata de caminhos. Eles
**não** rodam suítes pesadas (evita disputa de lock do Cargo); você fornece os logs.
Reconfira pessoalmente toda correção crítica/alta antes de publicá-la.

### 5. Avaliar pelas métricas

Aplique as 20 métricas de [métricas](references/metrics.md) — escala 0–4 ou N/A,
com justificativa citando `arquivo:linha`. Obrigatórias:

| ID | Pergunta |
|---|---|
| M01 | A lógica de programação usada é correta? |
| M02 | Havia alternativa “mais correta” (mais simples, robusta, idiomática)? |
| M03 | Todo o trabalho feito foi testado? |
| M04 | Os testes cobrem caminho feliz **e** infeliz, bordas e vários cenários? Teriam detectado o defeito? |
| M05 | Houve fragmentação do código (duplicação, lógica espalhada, módulos sem coesão)? |
| M06 | Deixou código legado, morto, depreciado ou compatibilidade sem prazo? |

e as complementares M07–M20 (escopo, veracidade, governança SDD, erros, segurança,
compatibilidade, desempenho, manutenibilidade, documentação, observabilidade,
integridade/concorrência, UX/acessibilidade, dependências/licenças, higiene do diff).

Cada problema vira uma **correção** `C<n>` com severidade **crítica / alta / média /
baixa / info** e grau de verificação: `✔ exp` (experimento executado), `✔ lido`
(linhas lidas), `✔ run` (check executado por você), `rev` (subagente, não
reconferido), `estimativa`. Nunca apresente `rev` ou `estimativa` como confirmado.
Toda correção indica a regra violada (critério do planning, skill de `.codex/skills`,
`sdd/`, POL/GOV) e uma ação concreta que o Codex possa executar.

### 6. Veredito

- **APROVADA** — todos os critérios ATENDIDOS; nenhuma correção ≥ média; alegações conferem.
- **APROVADA COM RESSALVAS** — critérios atendidos; correções médias/baixas sem risco de dado/segurança/gate.
- **REPROVADA** — critério NÃO ATENDIDO/PARCIAL, correção crítica/alta, alegação falsa material ou teste que não protege o que diz.
- **INCONCLUSIVA** — evidência insuficiente (diga o que faltou).

O veredito é independente e não altera estados SDD do Codex.

### 7. Escrever `.ai/task_analyzed.md`

Siga [o modelo](references/report-template.md), escrito para o Codex executar.

- **Arquivo inexistente:** crie com o bloco de topo e a `# Rodada 1`.
- **Arquivo existente:** é insumo. Leia a última rodada e verifique cada `C<n>`
  ainda aberto contra o estado atual: **CORRIGIDO / PENDENTE / REGREDIU** (com
  evidência). Correções novas continuam a numeração (`C<n>` nunca é reutilizado).
  Acrescente `# Rodada N — <título da task> — <data>` ao **final**; reescreva apenas o
  bloco de topo entre `<!-- task-analyzed:status -->` e `<!-- /task-analyzed:status -->`
  (estado atual e índice de rodadas). Nunca altere rodadas anteriores.
- Se o título do planning mudou para outra task, diga isso no topo da nova rodada e
  trate as correções antigas como encerradas por troca de task (não as apague).

### 8. Fechamento

Registre na rodada o que **não** foi feito (ex.: verificação Toolbox completa,
inspeção visual nativa) e por quê. Confira que os sha256 dos arquivos `.ai/` não
mudaram durante a análise. Acrescente a entrada ao final de `task_finalizada.md` e
confira por comparação binária (`cmp -n <tamanho anterior>`) que o prefixo foi
preservado. Responda ao usuário com o veredito, a contagem de correções abertas por
severidade, as 5 mais graves e o caminho `.ai/task_analyzed.md`.

## Armadilhas recorrentes no trabalho do Codex (verifique sempre)

- Critério marcado `[x]` ou "concluído" no relato sem evidência executável.
- `task_completed.md` citando arquivo, teste ou comando que não existe no diff/árvore.
- Critério de finalização reescrito ou enfraquecido entre o planning e o relato.
- Evidência volumosa (JSON de milhares de linhas, hashes) que prova estrutura, não comportamento.
- Testes que passam por motivo errado (qualquer exit≠0 vira sucesso; fixture feita à mão
  que não corresponde à saída real; assert só de presença de string).
- “Revisão independente” feita no mesmo contexto do implementador.
- Correções que adicionam camada nova sem remover a antiga (fragmentação/legado).
- Relatórios que afirmam execução de checks cujos logs não existem ou divergem.
- Artefatos de execução versionáveis por engano (`__pycache__`, `.bin` grandes, `.log`).
- Escopo maior que o autorizado em `sdd/project.md`, ou arquivo alterado que o relato omite.
