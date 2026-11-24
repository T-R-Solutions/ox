# SDD-ENXUTO-20261123 — Enxugar o SDD e remover o legado

- Data de abertura: 2026-11-23
- Rota: Completa — muda o contrato de governança (workflow, agentes, validador) e remove o histórico
- Revisão atual: r4
- Spec(s): NOT APPLICABLE — mudança de processo; as specs de produto migradas são insumo, não capacidade nova
- Estado: concluída

## 1. Prompt

Pedido original (literal): "Faça a correção dos problemas ainda existentes. O fluxo deve ser
assim [...] Quando o usuário escreve um pedido/tarefa, ele deve primeiro se transformar em um
prompt (através da skill de prompt). [...] Refatore como o sdd está configurado para algo mais
objetivo e centralizado. [...] grande parte desses itens, existem skills para isso, então é
delegado às skills. E apague todo o legado do projeto." Decisões do usuário na mesma conversa:
apagar sem commit de checkpoint; hashes gerados por ferramenta; 6 perfis de agente; itens
limítrofes conforme a recomendação, "mais enxuto, com coesão e coerência, sem perder a sinergia
entre as etapas e sem perder dados técnicos".

### 1 - Objetivos

Deixar o SDD do Ox com uma única fonte por regra e o fluxo pedido → prompt → constituição →
especificar → esclarecer → planejar → itens → coerência → executar → validar → fechar, com o
método delegado às skills de `.codex/skills/`; corrigir os problemas medidos na análise anterior
(referência a procedimento inexistente nos perfis do Codex, 13 perfis, hashes e matriz manuais,
catálogo de skills em 5 lugares) e remover o legado. Público: o mantenedor e os agentes Codex.
Insumos: `AGENTS.md`, `sdd/`, `.codex/`, `tools/governance/`, `docs/`, plano aprovado em
`/home/rodrigo/.claude/plans/fa-a-a-corre-o-dos-kind-flamingo.md`.

### 2 - Requisitos

- R-1: `sdd/workflow.md` é o único contrato: rotas, etapas 0–9 com saída, skill, papel e gate,
  mapa de skills e regras de agentes; `sdd/skills.md`, `sdd/agents.md` e `sdd/README.md` deixam
  de existir.
- R-2: os perfis do Codex são 6 (`ec_orquestrador_normal`, `ec_orquestrador_alta`,
  `ec_planejador`, `ec_implementador`, `ec_implementador_extra_alto`, `ec_verificador`) e cada um,
  e o `config.toml`, aponta para uma âncora existente de `sdd/workflow.md`.
- R-3: `sdd/tools/sddtask.py evidence --task <ID>` calcula os sha256 da seção 8; `validate.py`
  deriva a matriz REQ → D → T → AC das seções 3–5 e não exige `task_finalizada.md`.
- R-4: os fatos técnicos vigentes do legado são movidos antes da remoção: 10 specs de produto em
  `sdd/specs/`, insumos de `docs/validation/` usados por código ou docs vivos movidos para junto
  do consumidor, fatos de ADRs de processo consolidados em `docs/decisions/sdd-model.md`.
- R-5: o legado listado no passo 9 do plano é removido do working tree.
- R-6: a política de evidência externa da skill `prompt` vai para um arquivo de referência
  carregado só quando o prompt tem afirmação factual externa.
- R-7: `check-ox.py`, testes de governança, `automation.json`, `NOTICE`, `.gitignore`, índices
  de `docs/` e a skill `.claude/skills/codex-task-audit/` ficam alinhados ao modelo novo.

### 3 - Restrições

- NÃO commitar, fazer stage, push ou reescrever o histórico Git.
- NÃO rodar a verificação completa via Toolbox (não autorizada neste pedido).
- NÃO alterar código Rust de produto nem `application/vendor/`.
- NÃO atualizar pin de `reviews.static` de arquivo vivo alterado sem revisão independente
  registrada das classes revisadas (subprocess sem shell, literais `/tmp`, XML do corpus SVG) e
  de padrões novos; pins de arquivos removidos saem.
- NÃO apagar `scripts/config/native/gitleaks/gitleaks-history.ignore` (o histórico Git continua).
- NÃO enfraquecer checks: cada check removido de `check-ox.py` corresponde a um artefato removido.
- NÃO apagar um arquivo antes de mover seus fatos técnicos vigentes (R-4).
- Preservar as mudanças não commitadas de arquivos que permanecem (POL-05).
- Manter a skill `prompt` genérica, sem política do Ox (GOV-04).
- Permissões: o pedido autoriza editar e remover arquivos locais do repositório e da pasta
  ignorada `.local/`; não autoriza downloads, publicação nem commit.

### 4 - Critérios de Aceitação

- AC-01: estrutura e tasks do SDD válidas | método: `python3 sdd/tools/validate.py --root .` | esperado: exit 0
- AC-02: testes das ferramentas do SDD, incluindo `evidence` e a matriz derivada, passam | método: `python3 -m unittest discover -s sdd/tools/tests` | esperado: exit 0, ao menos 1 teste de `evidence` e 1 de matriz com órfão
- AC-03: check de governança passa | método: `python3 tools/governance/scripts/check-ox.py` | esperado: exit 0
- AC-04: testes de governança passam | método: `python3 tools/governance/scripts/run-tests.py` | esperado: exit 0
- AC-05: testes de scripts passam | método: `python3 -m unittest discover -s scripts/tests` | esperado: exit 0
- AC-06: testes da skill de auditoria passam | método: `python3 -m unittest discover -s .claude/skills/codex-task-audit/scripts` | esperado: exit 0
- AC-07: 6 perfis do Codex, TOML válido e âncoras existentes | método: `python3 sdd/tasks/SDD-ENXUTO-20261123/ac07_agents.py` (conta `.codex/agents/*.toml`, carrega os 7 arquivos com `tomllib` e confere cada `#âncora` contra os títulos de `sdd/workflow.md`) | esperado: exit 0, `perfis=6 carregados=7 ancoras_ausentes=0`
- AC-08: nenhum arquivo ativo referencia o legado | método: `bash sdd/tasks/SDD-ENXUTO-20261123/ac08_legacy_grep.sh` (grep em `git ls-files` + não rastreados pelos termos do legado, com as exclusões listadas no script: registro e artefatos desta task, ADR `sdd-model.md`, `gitleaks-history.ignore`, corpus sintético de `scripts/tests`, `OX-PATCH.md` de vendor e os ledgers de proveniência de `docs/licensing/`) | esperado: exit 0, `ocorrencias=0`
- AC-09: caminhos do legado ausentes | método: `test -e` em cada linha de `sdd/tasks/SDD-ENXUTO-20261123/removed-paths.txt` (passo 9 do plano; `docs/decisions/local-persistence-experiment-20261105.md` saiu da lista por ser decisão de produto, ver seção 7) | esperado: 0 caminhos existentes
- AC-10: specs de produto migradas | método: `ls sdd/specs/*.md` e `validate.py --root .` | esperado: 10 specs além do README, cada uma com tabela "Estado atual" e validação exit 0
- AC-11: evidência deste registro gerada pela ferramenta e atual | método: `python3 sdd/tools/sddtask.py evidence --task SDD-ENXUTO-20261123 --check --require-all` | esperado: exit 0
- AC-12: leitura obrigatória não cresce | método: `wc -w AGENTS.md sdd/constitution.md sdd/project.md sdd/workflow.md .codex/skills/prompt/SKILL.md` | esperado: total ≤ 5635 palavras (medição anterior, que também incluía `sdd/agents.md`)

### 5 - Entrega

- Arquivos/saídas: `sdd/workflow.md`, `sdd/constitution.md`, `sdd/project.md`, `AGENTS.md`,
  `sdd/templates/task.md`, `sdd/specs/*.md`, `sdd/tools/*.py` e testes, `.codex/config.toml`,
  `.codex/agents/*.toml`, `.codex/skills/prompt/`, `docs/decisions/sdd-model.md`,
  `tools/governance/`, `scripts/config/automation.json`, `.claude/skills/codex-task-audit/`,
  remoções do passo 9 do plano.
- Regra de conclusão: a task está concluída quando AC-01…AC-12 estiverem APPROVED
  ou NOT APPLICABLE com motivo, e a seção 9 estiver preenchida.

## 2. Esclarecimentos

| Q | Pergunta | Resposta do usuário | AC/etapa afetados |
|---|---|---|---|
| Q-1 | Quais itens limítrofes apagar? | "O que você sugere? Quero algo mais enxuto, com coesão e coerência, sem perder a sinergia entre as etapas e sem perder dados técnicos" → recomendação aprovada no plano | AC-08, AC-09, AC-10 |
| Q-2 | Como preservar as mudanças não commitadas? | "Apagar sem commit" | AC-09 |
| Q-3 | Como fica a validação? | "Hashes gerados por ferramenta" | AC-02, AC-11 |
| Q-4 | Quantos perfis? | "6 perfis" | AC-07 |

SUPOSIÇÃO: IDs POL/GOV/RQ não são renumerados; uma regra revogada some sem renumerar as demais.
SUPOSIÇÃO: estados de AC das specs migradas são herdados do `evidence.json` e marcados como
herdados; a evidência bruta não é migrada.

## 3. Especificação

Motivação (por quê): a análise de 2026-11-23 mediu que o núcleo do SDD já tinha fonte única,
mas os perfis do Codex citam um procedimento que só existe no histórico congelado, a etapa 8
exige hashes manuais, a matriz da etapa 6 é redigida à mão, o catálogo de skills vive em 5
lugares e o legado ainda é referenciado por cerca de 60 arquivos ativos.

- REQ-01: o SDD tem um único contrato de execução com etapa → skill → papel → gate.
- REQ-02: os agentes do Codex são 6 e cada instrução aponta para seção existente.
- REQ-03: hashes e matriz de coerência são produzidos pela ferramenta.
- REQ-04: nenhum dado técnico vigente se perde na remoção do legado.
- REQ-05: o legado não existe nem é referenciado pelos arquivos ativos.
- REQ-06: as verificações existentes continuam passando.
- AC-01 → REQ-01
- AC-12 → REQ-01
- AC-07 → REQ-02
- AC-02 → REQ-03
- AC-11 → REQ-03
- AC-10 → REQ-04
- AC-08 → REQ-05
- AC-09 → REQ-05
- AC-03 → REQ-06
- AC-04 → REQ-06
- AC-05 → REQ-06
- AC-06 → REQ-06

Cenários rejeitados: task com REQ sem item → `validate.py` falha com a matriz derivada; hash de
AC desatualizado → `sddtask.py evidence --check` sai com 1; perfil que cita âncora inexistente →
check de links do `check-ox.py` falha.

## 4. Plano

| Decisão | REQ | Escolha | Alternativa descartada e motivo |
|---|---|---|---|
| D-01 | REQ-01 | Absorver `skills.md`, `agents.md` e `README.md` em `workflow.md`, com tabela por etapa | Manter os três arquivos: o contrato continua dividido em 3 fontes |
| D-02 | REQ-02 | 6 perfis; `ec_verificador` junta revisão, testes e validação em contexto independente | 8 perfis com revisor e testador separados: a árvore tem no máximo 2 especialistas simultâneos |
| D-03 | REQ-03 | Subcomando `evidence` em `sddtask.py` e matriz derivada em `validate.py` | Remover os hashes: perde a detecção de critério alterado na retomada |
| D-04 | REQ-04 | Migrar specs de produto e insumos usados antes da remoção; ADR `sdd-model.md` consolida as decisões de processo vigentes | Apagar sem migrar: perde estado de AC de produto e insumos de scripts |
| D-05 | REQ-05 | Remover com `rm` no working tree e limpar referências ativas | Reescrever o histórico Git: destrutivo, não pedido |
| D-06 | REQ-06 | Ajustar `check-ox.py`, testes e configs aos artefatos removidos, sem afrouxar os checks restantes | Desligar checks que falharem: viola a restrição de não enfraquecer |

Skills lidas (obrigatória em toda rota com registro; no mínimo `prompt`):

| SKILL.md | Motivo | Contribuição |
|---|---|---|
| `.codex/skills/prompt/SKILL.md` | Etapas 1–2 | Estrutura do prompt, guardrails, ACs com método e esperado, perguntas Q-1…Q-4 |
| `.codex/skills/software-delivery/SKILL.md` | Etapa 5, mapeada no mapa de skills anterior | Lida e descartada: trata build e release, não fatiamento de itens; ordem dos itens definida pelas dependências da seção 5 |
| `.codex/skills/software-testing/SKILL.md` | Etapas 5, 7 e 8 | Oráculo independente (bytes reais e sha256 recalculado), casos normal e de falha de `evidence` e da matriz |

ADR: `docs/decisions/sdd-model.md`

## 5. Itens de trabalho

| Item | D | Arquivos (dono) | Depende de | Teste | Pronto quando |
|---|---|---|---|---|---|
| T-01 | D-04 | `sdd/specs/*.md`, insumos movidos de `docs/validation/`, `docs/decisions/sdd-model.md`, links em README/DESIGN/docs | — | AC-10 | 10 specs geradas e insumos movidos |
| T-02 | D-01 | `sdd/workflow.md`, `sdd/constitution.md`, `sdd/project.md`, `AGENTS.md`, `sdd/templates/task.md` | T-01 | AC-01, AC-12 | workflow com etapa → skill → papel → gate |
| T-03 | D-03 | `sdd/tools/sddtask.py`, `sdd/tools/validate.py`, `sdd/tools/tests/` | T-02 | AC-02, AC-11 | testes novos passam |
| T-04 | D-02 | `.codex/config.toml`, `.codex/agents/*.toml` | T-02 | AC-07 | 6 perfis com âncoras válidas |
| T-05 | D-01 | `.codex/skills/prompt/` | — | AC-12 | referência separada e SKILL.md menor |
| T-06 | D-06 | `tools/governance/`, `scripts/config/automation.json`, `scripts/tests/`, `NOTICE`, `.gitignore`, `.claude/skills/codex-task-audit/` | T-02 | AC-03, AC-04, AC-05, AC-06 | checks e testes passam |
| T-07 | D-05 | remoções do passo 9 do plano | T-01, T-06 | AC-08, AC-09 | caminhos ausentes e 0 referências |

## 6. Coerência

Matriz derivada por `sdd/tools/validate.py --root . --task SDD-ENXUTO-20261123`. Conflitos com a
constituição: nenhum; a mudança de GOV-04/GOV-05/GOV-10 tem ADR (`docs/decisions/sdd-model.md`).

## 7. Execução

| Item | Arquivos alterados | Teste executado | Exit | Observação |
|---|---|---|---|---|
| T-01 | `sdd/specs/*.md` (10 + README), `docs/design/reference-members.json`, `docs/licensing/{license-inventory,copy-provenance,license-review-20261109,duplicate-review-20261113}.json`, `tools/governance/config/external-fingerprints.json`, `docs/decisions/sdd-model.md`, `NOTICE`, links em README/DESIGN/docs (subagente, arquivos disjuntos) | `validate.py --root .`; `check-ox.py` | 0; 0 | Specs geradas de `spec.md` + `evidence.json`; 78 de 147 linhas de limitação eram controle de evidência e saíram |
| T-02 | `sdd/workflow.md`, `sdd/constitution.md`, `sdd/project.md`, `AGENTS.md`, `sdd/templates/task.md` | `validate.py --root .`; `wc -w` | 0; 5586 palavras | `skills.md`/`agents.md` absorvidos; seção `Local full-verification environment` mantida (consumida por `commit-governance` e testes) |
| T-03 | `sdd/tools/sddtask.py`, `sdd/tools/validate.py`, `sdd/tools/tests/*` | `unittest discover -s sdd/tools/tests` | 0 (56 testes) | Subcomando `evidence`, `--matrix`, specs `(herdado)` |
| T-04 | `.codex/config.toml`, `.codex/agents/*.toml` (8 removidos, `ec_verificador` criado) | `tools/governance/tests/test_instruction_routes.py` | 0 | 6 perfis, âncoras `#papel-*` |
| T-05 | `.codex/skills/prompt/SKILL.md`, `references/evidence-policy.md` | `skill-quick-validate.py`; `check-new-skills.py` | 0; 0 | SKILL.md de 1763 para 1533 palavras |
| T-06 | `tools/governance/scripts/{check-ox,governance_support,check-new-skills}.py`, `tools/governance/tests/*`, `scripts/config/automation.json`, `scripts/config/native/{bandit/bandit-baseline.json,ruff/ruff.toml}`, `docs/assets/{check.py,render.mjs}`, `.gitignore`, `.claude/skills/codex-task-audit/*` | `run-tests.py`; `unittest -s scripts/tests`; testes da skill de auditoria; `docs/assets/check.py` | 0; 0; 0; 0 | Pins de 11 arquivos removidos; entradas de baseline/ignore desses arquivos removidas |
| T-07 | remoção de `sdd/tasks/SDD-ENXUTO-20261123/removed-paths.txt` (53 caminhos, 6,2 GB) | `test -e` por caminho; grep do AC-08 | 0 existentes; 0 ocorrências | Sem stage/commit |

Falhas e tentativas abandonadas:
- O agente de documentação editou `application/vendor/cryoglyph-0.1.0/OX-PATCH.md`, contra a restrição de não alterar `vendor/`; a edição foi revertida e o arquivo entrou nas exclusões do AC-08.
- Antes da remoção, `license-review.json` e `duplicate-review.json` (dados técnicos de dependências citados por `docs/licensing/dependency-policy-20261109.md`) não estavam na lista de migração; foram recuperados do Git (`HEAD:docs/validation/...`) para `docs/licensing/` depois de o `check-ox.py` apontar os links quebrados.
- `docs/decisions/local-persistence-experiment-20261105.md` estava na lista de ADRs de processo do plano, mas registra decisões D2–D4 de produto; foi mantido (AC-09 ajustado).
- A primeira verificação independente encontrou defeitos em `sddtask.py evidence`: `--write` renovava hash desatualizado, inputs fora da raiz e de texto livre passavam, `\|` quebrava a linha, `--check` passava sem observações. Corrigidos com testes de regressão; `--require-all` adicionado ao AC-11. Também restaurada a checagem de ID normativo duplicado no `check-ox.py`, removida junto com a cobertura normativa.

## 8. Validação

Estado estável observado em 2026-11-24, depois das seções 9.1–9.2. Logs brutos em `.local/tasks/SDD-ENXUTO-20261123/` (ignorado pelo Git). Hashes preenchidos por `sddtask.py evidence --write`.

| Input | Caminho ou saída | Papel | SHA-256 |
|---|---|---|---|
| I-01 | `sdd/workflow.md` | material | `ef24127a9ffd594e153b6a4011f5744de8af032ac0264397d84249965047cb58` |
| I-02 | `sdd/constitution.md` | material | `ac86e4dc1f9af10da34c5bca1c53dce8a4d7f7a952b432f7f16bfe0bd64947d6` |
| I-03 | `sdd/project.md` | material | `ae1e1881e030ba421b53784a6f738f26e884c2c85221308dba4c3ae97d1c1e57` |
| I-04 | `AGENTS.md` | material | `dd53cb5f25f71bf3c6e1f72042a7a3628f67e50495b4b15c328ff5ec78158be0` |
| I-05 | `.codex/skills/prompt/SKILL.md` | material | `98bb62af25b1e62dda471c3ba032c73f45283af96400404db71224afdb3c05d5` |
| I-06 | `sdd/tools/validate.py` | oráculo | `79bbf719f8349375ea31eaf02335ecc9edaca5b1944eb4093da3e589ae6e9b59` |
| I-07 | `sdd/tools/sddtask.py` | material | `c07b392b424a1e62929273e73ccde83f742cde98cd21645e6f62f6439daae2b8` |
| I-08 | `sdd/tools/tests/test_sddtask.py` | oráculo | `9e3453f89113ee32db60a7e2655df7d3c675a051386cbc8e8db5572714a10e7c` |
| I-09 | `sdd/tools/tests/test_validate.py` | oráculo | `6358d776f8461fdf19b0b31ec75ebc276e2705053b9209ca413b7152b04ea211` |
| I-10 | `tools/governance/scripts/check-ox.py` | oráculo | `a7dfbe0d7571dbde89626a6fe867ddff905ee4dad71f313d86563e9f27bd6604` |
| I-11 | `tools/governance/scripts/governance_support.py` | material | `3b104bff72c0a367b0893b512d42d8ff7027f292b131b401b208fe88812fd058` |
| I-12 | `tools/governance/scripts/run-tests.py` | oráculo | `cc6d9abfa079238390232253f7b6f839b100fa62eedeadd82a29241daaec2df0` |
| I-13 | `tools/governance/tests/test_check_ox.py` | oráculo | `f8ac80490ef370e62d212e1a9f1f142a7e758bc3d1ef3d379c312975e268bf3f` |
| I-14 | `tools/governance/tests/test_instruction_routes.py` | oráculo | `3f5351582664377865dbcbb8bd14ce922b1cb9cca3c14ab8b5866bcdc3a4be91` |
| I-15 | `scripts/config/automation.json` | configuração | `a0501f14fb3a5eb2a540d7d582d79cb69e76a4de618bb43eb021cccdcd8fb98e` |
| I-16 | `.claude/skills/codex-task-audit/scripts/task_inventory.py` | material | `381fa4142f920304b1abfedfe46407be865b5d4ef2a4e67f42db87a4f2a8a010` |
| I-17 | `.claude/skills/codex-task-audit/scripts/test_scripts.py` | oráculo | `62f35bdb39dddde5877e587c5310d38422e9b7ddbc2663f00de83f919dc881c9` |
| I-18 | `sdd/tasks/SDD-ENXUTO-20261123/ac07_agents.py` | oráculo | `c1012419a54fe22640163e91cee558320cd4c7efb79c286c9fdc2f64362d82a1` |
| I-19 | `.codex/config.toml` | material | `3373184901ce9b92473745e280a2dff6e436260c1e341377e21676099e3524f7` |
| I-20 | `.codex/agents/ec_implementador.toml` | material | `221eca00aaff59a2305acc89a726581b6d8014cb9956c11f60390d3d57bbc899` |
| I-21 | `.codex/agents/ec_implementador_extra_alto.toml` | material | `dc68fb6f6c94445e249f9204c12dc66d3d5f0446c97915a895fd6312df63aa39` |
| I-22 | `.codex/agents/ec_orquestrador_alta.toml` | material | `19a01c64e2e2cdc1094ec74beac423b6c22eaa682daa3db8c91886091d110fcd` |
| I-23 | `.codex/agents/ec_orquestrador_normal.toml` | material | `a28af5010a0a933f9835193afa82928c55befd8a2a6a7478fbdc4efae3e76cd1` |
| I-24 | `.codex/agents/ec_planejador.toml` | material | `5dfc1d4e91e0f2a6bb768a941d5898ac8c6c5ff37459c1fd5f4d518333cc7b85` |
| I-25 | `.codex/agents/ec_verificador.toml` | material | `a2b183478a9c08c1fe070a823354e6c481186af10765b77bbde7d920d951a646` |
| I-26 | `sdd/tasks/SDD-ENXUTO-20261123/ac08_legacy_grep.sh` | oráculo | `46a5654a53f02637f649bbd5188a3bde09c7907f2c3ac8262a2ba9ea49d76590` |
| I-27 | `sdd/tasks/SDD-ENXUTO-20261123/removed-paths.txt` | material | `73f6803b0a3192264276d21747a945e1ee6ccbc60cd9e4eed8bd7a34ab593fe0` |
| I-28 | `sdd/specs/README.md` | material | `d1b27f89c2b4d5f538defe917fff29c5337f9f7b8a48222f11657d8f3726ee49` |
| I-29 | `sdd/specs/agent-runtime.md` | material | `b33edff053454d9a405f5cdd66c5d11f600a428313db205da046d25976c05d98` |
| I-30 | `sdd/specs/bootstrap.md` | material | `79595bddd4d729359a390e679c9f72b94198d8a7626c3520bcf0fd8db8aaa719` |
| I-31 | `sdd/specs/f0-gate.md` | material | `2d3cc73ddc98efafda6290351dcd9c49d2dda347f41b314290d5fa233a4e1965` |
| I-32 | `sdd/specs/foundation.md` | material | `b59a488d343c97e64bd753c3b31a78dd40eb2fb91a2cc9d5b97849dccb465868` |
| I-33 | `sdd/specs/ide-shell.md` | material | `2a1b18917e039ccb9951719e8e89d67f78c222958f371bfc10d46a562078f555` |
| I-34 | `sdd/specs/local-persistence.md` | material | `133e5e4822dcbb606fe6e5d655c427cafc8ca273ae1423a3d2446c08d132cb0d` |
| I-35 | `sdd/specs/local-task-ui.md` | material | `0f76671ff4e8600de2696db4dafdede264aeca8047893607ba113ebe67c044b8` |
| I-36 | `sdd/specs/plugin-host.md` | material | `d68ed7e2c12ce9794072bf3cc1900c9e289f9f69a8b2d533eba7aedc20e2ff58` |
| I-37 | `sdd/specs/verification-engine.md` | material | `3f279b5894a3e7e1a604df0db241528b479063a04c046ab22d3deae79f5a2bf8` |
| I-38 | `sdd/specs/visual-workbench.md` | material | `cde4695813a9e00f9612d41998eeeca8470f11508cf645dd7d119277b9e21569` |
| I-39 | `.local/tasks/SDD-ENXUTO-20261123/ac01.log` | material | `a786814fa8faeb6e99afa71e194456f198cda12635cad661e05b06b530b3c4a1` |
| I-40 | `.local/tasks/SDD-ENXUTO-20261123/ac02.log` | material | `5fbcd85c11835afaa6f0f9f321c30e07f747740d15e12944e63067d54f33c7c4` |
| I-41 | `.local/tasks/SDD-ENXUTO-20261123/ac03.log` | material | `d0d4150a251c8b8b22833843b794d5d61e9fbc6583fb70f5f81467e7d5127b7b` |
| I-42 | `.local/tasks/SDD-ENXUTO-20261123/ac04.log` | material | `a379407fa5da0f8c87cc8ed9ca6ebdd07499814a63ce3cce4267388403bb7306` |
| I-43 | `.local/tasks/SDD-ENXUTO-20261123/ac05.log` | material | `ac436f86f961497de652ef774c524987580e1004e712d53570e05a6aaaabf305` |
| I-44 | `.local/tasks/SDD-ENXUTO-20261123/ac06.log` | material | `8ecc31b95f72ae59087362662105fcd2974c9ffbe59a76799292e44fe1c74999` |
| I-45 | `.local/tasks/SDD-ENXUTO-20261123/ac07.log` | material | `56bed67c321a641b6b4328cb81dd12863e7d28fa7390ff19683cf74ee88e3223` |
| I-46 | `.local/tasks/SDD-ENXUTO-20261123/ac08.log` | material | `75af20d326616ff20e436dc0b3633c9563a1d631b885341ee47bfb38e64618fa` |
| I-47 | `.local/tasks/SDD-ENXUTO-20261123/ac09.log` | material | `252dfb01199a20009d56105dcecd4f737acf3004f6e78d744a1f9c7c9cd30632` |
| I-48 | `.local/tasks/SDD-ENXUTO-20261123/ac10.log` | material | `7aa2ef88a436b089cd811a506a69bdf2eeec4be165f7a649fa605e7a3098c8f2` |
| I-49 | `.local/tasks/SDD-ENXUTO-20261123/ac12.log` | material | `0b5397dad408e3ec3636601e3db3bd33e374fb6e17691c37c6557346f3887c02` |

| AC | Critério (SHA-256) | Método executado | Inputs | Resultado observado | Estado |
|---|---|---|---|---|---|
| AC-01 | `976460c5db8915d8a26fabae631fb2e0dcb82c8885e721d506836e13a93d3009` | `python3 sdd/tools/validate.py --root .` | I-01, I-02, I-03, I-06, I-39 | exit 0; `PASS: estrutura, 1 task(s), 10 spec(s)` | APPROVED |
| AC-02 | `e38241e576702fd076f0b7173afce3cfdf4ca0a30ed11b75f2d48ca3ff13a02a` | `python3 -m unittest discover -s sdd/tools/tests` | I-07, I-06, I-08, I-09, I-40 | exit 0; 58 testes OK, incluindo 9 de `evidence` (stale não renovado, contenção, pipe escapado, `--require-all`) e 2 de matriz com órfão | APPROVED |
| AC-03 | `2beadd2d209c3063b5a20d2d15e9384f32720268927730bf7a86856bc08c3cbf` | `python3 tools/governance/scripts/check-ox.py` | I-01, I-02, I-03, I-11, I-10, I-41 | exit 0; `PASS: SDD, normative IDs, skill map, local links and external-content inspection` | APPROVED |
| AC-04 | `a0a0ecb4b4ff7e1aab6cabd430190638c01fe1ae391f47765256a2cf257f88ee` | `python3 tools/governance/scripts/run-tests.py` | I-10, I-11, I-12, I-13, I-14, I-42 | exit 0; 234 testes OK (1 skip: `test_native_scans` exige Docker) | APPROVED |
| AC-05 | `4ccd98b2c08036983a837a292f6e73613b919175db77cfa916722c9311a0d694` | `python3 -m unittest discover -s scripts/tests` | I-15, I-43; sem oráculo separado: a suíte `scripts/tests` inteira (139 testes) é o oráculo | exit 0; 139 testes OK (1 skip) | APPROVED |
| AC-06 | `3f5cb04f17bccd467b8294c3cb23d06edd84ab31b726d391af068d57d386158b` | `python3 -m unittest discover -s .claude/skills/codex-task-audit/scripts` | I-16, I-17, I-44 | exit 0; 14 testes OK | APPROVED |
| AC-07 | `7bc6848013db06b1f23bfea23678f05faec36ed3ca3319093682d9c789d6ba5f` | `python3 sdd/tasks/SDD-ENXUTO-20261123/ac07_agents.py` | I-19, I-20, I-21, I-22, I-23, I-24, I-25, I-01, I-18, I-45 | exit 0; `perfis=6 carregados=7 ancoras_ausentes=0` | APPROVED |
| AC-08 | `5177f9d96970de8b8d474172ae1abe2058466c9e318e86c33901f8ac639164c9` | `bash sdd/tasks/SDD-ENXUTO-20261123/ac08_legacy_grep.sh` | I-15, I-26, I-46 | exit 0; `ocorrencias=0` | APPROVED |
| AC-09 | `edf1e569dfe03576bd2a40200510f5ca2499e48bb39e9129b25297a740d5755a` | `test -e` por linha de `removed-paths.txt` | I-27, I-47; sem oráculo separado: `test -e` do shell decide existência | 53 caminhos, `existentes=0` | APPROVED |
| AC-10 | `067c8a92d7df97b61770d1d7551d89c27cecb342b34ad136d9a3fdeb31f4b76c` | `ls sdd/specs/*.md`; `validate.py --root .` | I-28, I-29, I-30, I-31, I-32, I-33, I-34, I-35, I-36, I-37, I-38, I-06, I-48 | 10 specs além do README, cada uma com 1 seção `## Estado atual`; validate exit 0 (10 specs). Estados conferidos pelo verificador independente contra `HEAD:sdd/features/product-*/evidence.json` | APPROVED |
| AC-11 | `b8bdc4f0649d2bbab59ee346933b4b761d1bc8d0e0df7e9fab3ef2a762145ba6` | `python3 sdd/tools/sddtask.py evidence --task SDD-ENXUTO-20261123 --check --require-all` | I-07, I-08 | exit 0; `0 problema(s) em 61 verificação(ões)` (12 critérios e 49 inputs atuais) | APPROVED |
| AC-12 | `cb4e2b764bf57dea1e90fafdb7f859eac431ae468c17ecf8a9da96e75dbadeca` | `wc -w AGENTS.md sdd/constitution.md sdd/project.md sdd/workflow.md .codex/skills/prompt/SKILL.md` | I-04, I-01, I-02, I-03, I-05, I-49; sem oráculo separado: `wc -w` e o limite do critério | 5602 palavras ≤ 5635 | APPROVED |

Contexto do validador: duas verificações independentes em contexto novo (sem o histórico desta sessão). A primeira reproduziu AC-01…AC-10 e AC-12 e apontou defeitos em `sddtask.py evidence`, nos checks e no AC-09; a segunda revisou as correções e os 8 arquivos com pin renovado. As observações acima foram refeitas pela raiz depois das correções, sobre os mesmos comandos.

## 9. Fechamento

- Documentação: `README.md`, `application/README.md`, `DESIGN.md`, `docs/README.md`, `docs/architecture/{application,context,contracts}.md`, `docs/design/{ide-shell,surfaces,windows-apps-analysis,reference-coverage}.md`, `docs/security/trust-boundaries.md`, `docs/licensing/{review,dependency-policy-20261109}.md`, `docs/assets/README.md`, `scripts/README.md`, `scripts/security/SOURCES.md`, ADRs mantidos de `docs/decisions/` → atualizados (links para specs, fatos dos relatórios removidos escritos no texto); `docs/development/local-artifacts.md` → sem impacto: não cita o legado
- `sdd/project.md`: atualizado (escopo vigente, estado das capacidades pelas specs, comandos)
- Inputs da seção 8 alterados no fechamento: nenhum; 9.1–9.2 concluídos antes da observação final
- Checks de governança: `validate.py --root .` exit 0; `run-tests.py` exit 0 (234 testes); `check-ox.py` exit 0
- Pendências: (1) verificação completa via Toolbox não rodou (não autorizada) → rodar com o comando de `AGENTS.md`; Ruff/Bandit não estão instalados localmente, então os 8 pins renovados foram revisados por leitura independente, sem saída de scanner. (2) Entrada B110 obsoleta de `sdd/tools/validate.py` no baseline do Bandit e ignore `I001` com comentário obsoleto em `ruff.toml` → limpar numa task com revisão de política. (3) `check-ox.py` ignora symlinks em silêncio (herdado de antes desta task; HEAD reportava "Symlink not portable") e não tem mais as checagens de POL/GOV duplicadas em AGENTS e de recursos copiados (também removidas antes desta task) → reavaliar numa task de governança. (4) O diagrama `docs/assets/documentation.svg` ainda mostra o nó "governança e cópia" → regenerar com `render.mjs` (exige baixar ferramentas, não autorizado). (5) Input de saída derivada com hash de 64 hex fica `unverifiable` e não é problema; o oráculo depende de o comando estar registrado. (6) Nada foi colocado em stage nem commitado; o índice do Git ainda contém renames antigos para `sdd/history/`, anteriores a esta task.
- Estado final: concluída

## Revisão r2 — 2026-11-24 — Resposta à revisão externa

Motivo: a [revisão externa](SDD-ENXUTO-20261123.review.md), colada pelo usuário em 2026-11-24,
recomenda reabrir a task antes do commit. Achados: (1) o AC-08 deixou passar referências a
arquivos removidos; (2) o aceite depende de logs em `.local/`, ignorado pelo Git; (3) o validador
lê as tabelas das etapas 4 e 5 só da seção original. Ajuste de encaminhamento: o rótulo
"governança e cópia" continua nas fontes Mermaid. O escopo da task não muda (SDD centralizado e
legado removido); a correção é do mesmo escopo, por isso é revisão e não task nova.

### 1. Prompt

Pedido: o texto da revisão externa, cujo pedido explícito é "eu reabriria a task antes do commit",
e a resposta do usuário à Q-5. Objetivo: corrigir os três achados e o rótulo do diagrama.

Restrições adicionais às da seção 1.3, que continuam valendo:
- NÃO alterar o índice do Git: os 330 renomes e as 51 exclusões já preparados não são desta revisão.
- NÃO baixar ferramentas para regenerar o SVG; o texto do SVG é editado e conferido por render local.
- NÃO editar as linhas originais das seções 1–9; só os metadados `Revisão atual` e `Estado`.
- NÃO adicionar ocorrência nova ao baseline do Bandit (script de AC sem `subprocess`).

Critérios revisados e novos (por ID vale esta revisão):

- AC-08: nenhum arquivo ativo referencia o legado por termo, por caminho removido (de HEAD ou de `removed-paths.txt`, em texto, código inline ou link) ou por nome de arquivo que existia em um único caminho de HEAD, removido | método: `bash sdd/tasks/SDD-ENXUTO-20261123/ac08_refs.sh` (exclusões e permissões com motivo em `EXCLUDE` e `ALLOWED` de `ac08_refs.py`; histórico citado como `<commit>:<caminho>` não conta) | esperado: exit 0, `ocorrencias=0`
- AC-13: o aceite das tasks é conferível sem `.local/` | método: `bash sdd/tasks/SDD-ENXUTO-20261123/ac13_clean_copy.sh` (copia os arquivos ativos para um diretório temporário sem os ignorados e roda `validate.py --root .` e `evidence --check --require-all` de cada task) | esperado: exit 0, `tasks=2 falhas=0 local_copiado=0`
- AC-14: as tabelas das etapas 4 e 5 seguem a revisão mais recente por ID, e ID repetido na mesma camada, linha sem ID e tabela de cabeçalho desconhecido são reprovados | método: `python3 -m unittest discover -s sdd/tools/tests -k test_revision_tables -k test_duplicate_id_in_same_layer -k test_rejects_unrecognized_or_split_stage_tables -v` e, numa cópia, `Task.table` lendo só a seção original | esperado: exit 0 com 4 testes OK; com a mutação, os 4 falham, entre eles os 2 `test_revision_tables`
- AC-15: o rótulo "governança e cópia" sai do diagrama de navegação | método: `grep -c "governança e cópia" docs/assets/diagrams/documentation.mmd docs/README.md docs/assets/documentation.svg`; `python3 docs/assets/check.py`; render do SVG no Firefox headless | esperado: 0 nos três arquivos; `0 failures`; rótulo novo dentro do nó
- AC-16: o validador reprova input citado em `.local/` | método: `python3 -m unittest discover -s sdd/tools/tests -k local_dir -v` | esperado: exit 0, 1 teste OK que cobre task aberta, task concluída e o caso aceito com o log em `sdd/tasks/<ID>/`

### 2. Esclarecimentos

| Q | Pergunta | Resposta do usuário | AC/etapa afetados |
|---|---|---|---|
| Q-5 | Os logs citados na seção 8 ficam em `.local/`, que o Git ignora; qual regra de retenção adotar? | "Versionar em sdd/tasks/<ID>/ (Recomendado)" | AC-11, AC-13, AC-16 |

### 3. Especificação

- REQ-07: a evidência citada na seção 8 é versionada e o aceite é conferível em outro checkout.
- AC-13 → REQ-07
- AC-16 → REQ-07
- AC-14 → REQ-03
- AC-15 → REQ-05

### 4. Plano

| Decisão | REQ | Escolha | Alternativa descartada e motivo |
|---|---|---|---|
| D-07 | REQ-05 | AC-08 por caminho: todo caminho de HEAD ou de `removed-paths.txt` ausente do working tree, em qualquer token com `/`, relativo à raiz ou ao arquivo; histórico citado como `<commit>:<caminho>` | Acrescentar termos ao padrão antigo: continua omitindo o que não foi listado, que é o achado 1 |
| D-08 | REQ-03 | `Task.table` aplica as revisões por ID, na posição original; ID repetido na mesma camada mantém as duas linhas | Proibir revisão das etapas 4 e 5: contradiz a regra "por ID vale a revisão mais recente" |
| D-09 | REQ-07 | Log citado é versionado em `sdd/tasks/<ID>/` (até 1 MiB); `validate.py` reprova input em `.local/`; as duas tasks reobservam os ACs com logs versionados | Reexecutar em outro checkout: o aceite deixa de ser conferível por bytes; documentar a dependência: a fragilidade continua (Q-5) |
| D-10 | REQ-05 | Trocar o rótulo nas duas fontes Mermaid e no texto do SVG | Regenerar com `render.mjs`: exige baixar o Mermaid, não autorizado |

| SKILL.md | Motivo | Contribuição |
|---|---|---|
| `.codex/skills/prompt/SKILL.md` | Etapas 1–2 da revisão | Avaliação independente da revisão recebida antes de aceitá-la; critério de conclusão explícito |
| `.codex/skills/software-testing/SKILL.md` | AC-14 e AC-16 | Oráculo independente (o caso do revisor); teste que detecta o defeito original, conferido por mutação |
| `.codex/skills/technical-documentation/SKILL.md` | README, ADRs e diagrama | Rotas obsoletas removidas; visual alterado renderizado e inspecionado |

### 5. Itens de trabalho

| Item | D | Arquivos (dono) | Depende de | Teste | Pronto quando | Skill |
|---|---|---|---|---|---|---|
| T-08 | D-07 | `sdd/tasks/SDD-ENXUTO-20261123/ac08_refs.{py,sh}`, `application/README.md`, `docs/decisions/{scripts-toolbox-native,scripts-task-closure,f0-boundary-20261102,local-persistence-experiment-20261105,licensing}.md`, `docs/design/ide-shell.md`, `docs/licensing/{review.md,license-source.json}`, `sdd/specs/bootstrap.md` | — | AC-08 | `ocorrencias=0` e referência plantada detectada | `technical-documentation` |
| T-09 | D-08 | `sdd/tools/sddtask.py`, `sdd/tools/tests/test_validate.py` | — | AC-14 | testes passam e falham com a mutação | `software-testing` |
| T-10 | D-09 | `.gitignore`, `sdd/workflow.md`, `sdd/templates/task.md`, `sdd/tools/validate.py`, `sdd/tools/tests/test_validate.py`, `docs/development/local-artifacts.md`, `.claude/skills/codex-task-audit/references/ox-governance.md`, `ac13_clean_copy.sh`, evidência r2 das duas tasks | T-09 | AC-13, AC-16 | cópia sem `.local/` passa | `software-testing` |
| T-11 | D-10 | `docs/assets/diagrams/documentation.mmd`, `docs/README.md`, `docs/assets/documentation.svg` | — | AC-15 | rótulo trocado e render inspecionado | `technical-documentation` |

### 7. Execução

| Item | Arquivos alterados | Teste executado | Exit | Observação |
|---|---|---|---|---|
| T-08 | os do item | `ac08_refs.sh`; arquivo de sonda com 4 referências | 0 (`ocorrencias=0`); 1 (3 detectadas, a ref `ea3cf0f:` ignorada) | Primeira execução: 11 ocorrências, 8 reais e 3 falsos positivos (ver abaixo) |
| T-09 | os do item | `unittest -s sdd/tools/tests`; mutação em cópia | 0; 1 (2 FAIL) | O caso do revisor (D-01 ligado ao REQ errado numa r2) agora falha |
| T-10 | os do item | `check-ox.py`; `ac13_clean_copy.sh` antes da reobservação | 1 (inputs em `.local/`); 1 (`falhas=3`) | Reproduz o achado 2 antes da correção da evidência |
| T-11 | os do item | `docs/assets/check.py`; Firefox 145 headless `--screenshot` | 0; 0 | Rótulo "Desenvolvimento · verificar e manter" em 2 linhas no nó de 280×94 |

Falhas e tentativas abandonadas:
- Primeira versão de `ac08_refs.py` chamava `git` por `subprocess`; o scan Bandit compara com
  baseline e acusaria B404/B603/B607 novos. As listas do Git passaram para `ac08_refs.sh`.
- Falsos positivos da primeira execução, tratados com motivo no cabeçalho do script: caminhos de
  arquivos zip externos na tabela de fontes da skill `readme-lifecycle-engineering`; o termo
  "procedimento canônico" em `scripts/README.md` (descreve o shared-toolbox; o script anterior só
  buscava o termo em `.codex/`); a linha `"reason"` de `automation.json`, registro de revisões.
- Um teste novo usava `\n` dentro de expressão de f-string, sintaxe inválida no Python 3.11
  declarado pelo projeto; corrigido. Só há Python 3.13 nesta máquina: a compatibilidade com 3.11
  não foi executada.
- `sddtask.py` tinha `nº`; trocado por "número" junto com o texto novo, por precaução com a regra
  de caracteres ambíguos do Ruff (RUF002), que não está instalado aqui.

Verificação independente, rodada 1 (contexto novo, sem o histórico desta sessão): REJECTED, com
11 defeitos; pins de `validate.py` e `test_validate.py` aprovados. Correções:
- D1 (alta): `.gitignore:13` (`*.log`) ignorava também `sdd/tasks/<ID>/*.log`, o que anularia a
  D-09. Acrescentada a exceção `!/sdd/tasks/**/*.log`; `git status` passa a mostrar os logs.
- D2 (alta): a busca por nome usava a lista do índice, que inclui 17.840 arquivos apagados do
  disco, e ficava neutralizada. Ativo passou a ser o que existe. A busca por nome ficou restrita a
  nomes de um único caminho de HEAD: em 89 ocorrências, os nomes de vários caminhos
  (`result.txt` ×18, `request.txt` ×13…) eram saídas geradas ou nomes genéricos. Revisão manual
  desses: `sdd/specs/bootstrap.md:30` (`plan.md`) era referência real e foi corrigida;
  `application/crates/ox-ui/src/desktop/views.rs:1221-1222` descreve `plan.md`/`tasks.md`/
  `evidence.json` do modelo anterior, mas é código Rust de produto (pendência); os demais são
  nomes de saída de scripts e testes ou nomes genéricos da skill `commit-governance`.
  Referências reais achadas pela busca corrigida: `f0-boundary-20261102.md:12`,
  `local-persistence-experiment-20261105.md:12` e `license-source.json` em `licensing.md:10` e
  `docs/licensing/review.md:42`. Esse ledger (URL, método e SHA-256 do texto GPL de `LICENSE`)
  não tinha sido migrado no r1, uma perda de dado técnico (REQ-04); foi restaurado byte a byte
  de `HEAD:docs/validation/maintenance-001/license-source.json` para `docs/licensing/`.
- D3: cada exclusão e permissão tem motivo no script; a skill readme-lifecycle saiu da exclusão
  de arquivo inteiro e só a tabela de fontes (`| E0n |`) é permitida.
- D4: `local_input` passou a ler `.local/` na célula em qualquer forma (inclusive texto e
  `` `caminho` (log) ``), não só o caminho resolvido.
- D5 e D7: `Task.table` lê todas as tabelas com o cabeçalho em cada camada; o validador reprova
  ID repetido na mesma camada, linha sem ID e tabela de etapa 4 ou 5 com cabeçalho desconhecido.
- D6: o teste de ID repetido põe a linha errada primeiro; formas `sdd/../.local`, link
  `../../.local`, `` `…` (log) `` e texto entraram no teste de `.local/`.
- D8: o método do AC-14 selecionava 4 testes contra 3 esperados; nomes completos no `-k` e
  esperado ajustado (o critério ainda não tinha observação).
- D9: a lista de pendências visuais do README cita a fonte real
  (`ea3cf0f:docs/validation/visual-integration-20261111/report.md`), não a spec; a frase sobre
  comando gráfico agora ressalva a suíte X11.
- D10: listas do Git com `-z`; token com `/` inicial ou prefixo `x:` é examinado; URL e barra
  invertida ficam fora, com motivo no cabeçalho.
- D11: `scripts-toolbox-native.md` cita a feature como `ea3cf0f:`; `local-artifacts.md` com a
  ordem original das frases e a retenção de `.local/tasks/` declarada (descartável, fora da rotação
  de `scripts/lib/logs.sh`, que só trata `.local/logs`).
- Mutantes M4 (sem guarda `in_layer`) e M6/M8 sobrevivem e são equivalentes no veredito: o ID
  repetido, a falta de coluna e o input fora da raiz já reprovam por outra mensagem.

Verificação independente, rodada 2: D1–D7 e D9–D11 APPROVED; pin de `test_validate.py`
aprovado; pin de `validate.py` REJECTED. Correções:
- N1: `validate.py` tinha travessão curto (U+2013) em 3 linhas (docstring e comentários; uma era
  nova), que a regra RUF002/RUF003 aponta; o histórico do pin já registrava essa troca. Trocado por
  hífen. O verificador registrou que também tinha aprovado duas dessas linhas na rodada 1.
- N2: a correção de `sdd/specs/bootstrap.md:30` apontava o `plan.md` de product-plugin-host; o
  texto original se referia ao `plan.md` (D-08) e ao `tasks.md` (T011) da própria feature
  bootstrap. Corrigido para `ea3cf0f:sdd/features/product-bootstrap/{plan,tasks}.md`.
- D8: a mutação do AC-14 derruba 4 testes, não 2; esperado ajustado antes da observação.
- N3: o ramo `resolve()` de `local_input` não tinha teste (mutante sobrevivia); acrescentado o caso
  de diretório de task que é symlink para `.local/`; o mutante agora falha em 2 subtestes.

### 8. Validação

#### Estado na reabertura (obsoletas)

Na reabertura, todo AC volta a UNVERIFIED até a nova observação: os logs citados estão em `.local/` (achado 2) ou o critério mudou (AC-08).

| AC | Critério (SHA-256) | Método executado | Inputs | Resultado observado | Estado |
|---|---|---|---|---|---|
| AC-01 | — | — | — | aguarda observação r2 | UNVERIFIED |
| AC-02 | — | — | — | aguarda observação r2 | UNVERIFIED |
| AC-03 | — | — | — | aguarda observação r2 | UNVERIFIED |
| AC-04 | — | — | — | aguarda observação r2 | UNVERIFIED |
| AC-05 | — | — | — | aguarda observação r2 | UNVERIFIED |
| AC-06 | — | — | — | aguarda observação r2 | UNVERIFIED |
| AC-07 | — | — | — | aguarda observação r2 | UNVERIFIED |
| AC-08 | — | — | — | aguarda observação r2 | UNVERIFIED |
| AC-09 | — | — | — | aguarda observação r2 | UNVERIFIED |
| AC-10 | — | — | — | aguarda observação r2 | UNVERIFIED |
| AC-11 | — | — | — | aguarda observação r2 | UNVERIFIED |
| AC-12 | — | — | — | aguarda observação r2 | UNVERIFIED |
| AC-13 | — | — | — | aguarda observação r2 | UNVERIFIED |
| AC-14 | — | — | — | aguarda observação r2 | UNVERIFIED |
| AC-15 | — | — | — | aguarda observação r2 | UNVERIFIED |
| AC-16 | — | — | — | aguarda observação r2 | UNVERIFIED |

#### Observação r2

Observação do verificador independente (contexto novo, rodadas 3 e 4), que devolveu as linhas sem
hashes; logs versionados em `sdd/tasks/<ID>/r2/`. O escritor do registro atribuiu os IDs `I-n`, gravou
os hashes com `sddtask.py evidence --write` e rodou os ACs que conferem o próprio registro.

| Input | Caminho ou saída | Papel | SHA-256 |
|---|---|---|---|
| I-50 | `sdd/workflow.md` | material | `c3808582075f83a4b46bf08c3958a6a700d136a6fa31da3631b20b63230d6652` |
| I-51 | `sdd/constitution.md` | material | `ac86e4dc1f9af10da34c5bca1c53dce8a4d7f7a952b432f7f16bfe0bd64947d6` |
| I-52 | `sdd/project.md` | material | `ae1e1881e030ba421b53784a6f738f26e884c2c85221308dba4c3ae97d1c1e57` |
| I-53 | `sdd/tools/validate.py` | oráculo | `3908e9d5371cf52a90f8e43846647498e6af9ed9ed41d6d47162da61a243e503` |
| I-54 | `sdd/tasks/SDD-ENXUTO-20261123/r2/ac01.log` | material | `a47f636fad650722d7c96ba8768ac2d3c4a303a4a362af8a1e885e7ab9260e00` |
| I-55 | `sdd/tools/sddtask.py` | material | `9e30d1c8df59c68f44c3f8ff7b47e6a572f020073270860fa6575800c9fd3224` |
| I-56 | `sdd/tools/tests/test_sddtask.py` | oráculo | `9e3453f89113ee32db60a7e2655df7d3c675a051386cbc8e8db5572714a10e7c` |
| I-57 | `sdd/tools/tests/test_validate.py` | oráculo | `b3e4247d7772e06669535d88e4de0928d78b373f0b805ea4de8516f691dd6ecf` |
| I-58 | `sdd/tasks/SDD-ENXUTO-20261123/r2/ac02.log` | material | `91f211a49518f131b70cc6e57ba188271da2cb3fb8ac8cd6b57ff587f9955883` |
| I-59 | `tools/governance/scripts/governance_support.py` | material | `3b104bff72c0a367b0893b512d42d8ff7027f292b131b401b208fe88812fd058` |
| I-60 | `tools/governance/scripts/check-ox.py` | oráculo | `a7dfbe0d7571dbde89626a6fe867ddff905ee4dad71f313d86563e9f27bd6604` |
| I-61 | `sdd/tasks/SDD-ENXUTO-20261123/r2/ac03.log` | material | `f2baac5711d3ed677085444739c418258fc874fc59039628aded99e8445faed4` |
| I-62 | `tools/governance/scripts/run-tests.py` | oráculo | `cc6d9abfa079238390232253f7b6f839b100fa62eedeadd82a29241daaec2df0` |
| I-63 | `tools/governance/tests/test_check_ox.py` | oráculo | `f8ac80490ef370e62d212e1a9f1f142a7e758bc3d1ef3d379c312975e268bf3f` |
| I-64 | `tools/governance/tests/test_instruction_routes.py` | oráculo | `0cf2ef1bb4918dd46e77b0fc1e19a1252d3f62a75dc82beb041483f2681eb503` |
| I-65 | `sdd/tasks/SDD-ENXUTO-20261123/r2/ac04.log` | material | `856ade2959b107a6ca3b7096ff4563eac3a9ff2cc6bc71cb2135fa217f873037` |
| I-66 | `scripts/config/automation.json` | configuração | `989f268b634b394ea25200d796ada3edaa6ec3ed66b90e62a3f31376df1172ed` |
| I-67 | `sdd/tasks/SDD-ENXUTO-20261123/r2/ac05.log` | material | `09761219f695fd2715a47835f15704e1e3ed18f5921171fa9b203081225ebd81` |
| I-68 | `.claude/skills/codex-task-audit/scripts/task_inventory.py` | material | `381fa4142f920304b1abfedfe46407be865b5d4ef2a4e67f42db87a4f2a8a010` |
| I-69 | `.claude/skills/codex-task-audit/scripts/test_scripts.py` | oráculo | `62f35bdb39dddde5877e587c5310d38422e9b7ddbc2663f00de83f919dc881c9` |
| I-70 | `sdd/tasks/SDD-ENXUTO-20261123/r2/ac06.log` | material | `2dd5831622680032d16c1859cf54414ca53d67b5bd4402ff0226a2dd4abc4adc` |
| I-71 | `.codex/config.toml` | material | `3373184901ce9b92473745e280a2dff6e436260c1e341377e21676099e3524f7` |
| I-72 | `.codex/agents/ec_implementador.toml` | material | `c76ca3b940b25758b323a9970ee30792dc0c7ae0e3e7c1dbd4c21350de652f2b` |
| I-73 | `.codex/agents/ec_implementador_extra_alto.toml` | material | `ca64eaa6ec6ddbacb21af9b7a30cd09b09772460afd34f98f6f1838fbde29f11` |
| I-74 | `.codex/agents/ec_orquestrador_alta.toml` | material | `3a2e31366e1f5a5d44c25e08df8bd9c85d4287adbaeb7e89f2cc5e90cf7f931d` |
| I-75 | `.codex/agents/ec_orquestrador_normal.toml` | material | `f10d3e3642d18ef1a4cae2a08b5d7899e00fcdc7319208d7f4b3fd0b12f0f601` |
| I-76 | `.codex/agents/ec_planejador.toml` | material | `e8091a9dc41c34a50d994989190051bd9758334d707e19df71ad70487ab94668` |
| I-77 | `.codex/agents/ec_verificador.toml` | material | `8449e20054ea1df0b94441836abd5aa1e2b506c05564af274f7de78d643c1320` |
| I-78 | `sdd/tasks/SDD-ENXUTO-20261123/ac07_agents.py` | oráculo | `c1012419a54fe22640163e91cee558320cd4c7efb79c286c9fdc2f64362d82a1` |
| I-79 | `sdd/tasks/SDD-ENXUTO-20261123/r2/ac07.log` | material | `477bafa7f3c3b1e4330bad5a27f31de7d8bb570100bcd0d0c165fdcd3201374e` |
| I-80 | `sdd/tasks/SDD-ENXUTO-20261123/ac08_refs.sh` | oráculo | `46e4579c852937544acd549d458c4050896a6819e796ce8ece600c5f267e41ef` |
| I-81 | `sdd/tasks/SDD-ENXUTO-20261123/ac08_refs.py` | oráculo | `ae1cc1032c2b07a04fbce8a8d18b9f39f65d50b4b771e5bf92302a75149db50e` |
| I-82 | `sdd/tasks/SDD-ENXUTO-20261123/removed-paths.txt` | configuração | `73f6803b0a3192264276d21747a945e1ee6ccbc60cd9e4eed8bd7a34ab593fe0` |
| I-83 | `sdd/tasks/SDD-ENXUTO-20261123/r2/ac08.log` | material | `16382f77fdcaf4d6e3efb3d30b825d313d52254198f5e1ea5e41d38d70dfa1ca` |
| I-84 | `sdd/tasks/SDD-ENXUTO-20261123/removed-paths.txt` | material | `73f6803b0a3192264276d21747a945e1ee6ccbc60cd9e4eed8bd7a34ab593fe0` |
| I-85 | `sdd/tasks/SDD-ENXUTO-20261123/r2/ac09.log` | material | `fc4922d3b9f5ea5fd087e7f3419a4874ab288ec94da9c0c2f8e3a0ea519f8bbd` |
| I-86 | `sdd/specs/README.md` | material | `d1b27f89c2b4d5f538defe917fff29c5337f9f7b8a48222f11657d8f3726ee49` |
| I-87 | `sdd/specs/agent-runtime.md` | material | `b33edff053454d9a405f5cdd66c5d11f600a428313db205da046d25976c05d98` |
| I-88 | `sdd/specs/bootstrap.md` | material | `7bf4e6ed3f15ac423d2966a5426c5b32651aaabfc8eaabed3897c5459332b6a7` |
| I-89 | `sdd/specs/f0-gate.md` | material | `2d3cc73ddc98efafda6290351dcd9c49d2dda347f41b314290d5fa233a4e1965` |
| I-90 | `sdd/specs/foundation.md` | material | `b59a488d343c97e64bd753c3b31a78dd40eb2fb91a2cc9d5b97849dccb465868` |
| I-91 | `sdd/specs/ide-shell.md` | material | `2a1b18917e039ccb9951719e8e89d67f78c222958f371bfc10d46a562078f555` |
| I-92 | `sdd/specs/local-persistence.md` | material | `133e5e4822dcbb606fe6e5d655c427cafc8ca273ae1423a3d2446c08d132cb0d` |
| I-93 | `sdd/specs/local-task-ui.md` | material | `0f76671ff4e8600de2696db4dafdede264aeca8047893607ba113ebe67c044b8` |
| I-94 | `sdd/specs/plugin-host.md` | material | `d68ed7e2c12ce9794072bf3cc1900c9e289f9f69a8b2d533eba7aedc20e2ff58` |
| I-95 | `sdd/specs/verification-engine.md` | material | `3f279b5894a3e7e1a604df0db241528b479063a04c046ab22d3deae79f5a2bf8` |
| I-96 | `sdd/specs/visual-workbench.md` | material | `cde4695813a9e00f9612d41998eeeca8470f11508cf645dd7d119277b9e21569` |
| I-97 | `sdd/tasks/SDD-ENXUTO-20261123/r2/ac10.log` | material | `bfc390c7e88b22f0990f6ec87868911846e0a4b044a44097aab11e7455c1fbe0` |
| I-98 | `AGENTS.md` | material | `dd53cb5f25f71bf3c6e1f72042a7a3628f67e50495b4b15c328ff5ec78158be0` |
| I-99 | `.codex/skills/prompt/SKILL.md` | material | `98bb62af25b1e62dda471c3ba032c73f45283af96400404db71224afdb3c05d5` |
| I-100 | `sdd/tasks/SDD-ENXUTO-20261123/r2/ac12.log` | material | `7b3c16a4d2fa92b888ee9bc199556ab02893ffd102959e49965df4c40c6e361e` |
| I-101 | `sdd/tools/validate.py` | material | `3908e9d5371cf52a90f8e43846647498e6af9ed9ed41d6d47162da61a243e503` |
| I-102 | `.gitignore` | configuração | `62bce61df7464353624b3e0db763751318e41edcaa69c0a94b10946162d799d9` |
| I-103 | `sdd/tasks/SDD-ENXUTO-20261123/ac13_clean_copy.sh` | oráculo | `3ff9ab28fbd15f621204493593d961ef953461113c5b5dfd4d67c518bdf9596f` |
| I-104 | `sdd/tasks/SDD-ENXUTO-20261123/r2/ac14.log` | material | `be858654cd27fd5d725c03894fa4555c530656bc6ef513896c8ea2f9762d92a4` |
| I-105 | `docs/assets/diagrams/documentation.mmd` | material | `2fc9eb0814394ad1ab134588bb9f2cfc14c69c85a2f295d002e7d24a5b6e21cf` |
| I-106 | `docs/README.md` | material | `e7eab63009c8f51fd04a4cd71dae602f4832e0b816a1b4cab83d457e70a37cb9` |
| I-107 | `docs/assets/documentation.svg` | material | `6c82cc822195b08a71c3ae928ac78d02149f17cb18604ee98cc2bbd009e47031` |
| I-108 | `docs/assets/check.py` | oráculo | `492c55f947af9bc21cf22eeb1fe9d2d3086b11c0fb87c5b7d88ba941153a5d95` |
| I-109 | `sdd/tasks/SDD-ENXUTO-20261123/r2/ac15.log` | material | `e6697cfaab0232a13b1b6101884a282da4ad18cd72d688f63e945334dc76d00b` |
| I-110 | `sdd/tasks/SDD-ENXUTO-20261123/r2/ac15-documentation.png` | material | `c1b6ae4a174b91529353110a64446e831b952a80ad3395fb11c136eda12d8144` |
| I-111 | `sdd/tasks/SDD-ENXUTO-20261123/r2/ac16.log` | material | `1ff508de0ab61e594033779d605003116460f09701593033d971e26934cd149a` |

| AC | Critério (SHA-256) | Método executado | Inputs | Resultado observado | Estado |
|---|---|---|---|---|---|
| AC-01 | `976460c5db8915d8a26fabae631fb2e0dcb82c8885e721d506836e13a93d3009` | `python3 sdd/tools/validate.py --root .` | I-50, I-51, I-52, I-53, I-54 | exit 0; `PASS: estrutura, 2 task(s), 10 spec(s)` | APPROVED |
| AC-02 | `e38241e576702fd076f0b7173afce3cfdf4ca0a30ed11b75f2d48ca3ff13a02a` | `python3 -m unittest discover -s sdd/tools/tests` (mais `-v` complementar, para os nomes) | I-55, I-53, I-56, I-57, I-58 | exit 0; 69 testes OK; 11 de `EvidenceCommandTests`; matriz: `test_matrix_is_derived_from_sections_3_to_5` e `test_rejects_req_whose_criteria_no_item_tests` (órfão) | APPROVED |
| AC-03 | `2beadd2d209c3063b5a20d2d15e9384f32720268927730bf7a86856bc08c3cbf` | `python3 tools/governance/scripts/check-ox.py` | I-50, I-51, I-52, I-59, I-60, I-61 | exit 0; `PASS: SDD, normative IDs, skill map, local links and external-content inspection` | APPROVED |
| AC-04 | `a0a0ecb4b4ff7e1aab6cabd430190638c01fe1ae391f47765256a2cf257f88ee` | `python3 tools/governance/scripts/run-tests.py` | I-60, I-59, I-62, I-63, I-64, I-65 | exit 0; 246 testes, `OK (skipped=1)`; o pulado é `test_native_scans` (exige Docker e imagens centrais) | APPROVED |
| AC-05 | `4ccd98b2c08036983a837a292f6e73613b919175db77cfa916722c9311a0d694` | `python3 -m unittest discover -s scripts/tests` (reobservado depois da renovação dos pins) | I-66, I-67; sem oráculo separado: a suíte `scripts/tests` inteira é o oráculo | exit 0; 139 testes, `OK (skipped=1)` | APPROVED |
| AC-06 | `3f5cb04f17bccd467b8294c3cb23d06edd84ab31b726d391af068d57d386158b` | `python3 -m unittest discover -s .claude/skills/codex-task-audit/scripts` | I-68, I-69, I-70 | exit 0; 14 testes OK | APPROVED |
| AC-07 | `7bc6848013db06b1f23bfea23678f05faec36ed3ca3319093682d9c789d6ba5f` | `python3 sdd/tasks/SDD-ENXUTO-20261123/ac07_agents.py` | I-71, I-72, I-73, I-74, I-75, I-76, I-77, I-50, I-78, I-79 | exit 0; `perfis=6 carregados=7 ancoras_ausentes=0` | APPROVED |
| AC-08 | `886827f431fc2a303d4d66abfd1f0de44418b8b9f16862f2c7356addf49289c2` | `bash sdd/tasks/SDD-ENXUTO-20261123/ac08_refs.sh` (reobservado depois da renovação dos pins) | I-66, I-80, I-81, I-82, I-83 | exit 0; `ocorrencias=0 ativos=602 removidos=23066`; sondas do verificador (caminho completo, relativo ao subdiretório, `/` inicial, prefixo `x:`, nome solto, `.rs`) detectadas; `ea3cf0f:…` e URL ignorados, como declarado | APPROVED |
| AC-09 | `edf1e569dfe03576bd2a40200510f5ca2499e48bb39e9129b25297a740d5755a` | `test -e` por linha de `removed-paths.txt` (laço no log) | I-84, I-85; sem oráculo separado: `test -e` do shell decide a existência | exit 0; `caminhos=53 existentes=0` | APPROVED |
| AC-10 | `067c8a92d7df97b61770d1d7551d89c27cecb342b34ad136d9a3fdeb31f4b76c` | `ls sdd/specs/*.md`; `grep -c "^## Estado atual" sdd/specs/*.md`; `python3 sdd/tools/validate.py --root .` | I-86, I-87, I-88, I-89, I-90, I-91, I-92, I-93, I-94, I-95, I-96, I-53, I-97 | exit 0; 10 specs além do README, cada uma com 1 `## Estado atual`; validate PASS com 10 specs | APPROVED |
| AC-11 | `b8bdc4f0649d2bbab59ee346933b4b761d1bc8d0e0df7e9fab3ef2a762145ba6` | `python3 sdd/tools/sddtask.py evidence --task SDD-ENXUTO-20261123 --check --require-all` (pelo escritor do registro, depois do `--write`) | I-55, I-56 | exit 0; `0 problema(s) em 127 verificação(ões)` (16 critérios e os inputs vigentes) | APPROVED |
| AC-12 | `cb4e2b764bf57dea1e90fafdb7f859eac431ae468c17ecf8a9da96e75dbadeca` | `wc -w AGENTS.md sdd/constitution.md sdd/project.md sdd/workflow.md .codex/skills/prompt/SKILL.md` | I-98, I-50, I-51, I-52, I-99, I-100; sem oráculo separado: `wc -w` e o limite do critério | exit 0; 222 + 966 + 317 + 2593 + 1533 = 5631 ≤ 5635 | APPROVED |
| AC-13 | `4ed52e93a1e91fa07ad9c24f28970f5f0cfd38937ff0ad09f4a26cb9c146fc72` | `bash sdd/tasks/SDD-ENXUTO-20261123/ac13_clean_copy.sh` (pelo escritor do registro, depois do `--write`) | I-55, I-101, I-102, I-103 | exit 0; `tasks=2 falhas=0 local_copiado=0`; antes da reobservação, o mesmo script deu `falhas=3` (reproduz o achado 2) | APPROVED |
| AC-14 | `bedba4618dd9f1a66522853b2202ed46b92fe0ae0cf02e83f3d2903ac417296b` | `python3 -m unittest discover -s sdd/tools/tests -k test_revision_tables -k test_duplicate_id_in_same_layer -k test_rejects_unrecognized_or_split_stage_tables -v`; mutação em cópia (`Task.table` só com a seção original, diff no log) | I-55, I-101, I-57, I-104 | real: exit 0, 4 testes OK; mutação: exit 1, `FAILED (failures=4)`, inclusive os 2 `test_revision_tables` | APPROVED |
| AC-15 | `bca4a894b2445e81f89431fb47083c3f585c492b8b9720511d8eca4b96439294` | `grep -c "governança e cópia"` nos 3 arquivos; `python3 docs/assets/check.py`; Firefox headless `--screenshot` do SVG e inspeção do PNG | I-105, I-106, I-107, I-108, I-109, I-110 | exit 0; 0 nos três arquivos; `212 local targets/anchors, 9 SVGs; 0 failures`; PNG 920×512 com "Desenvolvimento ·" / "verificar e manter" em 2 linhas dentro do nó, sem corte | APPROVED |
| AC-16 | `6dd6ad0e2e4bfaf2bef3f8354a5d697bed739929ed448ec554a2f6c87ab25310` | `python3 -m unittest discover -s sdd/tools/tests -k local_dir -v` | I-101, I-57, I-111 | exit 0; 1 teste OK (`test_rejects_input_kept_in_local_dir`: task aberta e concluída, formas de célula, diretório symlink e o caso aceito em `sdd/tasks/<ID>/`) | APPROVED |

### 9. Fechamento

- Documentação: `application/README.md`, `docs/README.md`, `docs/assets/{documentation.svg,diagrams/documentation.mmd}`, `docs/decisions/{scripts-toolbox-native,scripts-task-closure,f0-boundary-20261102,local-persistence-experiment-20261105,licensing}.md`, `docs/design/ide-shell.md`, `docs/development/local-artifacts.md`, `docs/licensing/{review.md,license-source.json}`, `sdd/specs/bootstrap.md`, `sdd/workflow.md` (Evidência), `sdd/templates/task.md`, `.claude/skills/codex-task-audit/references/ox-governance.md`, `.gitignore` → atualizados
- `sdd/project.md`: sem mudança (escopo vigente, capacidades e comandos continuam corretos)
- Inputs da seção 8 alterados no fechamento: nenhum (`evidence --check --require-all` exit 0, 127 verificações; cópia sem `.local/` exit 0)
- Checks de governança: `validate.py --root .` exit 0; `check-ox.py` exit 0; `run-tests.py` exit 0 (246 testes, 1 skip); `scripts/tests` exit 0 (139, 1 skip); suíte do SDD exit 0 (69)
- Pendências: (1) verificação completa via Toolbox não rodou (não autorizada); Ruff e Bandit não estão instalados, então os pins de `validate.py` e `test_validate.py` foram renovados por revisão independente, sem scanner; a compatibilidade com Python 3.11 foi conferida só por `ast` com `feature_version=(3,11)`. (2) `application/vendor/cryoglyph-0.1.0/OX-PATCH.md:37` cita `docs/validation/`; vendor é protegido pela seção 1.3 → corrigir numa task que autorize vendor. (3) `application/crates/ox-ui/src/desktop/views.rs:1221-1222` descreve `plan.md`/`tasks.md`/`evidence.json` do modelo anterior; código Rust de produto, fora do escopo → task de produto. (4) O texto do SVG foi editado à mão; regenerar com `render.mjs` quando o download das ferramentas for autorizado (fonte e SVG já concordam). (5) A busca por nome do AC-08 cobre só nomes únicos em HEAD; os genéricos foram revistos uma vez (seção 7). O `validate.py` reprova input em `.local/`, mas não em outros diretórios ignorados (`.cache/`) citados como saída derivada, nem reconhece `### 4 Plano` sem ponto como etapa. (6) Nada foi colocado em stage nem commitado. O índice já tinha 330 renomes e 51 exclusões de antes; `git add -A` incluiria também mudanças locais de `application/crates/` que não são desta task, então o commit precisa escolher os caminhos. Arquivos novos não rastreados: este `.review.md`, `sdd/tasks/*/r2/`, `ac08_refs.{py,sh}`, `ac13_clean_copy.sh`, `docs/licensing/license-source.json`. (7) Os logs antigos em `.local/tasks/SDD-ENXUTO-20261123/` não são mais citados e podem ser apagados.
- Estado final: concluída

## Revisão r3 — 2026-11-24 — Base fixa do AC-08

Motivo: a segunda revisão externa (em [SDD-ENXUTO-20261123.review.md](SDD-ENXUTO-20261123.review.md))
confirmou a r2 e apontou que `ac08_refs.sh` lia os caminhos removidos de `git ls-tree HEAD`. Depois
do commit da remoção, o HEAD não tem mais esses caminhos e a busca deixa de vê-los. Mesmo escopo.

### 1. Prompt

Pedido: fixar a base da comparação em `ea3cf0f` e reobservar o AC-08. Restrições da r2 mantidas.

- AC-08: nenhum arquivo ativo referencia o legado por termo, por caminho removido (existente em `ea3cf0f`, último commit com o legado, ou em `removed-paths.txt`; em texto, código inline ou link) ou por nome de arquivo que existia em um único caminho de `ea3cf0f`, removido | método: `bash sdd/tasks/SDD-ENXUTO-20261123/ac08_refs.sh` (base fixa no script; exclusões e permissões com motivo em `EXCLUDE` e `ALLOWED` de `ac08_refs.py`; histórico citado como `<commit>:<caminho>` não conta) | esperado: exit 0, `base=ea3cf0f` e `ocorrencias=0`; com a lista de um HEAD simulado depois das remoções, a referência reintroduzida a `sdd/features/scripts-task-closure/plan.md` continua detectada pela base fixa

### 4. Plano

| Decisão | REQ | Escolha | Alternativa descartada e motivo |
|---|---|---|---|
| D-11 | REQ-05 | Base fixa `ea3cf0f` (SHA completo) em `ac08_refs.sh`; sem esse commit (clone raso), exit 2 com mensagem | HEAD corrente: perde a cobertura depois do commit; base por parâmetro: o critério fica dependente de quem roda |

| SKILL.md | Motivo | Contribuição |
|---|---|---|
| `.codex/skills/software-testing/SKILL.md` | AC-08 | Teste que reproduz o defeito (HEAD simulado) antes da correção |

### 5. Itens de trabalho

| Item | D | Arquivos (dono) | Depende de | Teste | Pronto quando | Skill |
|---|---|---|---|---|---|---|
| T-12 | D-11 | `sdd/tasks/SDD-ENXUTO-20261123/ac08_refs.{sh,py}` | — | AC-08 | base fixa e reprodução do revisor detectada | `software-testing` |

### 7. Execução

| Item | Arquivos alterados | Teste executado | Exit | Observação |
|---|---|---|---|---|
| T-12 | `ac08_refs.sh` (base `ea3cf0f2b52d…`, guarda do commit, linha `base=`), `ac08_refs.py` (textos "HEAD" → "base"; exit 2 com lista base vazia, achado da rodada 5 do verificador) | `ac08_refs.sh`; sonda com `sdd/features/scripts-task-closure/plan.md` contra a lista de `ea3cf0f` e contra a de um HEAD simulado (só caminhos existentes) | 0 (`ocorrencias=0`); 1 com a base (1 ocorrência); 0 com o HEAD simulado (`removidos=53`) | Reproduz a revisão 2: só `removed-paths.txt` sobra no HEAD simulado, e `sdd/features/` não está nele (foi renomeado no índice antes da task) |

### 8. Validação

#### Estado na reabertura (obsoletas)

| AC | Critério (SHA-256) | Método executado | Inputs | Resultado observado | Estado |
|---|---|---|---|---|---|
| AC-08 | — | — | — | critério e script mudaram; aguarda observação r3 | UNVERIFIED |

#### Observação r3

Observação do verificador independente (rodadas 5 e 6), devolvida sem hashes; o escritor do
registro atribuiu os IDs e gravou os hashes com `sddtask.py evidence --write`.

| Input | Caminho ou saída | Papel | SHA-256 |
|---|---|---|---|
| I-112 | `scripts/config/automation.json` | configuração | `989f268b634b394ea25200d796ada3edaa6ec3ed66b90e62a3f31376df1172ed` |
| I-113 | `sdd/tasks/SDD-ENXUTO-20261123/ac08_refs.sh` | oráculo | `ff600d9265eb53aef3f9fa794e7eefa1f15d26cc04e3eaf5a0445a2edf408ab1` |
| I-114 | `sdd/tasks/SDD-ENXUTO-20261123/ac08_refs.py` | oráculo | `a99841be1bef265e0c7b8b4a8336f029a651f50a1e090831b70e62e9d3cd3678` |
| I-115 | `sdd/tasks/SDD-ENXUTO-20261123/removed-paths.txt` | configuração | `73f6803b0a3192264276d21747a945e1ee6ccbc60cd9e4eed8bd7a34ab593fe0` |
| I-116 | `sdd/tasks/SDD-ENXUTO-20261123/r3/ac08.log` | material | `d47357f4a60c513e78dbfeb3703c21b54ba80491a6713ee485e7094e2b518172` |

| AC | Critério (SHA-256) | Método executado | Inputs | Resultado observado | Estado |
|---|---|---|---|---|---|
| AC-08 | `b54f1472a4df110bf7c3c38ab8aa0f05d2fa052732d767a80b83dee64405e37e` | `bash sdd/tasks/SDD-ENXUTO-20261123/ac08_refs.sh`; sonda com `sdd/features/scripts-task-closure/plan.md` injetada na lista de ativos e rodada com `ac08_refs.py` contra a lista de `ea3cf0f` e contra a de um HEAD simulado (só caminhos existentes); guarda de lista base vazia | I-112, I-113, I-114, I-115, I-116 | exit 0; `base=ea3cf0f`, `ocorrencias=0 ativos=603 removidos=23066`. Sonda: com `ea3cf0f`, exit 1 e 1 ocorrência; com o HEAD simulado, exit 0, `ocorrencias=0`, `removidos=53`. Lista base vazia: exit 2. Nenhuma sonda no working tree | APPROVED |

### 9. Fechamento

- Documentação: sem impacto: só o script e o critério do AC-08 mudaram; a resposta está na [revisão externa 2](SDD-ENXUTO-20261123.review.md)
- `sdd/project.md`: sem mudança
- Inputs da seção 8 alterados no fechamento: nenhum (`evidence --check --require-all` exit 0, 132 verificações; cópia sem `.local/` exit 0)
- Checks de governança: `validate.py --root .` exit 0; `check-ox.py` exit 0; suíte do SDD exit 0 (69)
- Pendências: as da r2 continuam (verificação completa, Ruff, Bandit e Python 3.11 não executados; `OX-PATCH.md:37`; `views.rs:1221-1222`; SVG editado à mão; nada em stage nem commitado). O AC-08 exige o commit `ea3cf0f` no clone (num clone raso, sai com exit 2). Em `ac08_refs.py`, `main` reaproveita o nome `base` para o diretório do arquivo depois do último uso da lista; não muda o resultado (nota do verificador).
- Estado final: concluída

## Revisão r4 — 2026-11-24 — Achados da verificação completa

Motivo: a verificação completa (`./scripts/automate.sh run --scope complete`, execução
`ox-run-s2V25Ten`, rodada pelo usuário depois dos commits `b37b08b` e `d5c9f5b`) saiu com código 3.
Dois achados são desta task: Ruff F541 em `sdd/tools/tests/test_sddtask.py:266` (f-string sem
variável, presente desde o r1) e Bandit B112 em `sdd/tasks/SDD-ENXUTO-20261123/ac08_refs.py:115`
(`except UnicodeDecodeError: continue`). O terceiro, `audit` bloqueado, era a base do RustSec
vencida (válida até 2026-11-23). O usuário escolheu corrigir por revisão e autorizou o download.

### 7. Execução

| Item | Arquivos alterados | Teste executado | Exit | Observação |
|---|---|---|---|---|
| T-03 | `sdd/tools/tests/test_sddtask.py` (sem o `f` da linha 266; correção segura indicada pelo Ruff) | `run --check ruff --check bandit` (`ox-run-ALzoMXov`) | 0 (`ruff` e `bandit` passed) | Arquivo sem pin |
| T-12 | `ac08_refs.py`: `except` atribui `text = None` e o `continue` vem depois, sem supressão e sem entrada no baseline | o mesmo; `ac08_refs.sh` | 0; 0 (`ocorrencias=0`) | Arquivo sem pin |
| — | base RustSec renovada: `scripts/security/prepare-datasets.sh --review <revisão> --download --only rustsec`, revisão `1d328b6bb9f2f350bf65c1c81ab68781cb9e018a` (2026-11-24), válida até 2026-11-29; registro `.cache/ox/security/datasets.json` | `run --surface application --check audit` (`ox-run-ljD4fTvd`) | 0 (`audit` passed, 0 achados) | Download autorizado pelo usuário em 2026-11-24 |

Falhas e tentativas abandonadas:
- O B112 escapou da revisão: o verificador afirmou na rodada 1 que o B112 só aponta exceção
  ampla, mas `scripts/config/native/bandit/bandit.yaml` define
  `try_except_continue: check_typed_exception: true`, e o escritor do registro já tinha lido esse
  arquivo sem conferir a afirmação. O F541 estava fora do diff revisado nas r2 e r3.

### 8. Validação

#### Estado na reabertura (obsoletas)

| AC | Critério (SHA-256) | Método executado | Inputs | Resultado observado | Estado |
|---|---|---|---|---|---|
| AC-02 | — | — | — | `test_sddtask.py` mudou; aguarda observação r4 | UNVERIFIED |
| AC-08 | — | — | — | `ac08_refs.py` mudou; aguarda observação r4 | UNVERIFIED |
| AC-11 | — | — | — | `test_sddtask.py` mudou; aguarda observação r4 | UNVERIFIED |

#### Observação r4

AC-02 e AC-08 pelo verificador independente (rodada 7), devolvidos sem hashes; AC-11 pelo escritor
do registro depois do `--write`.

| Input | Caminho ou saída | Papel | SHA-256 |
|---|---|---|---|
| I-117 | `sdd/tools/sddtask.py` | material | `9e30d1c8df59c68f44c3f8ff7b47e6a572f020073270860fa6575800c9fd3224` |
| I-118 | `sdd/tools/validate.py` | oráculo | `3908e9d5371cf52a90f8e43846647498e6af9ed9ed41d6d47162da61a243e503` |
| I-119 | `sdd/tools/tests/test_sddtask.py` | oráculo | `82d79790a7e7ce8de48d4d543629c6ce7f1cb0a5512efec8f33f9a270726dd6e` |
| I-120 | `sdd/tools/tests/test_validate.py` | oráculo | `b3e4247d7772e06669535d88e4de0928d78b373f0b805ea4de8516f691dd6ecf` |
| I-121 | `sdd/tasks/SDD-ENXUTO-20261123/r4/ac02.log` | material | `4326725d3f4198d25d73756a99999b7eb04b51f57bd87df42c30cc205c8b09fa` |
| I-122 | `scripts/config/automation.json` | configuração | `989f268b634b394ea25200d796ada3edaa6ec3ed66b90e62a3f31376df1172ed` |
| I-123 | `sdd/tasks/SDD-ENXUTO-20261123/ac08_refs.sh` | oráculo | `ff600d9265eb53aef3f9fa794e7eefa1f15d26cc04e3eaf5a0445a2edf408ab1` |
| I-124 | `sdd/tasks/SDD-ENXUTO-20261123/ac08_refs.py` | oráculo | `594ce920ea04a4b7e59b1b57c4bf2e04d71899a0cc26183805c65acb516d9845` |
| I-125 | `sdd/tasks/SDD-ENXUTO-20261123/removed-paths.txt` | configuração | `73f6803b0a3192264276d21747a945e1ee6ccbc60cd9e4eed8bd7a34ab593fe0` |
| I-126 | `sdd/tasks/SDD-ENXUTO-20261123/r4/ac08.log` | material | `e2136a436c85d4a495b75e14e5b5efefe1ab037c4fa59c5b45db2e4be15d8238` |

| AC | Critério (SHA-256) | Método executado | Inputs | Resultado observado | Estado |
|---|---|---|---|---|---|
| AC-02 | `e38241e576702fd076f0b7173afce3cfdf4ca0a30ed11b75f2d48ca3ff13a02a` | `python3 -m unittest discover -s sdd/tools/tests` (mais `-v` complementar) | I-117, I-118, I-119, I-120, I-121 | exit 0; 69 testes OK; 11 de `EvidenceCommandTests` (inclusive `test_obsolete_observations_are_not_rewritten`, o teste corrigido); matriz: `test_matrix_is_derived_from_sections_3_to_5` e `test_rejects_req_whose_criteria_no_item_tests` (órfão) | APPROVED |
| AC-08 | `b54f1472a4df110bf7c3c38ab8aa0f05d2fa052732d767a80b83dee64405e37e` | `bash sdd/tasks/SDD-ENXUTO-20261123/ac08_refs.sh`; sonda com `sdd/features/scripts-task-closure/plan.md` injetada na lista de ativos e rodada com `ac08_refs.py` contra a lista de `ea3cf0f` e contra a do HEAD real `d5c9f5b`; guarda de lista base vazia | I-122, I-123, I-124, I-125, I-126 | exit 0; `base=ea3cf0f`, `ocorrencias=0 ativos=605 removidos=23066`. Sonda: com `ea3cf0f`, exit 1 e 1 ocorrência; com o HEAD `d5c9f5b`, exit 0, `ocorrencias=0`, `removidos=53` (a perda de cobertura que a base fixa evita, agora no commit real). Lista base vazia: exit 2 | APPROVED |
| AC-11 | `b8bdc4f0649d2bbab59ee346933b4b761d1bc8d0e0df7e9fab3ef2a762145ba6` | `python3 sdd/tools/sddtask.py evidence --task SDD-ENXUTO-20261123 --check --require-all` (pelo escritor do registro, depois do `--write`) | I-117, I-119 | exit 0; `0 problema(s) em 142 verificação(ões)` | APPROVED |

### 9. Fechamento

- Documentação: sem impacto: só um teste e o script do AC-08 mudaram
- `sdd/project.md`: sem mudança
- Inputs da seção 8 alterados no fechamento: nenhum (`evidence --check --require-all` exit 0, 142 verificações; cópia sem `.local/` exit 0)
- Checks de governança: `validate.py --root .` exit 0; `check-ox.py` exit 0; suíte do SDD exit 0 (69); Ruff, Bandit e audit isolados via `automate.sh` passed (`ox-run-ALzoMXov`, `ox-run-ljD4fTvd`)
- Pendências: a verificação completa precisa rodar de novo para confirmar as 26 fases juntas (só Ruff, Bandit e audit foram repetidos isoladamente). A base RustSec vale até 2026-11-29; depois disso a fase `audit` volta a bloquear até nova renovação. Python 3.11 não executado. Continuam `OX-PATCH.md:37` (vendor) e `views.rs:1221-1222` (produto). Nada em stage nem commitado nesta revisão.
- Estado final: concluída
