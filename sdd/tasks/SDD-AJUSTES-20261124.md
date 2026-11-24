# SDD-AJUSTES-20261124 — Sequência da validação, fechamento sem ciclo e skill por item

- Data de abertura: 2026-11-24
- Rota: Completa — altera gates e a sequência de evidência das etapas 5, 6, 8 e 9 e o validador
- Revisão atual: r2
- Spec(s): NOT APPLICABLE — processo, não capacidade do produto
- Estado: concluída

## 1. Prompt

Pedido original (literal): "sim" — aceite da proposta: corrigir (1) a sequência da etapa 8, em que
o `ec_verificador` roda `sddtask.py evidence --check` antes de o orquestrador preencher os hashes;
(2) o ciclo entre as etapas 8 e 9 (8 manda concluir 9.1–9.2; 9.3 manda refazer 8); (3) o gate da
etapa 6 escrito como `validate.py --task <ID>` na tabela e `--matrix` no texto; (4) a escolha de
skill que não passa do planejador para o implementador e o verificador.

### 1 - Objetivos

Remover as quatro inconsistências do contrato de execução em `sdd/workflow.md`, no template de
task, nos perfis do Codex e no validador, sem mudar o fluxo de etapas nem os perfis existentes.
Público: Codex e mantenedor. Insumos: `sdd/workflow.md`, `sdd/templates/task.md`,
`.codex/agents/ec_*.toml`, `sdd/tools/validate.py` e testes.

### 2 - Requisitos

- Etapa 8: o verificador devolve, por AC, método executado, inputs com papel, resultado observado
  e estado, sem preencher hashes; quem escreve o registro (orquestrador, ou raiz na rota Local)
  grava as linhas, roda `sddtask.py evidence --write` e depois `--check --require-all`.
- Documentação afetada e `sdd/project.md` são atualizados no último item da etapa 7; a etapa 8 não
  depende da etapa 9 e a etapa 9 não manda refazer a etapa 8.
- Toda menção a `validate.py` com `--task` em `sdd/workflow.md`, no template e nos perfis usa
  `--root . --task <ID> --matrix`.
- Cada item `T-n` da seção 5 tem a coluna `Skill`; a delegação leva a skill do item; implementador
  e verificador usam a skill do item.
- O validador rejeita, em task da rota `Completa` aberta em 2026-11-24 ou depois, item sem skill,
  skill inexistente em `.codex/skills/` e skill ausente da tabela Skills lidas.
- Em task `concluída`, arquivo de input alterado ou removido depois do fechamento não reprova
  `validate.py --root .`; critério alterado, hash malformado e referência a `I-n` inexistente
  continuam reprovando, e `sddtask.py evidence --check` continua listando a alteração.

### 3 - Restrições

- NÃO commitar, fazer stage, push ou reescrever histórico.
- NÃO rodar a verificação completa via Toolbox.
- NÃO alterar código Rust do produto nem `application/vendor/`.
- NÃO alterar o registro fechado `sdd/tasks/SDD-ENXUTO-20261123.md`.
- NÃO renovar pin de `reviews.static` sem revisão independente das mudanças do arquivo.
- NÃO enfraquecer checks existentes; nenhum teste existente é removido.
- NÃO criar, remover ou renomear perfis do Codex nem mudar modelo ou esforço.
- Preservar as mudanças não commitadas existentes no working tree.
- Permissões: o pedido autoriza editar os arquivos acima e os testes; não autoriza commit,
  downloads nem a verificação completa.

### 4 - Critérios de Aceitação

- AC-01: o perfil `ec_verificador` não manda rodar `sddtask.py evidence`; a etapa 8 e os perfis de orquestrador mandam rodar `--write` e depois `--check --require-all`, e o Papel orquestrador remete ao passo 2 da etapa 8 | método: `python3 -m unittest discover -s tools/governance/tests -p test_instruction_routes.py` | esperado: exit 0, com asserções dessas três condições
- AC-02: `sdd/workflow.md` não cita os passos 9.1 ou 9.2 e a etapa 7 manda atualizar a documentação afetada e `sdd/project.md` | método: `bash sdd/tasks/SDD-AJUSTES-20261124/ac02_ac03.sh` | esperado: exit 0; linha `AC-02 ok`
- AC-03: toda linha de `sdd/workflow.md`, `sdd/templates/task.md` e `.codex/agents/*.toml` que cita `validate.py` com `--task` também cita `--matrix` | método: `bash sdd/tasks/SDD-AJUSTES-20261124/ac02_ac03.sh` | esperado: exit 0; linha `AC-03 ok`
- AC-04: a tabela de itens do template tem a coluna `Skill`, o gate da etapa 5 e a lista da Delegação citam a skill do item, e os perfis `ec_implementador`, `ec_implementador_extra_alto` e `ec_verificador` citam a skill do item | método: `python3 -m unittest discover -s tools/governance/tests -p test_instruction_routes.py` | esperado: exit 0, com asserções dessas condições
- AC-05: o validador rejeita item sem skill, skill inexistente e skill fora de Skills lidas em task da rota `Completa` aberta a partir de 2026-11-24, e aceita task anterior sem a coluna | método: `python3 -m unittest discover -s sdd/tools/tests` | esperado: exit 0, com testes de cada rejeição e da aceitação
- AC-06: SDD e governança continuam válidos | método: `python3 sdd/tools/validate.py --root .`, `python3 tools/governance/scripts/check-ox.py`, `python3 tools/governance/scripts/run-tests.py` e `python3 -m unittest discover -s scripts/tests` | esperado: exit 0 nos quatro
- AC-07: os pins de `reviews.static` dos arquivos alterados batem com os bytes atuais e a revisão está registrada no `reason` | método: `python3 sdd/tasks/SDD-AJUSTES-20261124/ac07_pins.py` | esperado: exit 0; `0 divergência(s)`
- AC-08: a leitura obrigatória (AGENTS, constitution, project, workflow e skill `prompt`) tem no máximo 5635 palavras | método: `wc -w AGENTS.md sdd/constitution.md sdd/project.md sdd/workflow.md .codex/skills/prompt/SKILL.md` | esperado: total ≤ 5635
- AC-10: o validador aceita task concluída com input alterado depois do fechamento e rejeita task aberta com input alterado e task concluída com critério alterado | método: `python3 -m unittest discover -s sdd/tools/tests` | esperado: exit 0, com testes dos três casos
- AC-09: a evidência deste registro foi gerada pela ferramenta e está atual | método: `python3 sdd/tools/sddtask.py evidence --task SDD-AJUSTES-20261124 --check --require-all` | esperado: exit 0

### 5 - Entrega

- Arquivos/saídas: `sdd/workflow.md`, `sdd/templates/task.md`, `.codex/agents/ec_verificador.toml`,
  `ec_implementador.toml`, `ec_implementador_extra_alto.toml`, `ec_orquestrador_*.toml` se citarem a
  sequência, `sdd/tools/validate.py`, `sdd/tools/tests/test_validate.py`,
  `tools/governance/tests/test_instruction_routes.py`, `scripts/config/automation.json` (pins) e
  artefatos em `sdd/tasks/SDD-AJUSTES-20261124/`.
- Regra de conclusão: a task está concluída quando AC-01…AC-10 estiverem APPROVED ou NOT APPLICABLE
  com motivo, e a seção 9 estiver preenchida.

## 2. Esclarecimentos

| Q | Pergunta | Resposta do usuário | AC/etapa afetados |
|---|---|---|---|
| — | Nenhuma pergunta aberta: as quatro correções foram propostas e aceitas ("sim") | — | — |

Fato descoberto na etapa 7 (2026-11-24): editar `sdd/workflow.md` deixou 13 inputs da task
fechada SDD-ENXUTO-20261123 desatualizados, e `validate.py --root .` saiu com 1 (15 falhas). Toda
task que alterasse arquivo usado por task fechada reprovaria o repositório. Alterar o registro
fechado é vetado pelas Restrições; o workflow já trata input alterado como retomada. Daí REQ-06,
D-06, T-06 e AC-10, registrados antes da validação.

Suposições: `SUPOSIÇÃO: a exigência da coluna Skill vale para tasks abertas a partir de 2026-11-24, para não reescrever o registro fechado SDD-ENXUTO-20261123.` `SUPOSIÇÃO: a rota é Completa porque a mudança altera gates de evidência (risco material, workflow, Rotas), embora a proposta a chamasse de Local.`

## 3. Especificação

Motivação (por quê): o verificador falharia sempre no `--check` (célula de hash vazia é
`malformed`); as etapas 8 e 9 dependem uma da outra; o gate da etapa 6 tem duas grafias; e a skill
escolhida no plano não chega a quem implementa e valida.

- REQ-01: a sequência da etapa 8 separa observação (verificador) de gravação e conferência de hashes (escritor do registro).
- REQ-02: a atualização de documentação ocorre antes da validação, sem ciclo entre as etapas 8 e 9.
- REQ-03: o gate da etapa 6 tem uma única grafia em todos os documentos que o citam.
- REQ-04: a skill de cada item é registrada no plano, transmitida na delegação e verificada pelo validador.
- REQ-06: em task concluída, alteração de input posterior ao fechamento é retomada, não falha do validador; as demais falhas da etapa 8 continuam.
- REQ-05: a mudança não quebra as checagens existentes nem aumenta a leitura obrigatória além do limite do ADR.
- AC-01 → REQ-01
- AC-09 → REQ-01
- AC-02 → REQ-02
- AC-03 → REQ-03
- AC-04 → REQ-04
- AC-05 → REQ-04
- AC-06 → REQ-05
- AC-07 → REQ-05
- AC-08 → REQ-05
- AC-10 → REQ-06

Cenários rejeitados: item com `Skill` vazia, `nenhuma` sem motivo, skill sem pasta em
`.codex/skills/` ou não listada em Skills lidas → `FAIL: etapa 5: …`; task Completa aberta antes
de 2026-11-24 sem a coluna → aceita.

## 4. Plano

| Decisão | REQ | Escolha | Alternativa descartada e motivo |
|---|---|---|---|
| D-01 | REQ-01 | Verificador devolve observações; o escritor do registro roda `--write` e `--check --require-all` | Verificador rodar `--write`: ele passaria a editar o registro, que tem um único escritor |
| D-02 | REQ-02 | Documentação e `project.md` viram o último item da etapa 7; a etapa 9 registra e confere com `--check --require-all` | Manter 9.1–9.2 e a repetição de 8: preserva o ciclo |
| D-03 | REQ-03 | Grafia única `validate.py --root . --task <ID> --matrix` | Só `--task`: o planejador não veria a matriz que a etapa 6 descreve |
| D-04 | REQ-04 | Coluna `Skill` na seção 5 (nomes entre crases ou `nenhuma: <motivo>`), campo na Delegação e checagem no validador para tasks Completa abertas a partir de 2026-11-24 | Exigir para todas: reprovaria o registro fechado SDD-ENXUTO-20261123, que não pode ser editado |
| D-06 | REQ-06 | Em task `concluída`, status `stale`/`missing` de arquivo de input não reprova; o resto da etapa 8 continua | Reobservar a task fechada numa revisão r2: vetado nas Restrições e repetido a cada edição de arquivo compartilhado. Limite aceito: o `validate.py` não detecta task marcada concluída sem o `--check --require-all` da etapa 9 |
| D-05 | REQ-05 | Rodar as suítes e checks existentes, revisar e renovar os pins só após revisão independente, medir a leitura obrigatória | Pular os pins: as fases Ruff/Bandit da verificação completa bloqueariam |

Skills lidas (obrigatória em toda rota com registro; no mínimo `prompt`):

| SKILL.md | Motivo | Contribuição |
|---|---|---|
| `.codex/skills/prompt/SKILL.md` | etapas 1–2 | cinco divisões, guardrails, AC com método e esperado, regra de conclusão |
| `.codex/skills/software-testing/SKILL.md` | etapas 5, 7 e 8 | casos de rejeição e de aceitação do validador; oráculo independente (verificador em contexto novo) |

ADR: NOT APPLICABLE — ajuste do contrato existente; `docs/decisions/sdd-model.md` não muda de decisão.

## 5. Itens de trabalho

| Item | D | Arquivos (dono) | Depende de | Teste | Pronto quando | Skill |
|---|---|---|---|---|---|---|
| T-01 | D-01 | `sdd/workflow.md` (etapa 8, papéis), `.codex/agents/ec_verificador.toml`, `ec_orquestrador_*.toml` | — | AC-01, AC-09 | asserções de AC-01 passam | nenhuma: edição de contrato em texto |
| T-02 | D-02 | `sdd/workflow.md` (etapas 7 e 9), `sdd/templates/task.md` (seção 9) | T-01 | AC-02 | script de AC-02 sai com 0 | nenhuma: edição de contrato em texto |
| T-03 | D-03 | `sdd/workflow.md` (tabela de etapas), `.codex/agents/*.toml` | T-01 | AC-03 | script de AC-03 sai com 0 | nenhuma: edição de contrato em texto |
| T-04 | D-04 | `sdd/workflow.md` (etapa 5, Delegação), `sdd/templates/task.md`, `.codex/agents/ec_implementador*.toml`, `sdd/tools/validate.py`, `sdd/tools/tests/test_validate.py`, `tools/governance/tests/test_instruction_routes.py` | T-01 | AC-04, AC-05 | suítes de AC-04 e AC-05 saem com 0 | `software-testing` |
| T-06 | D-06 | `sdd/tools/validate.py`, `sdd/tools/tests/test_validate.py`, `sdd/workflow.md` (Evidência e retomada) | T-04 | AC-10 | testes de AC-10 passam | `software-testing` |
| T-05 | D-05 | `scripts/config/automation.json`, `sdd/tasks/SDD-AJUSTES-20261124/` | T-02, T-03, T-04, T-06 | AC-06, AC-07, AC-08 | checks saem com 0 e pins batem | `software-testing` |

## 6. Coerência

`python3 sdd/tools/validate.py --root . --task SDD-AJUSTES-20261124 --matrix`: exit 0. Matriz:
REQ-01 → D-01 → T-01 → AC-01, AC-09; REQ-02 → D-02 → T-02 → AC-02; REQ-03 → D-03 → T-03 → AC-03;
REQ-04 → D-04 → T-04 → AC-04, AC-05; REQ-05 → D-05 → T-05 → AC-06, AC-07, AC-08;
REQ-06 → D-06 → T-06 → AC-10.

Conflitos com POL/GOV/RQ: nenhum. GOV-05 (estados e evidência) mantida: D-06 só muda quando o validador reprova input alterado após o fechamento. GOV-02 (contrato único) mantido: as mudanças ficam no workflow;
GOV-04: a coluna Skill aponta para o catálogo do workflow; GOV-05: hashes seguem pela ferramenta.

## 7. Execução

| Item | Arquivos alterados | Teste executado | Exit | Observação |
|---|---|---|---|---|
| T-01 | `sdd/workflow.md` (etapa 8, Papel orquestrador, Papel verificador), `.codex/agents/ec_verificador.toml`, `ec_orquestrador_normal.toml`, `ec_orquestrador_alta.toml` | `python3 -m unittest discover -s tools/governance/tests -p test_instruction_routes.py` | 0 | 5 testes; novo `test_stage_8_sequence_and_item_skill` |
| T-02 | `sdd/workflow.md` (etapas 7 e 9, tabela), `sdd/templates/task.md` (seções 8 e 9) | `bash sdd/tasks/SDD-AJUSTES-20261124/ac02_ac03.sh` | 0 | `AC-02 ok`; `technical-documentation` e `readme-lifecycle-engineering` passam da etapa 9 para a 7 no catálogo |
| T-03 | `sdd/workflow.md` (tabela, Papel planejador), `.codex/agents/ec_planejador.toml` | `bash sdd/tasks/SDD-AJUSTES-20261124/ac02_ac03.sh` | 0 | `AC-03 ok` |
| T-04 | `sdd/workflow.md` (etapa 5, Delegação, Papel implementador), `sdd/templates/task.md` (seção 5), `.codex/agents/ec_implementador.toml`, `ec_implementador_extra_alto.toml`, `sdd/tools/validate.py` (`item_skill_errors`), `sdd/tools/tests/test_validate.py`, `tools/governance/tests/test_instruction_routes.py` | `python3 -m unittest discover -s sdd/tools/tests` | 0 | 64 testes; mutantes mortos: sem a checagem de skill (7 casos), sem `SKILL_NAME_RE`, data ausente pulando a checagem |
| T-06 | `sdd/tools/validate.py` (`POST_CLOSE_DRIFT`, `drifted_after_close`), `sdd/tools/tests/test_validate.py`, `sdd/workflow.md` (Evidência e retomada) | `python3 -m unittest discover -s sdd/tools/tests` | 0 | 64 testes depois das correções; mutantes mortos: drift em task aberta (2 testes) e tolerância sem exigir hash válido (4 casos) |
| T-05 | `.claude/skills/codex-task-audit/SKILL.md`, `references/ox-governance.md` (gates das etapas 5–8 alinhados), `sdd/tasks/SDD-AJUSTES-20261124/ac02_ac03.sh`, `ac07_pins.py` | `python3 tools/governance/scripts/check-ox.py`; `python3 tools/governance/scripts/run-tests.py` | 0; 0 | run-tests: 238 testes, OK (1 skipped); pins aguardam revisão independente |

Documentação (último item da etapa 7): `sdd/workflow.md` e `sdd/templates/task.md` são o próprio
contrato; a skill de auditoria `.claude/skills/codex-task-audit/` foi alinhada; `README.md`,
`docs/README.md` e `docs/decisions/sdd-model.md` não descrevem a sequência das etapas 8 e 9 nem a
seção 5 (sem impacto); `sdd/project.md` sem mudança (fase e escopo iguais; nenhuma task aberta
além desta). Leitura obrigatória medida: 5634 palavras.

Falhas e tentativas abandonadas:
- Primeira aplicação das edições do workflow abortou (trecho da Delegação com quebra de linha diferente); nada foi gravado, corrigido e reaplicado.
- Leitura obrigatória chegou a 5674 palavras; reduzida a 5635 removendo a descrição das tabelas da etapa 8 (já no template), a repetição do passo 2 no Papel orquestrador e a frase "Pedido de status é rota Consulta" (já coberta por Rotas).
- `validate.py --root .` saiu com 1: termo `Completa` lido como subjetivo neste registro (corrigido com crases) e 13 inputs desatualizados da task fechada SDD-ENXUTO-20261123 (D-06).
- Teste de drift falhou por ordem do próprio teste (arquivo removido antes do caso malformado); a correção foi no teste e escondeu o defeito D1 abaixo.
- Verificação independente (contexto novo, 2026-11-24) reprovou AC-10 e a renovação de um pin, com 7 achados, todos corrigidos com teste de regressão e mutante morto:
  - D1 (importante): em task concluída, input com hash malformado, vazio ou symlink passava, porque `freshness` devolve `missing` antes de olhar o formato. Agora a tolerância exige SHA-256 completo gravado e caminho que não é symlink (`drifted_after_close`); teste `test_concluded_task_still_rejects_inputs_never_hashed`.
  - D2 (importante): `lambda` atribuído em `test_instruction_routes.py` (Ruff E731, selecionado por `E7`); virou `def stage`.
  - D3: `Data de abertura` antedatada dispensava a coluna Skill; agora a dispensa exige que a data do ID e a do metadado sejam anteriores a 2026-11-24.
  - D4: mutantes sobreviventes (sem `SKILL_NAME_RE`; data ausente pulando a checagem); agora mortos por casos de traversal `../skills/prompt` e data ausente ou não ISO.
  - D5: Skills lidas conferida por substring e texto fora de crases ignorado; agora conjunto exato e texto solto reprova.
  - D6: o contrato mostra `nenhuma: <motivo>` entre crases, mas o validador recusava essa forma; agora aceita as duas.
  - D7: a etapa 8 e o perfil do verificador não diziam quem observa e grava na rota Local; agora "o verificador (na rota Local, a raiz)" e "o escritor do registro grava e confere".
- Fechamento: `validate.py --root .` reprovou AC-09 APPROVED sem input `material` (eu tinha citado só a ferramenta); a saída do `--check` virou I-25 (`material`), `--write` preencheu o hash e os checks foram repetidos.

## 8. Validação

Observações do verificador em contexto novo (r2 e r3, 2026-11-24), gravadas pelo escritor do
registro; AC-07 e AC-09 executados pelo escritor (comandos determinísticos). Logs em
`.local/tasks/SDD-AJUSTES-20261124/` (ignorado pelo Git). A observação r1 do verificador (AC-07 e
AC-10 REJECTED, achados D1–D7) está na seção 7.

| Input | Caminho ou saída | Papel | SHA-256 |
|---|---|---|---|
| I-01 | `sdd/workflow.md` | material | `b38f2351b119528ffb8087d395e2d2fb08a3b3e115d87b0bb7c8a0880dc9b2c8` |
| I-02 | `.codex/agents/ec_verificador.toml` | material | `8449e20054ea1df0b94441836abd5aa1e2b506c05564af274f7de78d643c1320` |
| I-03 | `.codex/agents/ec_orquestrador_normal.toml` | material | `f10d3e3642d18ef1a4cae2a08b5d7899e00fcdc7319208d7f4b3fd0b12f0f601` |
| I-04 | `.codex/agents/ec_orquestrador_alta.toml` | material | `3a2e31366e1f5a5d44c25e08df8bd9c85d4287adbaeb7e89f2cc5e90cf7f931d` |
| I-05 | `tools/governance/tests/test_instruction_routes.py` | oráculo | `0cf2ef1bb4918dd46e77b0fc1e19a1252d3f62a75dc82beb041483f2681eb503` |
| I-06 | `sdd/tasks/SDD-AJUSTES-20261124/ac02_ac03.sh` | oráculo | `e92e2ce9f327e358709fa690dc01ea34f76f08519c32a513d25ea9e26efe982c` |
| I-07 | `sdd/templates/task.md` | material | `ee39c0bc144e855a43535d28b4406cbfa4694b9975ae8df034adb6f832cef001` |
| I-08 | `.codex/agents/ec_implementador.toml` | material | `c76ca3b940b25758b323a9970ee30792dc0c7ae0e3e7c1dbd4c21350de652f2b` |
| I-09 | `.codex/agents/ec_implementador_extra_alto.toml` | material | `ca64eaa6ec6ddbacb21af9b7a30cd09b09772460afd34f98f6f1838fbde29f11` |
| I-10 | `.codex/agents/ec_planejador.toml` | material | `e8091a9dc41c34a50d994989190051bd9758334d707e19df71ad70487ab94668` |
| I-11 | `sdd/tools/validate.py` | material | `93bdabcfd3973c43569a8eab63205a92f12bcd908f27ce50bca93a2cd5a6556c` |
| I-12 | `sdd/tools/tests/test_validate.py` | oráculo | `f351ea1ab3c3734f41c7fb5a2e2f0b9ab9b325b7ec69da7bdf3979999d8e3df8` |
| I-13 | `tools/governance/scripts/check-ox.py` | oráculo | `a7dfbe0d7571dbde89626a6fe867ddff905ee4dad71f313d86563e9f27bd6604` |
| I-14 | `tools/governance/scripts/run-tests.py` | oráculo | `cc6d9abfa079238390232253f7b6f839b100fa62eedeadd82a29241daaec2df0` |
| I-15 | `.local/tasks/SDD-AJUSTES-20261124/verifier-r2-ac06-run-tests.log` | oráculo | `bdca2e57762dae3a62691385f6dc86f8920e18e28d9cee5efe2a1f35c46145ca` |
| I-16 | `.local/tasks/SDD-AJUSTES-20261124/verifier-r2-ac06-scripts-tests.log` | oráculo | `904ae974b1c4aba2392c865fcb208853b2cbd9a12057382e0599f2333a9e00f2` |
| I-17 | `scripts/config/automation.json` | configuração | `046579002544773c2bf40966926622c5e60625e2df7b6397bf89b682fd0cd866` |
| I-18 | `sdd/tasks/SDD-AJUSTES-20261124/ac07_pins.py` | oráculo | `a5a8be8c6c61076a3b277d09c51851bc44be0ae41b952b601f76ca3823be72c5` |
| I-19 | `AGENTS.md` | material | `dd53cb5f25f71bf3c6e1f72042a7a3628f67e50495b4b15c328ff5ec78158be0` |
| I-20 | `sdd/constitution.md` | material | `ac86e4dc1f9af10da34c5bca1c53dce8a4d7f7a952b432f7f16bfe0bd64947d6` |
| I-21 | `sdd/project.md` | material | `ae1e1881e030ba421b53784a6f738f26e884c2c85221308dba4c3ae97d1c1e57` |
| I-22 | `.codex/skills/prompt/SKILL.md` | material | `98bb62af25b1e62dda471c3ba032c73f45283af96400404db71224afdb3c05d5` |
| I-23 | `.local/tasks/SDD-AJUSTES-20261124/verifier-r3-mutants.log` | oráculo | `bcbf2dd07fe0e7d76f1176fdcab1fc1c657b1ee832520f775b5fe57f9f245218` |
| I-24 | `sdd/tools/sddtask.py` | oráculo | `c07b392b424a1e62929273e73ccde83f742cde98cd21645e6f62f6439daae2b8` |
| I-25 | `.local/tasks/SDD-AJUSTES-20261124/close-evidence.log` | material | `e7c63c34ac32252827bcdb595f27935a07be3d0084630a9143f9cc8ae38c9b25` |

| AC | Critério (SHA-256) | Método executado | Inputs | Resultado observado | Estado |
|---|---|---|---|---|---|
| AC-01 | `3ba83f7d9d052325e22449e5420d5e02b4c363ac00f0e89f013a59c6ab7285f7` | `python3 -m unittest discover -s tools/governance/tests -p test_instruction_routes.py -v` | I-01, I-02, I-03, I-04, I-05 | exit 0; 5 testes OK, inclusive `test_stage_8_sequence_and_item_skill` (verificador sem `sddtask.py evidence`; `--write` e depois `--check --require-all` na etapa 8 e nos dois orquestradores; "etapa 8, passo 2" no Papel orquestrador) | APPROVED |
| AC-02 | `145ecd9d9ea9bedd3bfa3a58feffaf13630ba7da1d66f5a062161a7ecb0bec74` | `bash sdd/tasks/SDD-AJUSTES-20261124/ac02_ac03.sh` | I-01, I-06 | exit 0; `AC-02 ok`; sem 9.1/9.2; etapa 7 manda atualizar documentação e `sdd/project.md` | APPROVED |
| AC-03 | `45685885c3c4d55e4a3cdab8a27cf85b82d59494c434e8f3412aced479007e26` | `bash sdd/tasks/SDD-AJUSTES-20261124/ac02_ac03.sh` | I-01, I-07, I-02, I-03, I-04, I-08, I-09, I-10, I-06 | exit 0; `AC-03 ok` | APPROVED |
| AC-04 | `62c69e8ecbd8dbe13f12e6e7e46f59286e49b9758f1ca238e28bdf562d536889` | `python3 -m unittest discover -s tools/governance/tests -p test_instruction_routes.py -v` | I-07, I-01, I-08, I-09, I-02, I-05 | exit 0; 5 testes OK; asserções da coluna `Skill`, gate da etapa 5, Delegação e perfis | APPROVED |
| AC-05 | `c5714465911eda785a1ed7a7e8ef048de10ef7e7fb41870b4775c727908500f6` | `python3 -m unittest discover -s sdd/tools/tests -v` | I-11, I-12, I-24 | exit 0; 64 testes OK, inclusive `test_rejects_item_without_valid_skill`, `test_skill_cell_forms`, `test_skill_column_exemption_needs_both_dates_before_cutoff` e `test_task_opened_before_skill_column_passes_without_it`; 13 de 13 mutantes da checagem de skill mortos (r2) | APPROVED |
| AC-06 | `f8e875486dda4a6a183f853318a64e696de701212cd2d3721fd37a5c784dbfce` | `python3 sdd/tools/validate.py --root .`; `python3 tools/governance/scripts/check-ox.py`; `python3 tools/governance/scripts/run-tests.py`; `python3 -m unittest discover -s scripts/tests` | I-01, I-11, I-13, I-14, I-15, I-16 | exit 0 nos quatro: `PASS: estrutura, 2 task(s), 10 spec(s)`; `PASS: SDD, normative IDs…`; run-tests 241 OK (1 skip); scripts/tests 139 OK (1 skip; requer Docker) | APPROVED |
| AC-07 | `b80d502b7082ce9b22c76aa10c6b66d6cd115f52729575ab1d811bc4d16c620d` | `python3 sdd/tasks/SDD-AJUSTES-20261124/ac07_pins.py` (pelo escritor do registro, depois da aprovação dos 3 pins pelo verificador no r2/r3) | I-17, I-11, I-12, I-05, I-18 | exit 0; `25 pin(s); 0 divergência(s)` | APPROVED |
| AC-08 | `2f4fa3f151d917ef30668f2aa4073de1e9e1a16cb06862eec5fcc01225328607` | `wc -w AGENTS.md sdd/constitution.md sdd/project.md sdd/workflow.md .codex/skills/prompt/SKILL.md` | I-19, I-20, I-21, I-01, I-22; sem oráculo separado: o limite numérico está no próprio critério | exit 0; total 5634 ≤ 5635 | APPROVED |
| AC-10 | `44d0dbf5e7f8cfc02443b1a5ce80230fba8b65c0ed28533bda2fbafe31eb7100` | `python3 -m unittest discover -s sdd/tools/tests -v` e mutantes M2/M2b no scratchpad | I-11, I-12, I-23 | exit 0; `test_concluded_task_tolerates_input_drift_after_closure_only` e `test_concluded_task_still_rejects_inputs_never_hashed` OK; M2b morto; M2 sobrevive por ser equivalente (a guarda de SHA já recusa hash malformado) | APPROVED |
| AC-09 | `0e7a09e044cb1b07ca223d8460bda81bc438e12122a0869dab4eb4141e28d9c9` | `python3 sdd/tools/sddtask.py evidence --task SDD-AJUSTES-20261124 --check --require-all` (pelo escritor do registro) | I-25, I-24 | exit 0; `0 problema(s) em 34 verificação(ões)` no log I-25 (10 critérios e 24 inputs); depois de gravar I-25, `0 problema(s) em 35 verificação(ões)` | APPROVED |

Contexto do validador: independente (subagente novo, sem o histórico do implementador), três rodadas.

## 9. Fechamento

- Documentação: atualizada na etapa 7 (`sdd/workflow.md`, `sdd/templates/task.md`, `.codex/agents/*.toml`, `.claude/skills/codex-task-audit/SKILL.md` e `references/ox-governance.md`); `README.md`, `docs/README.md` e `docs/decisions/sdd-model.md` sem impacto (não descrevem a sequência das etapas 8–9 nem a seção 5)
- `sdd/project.md`: sem mudança (fase e escopo iguais; nenhuma task aberta depois desta)
- Inputs da seção 8 alterados no fechamento: nenhum (`sddtask.py evidence --task SDD-AJUSTES-20261124 --check --require-all` exit 0 depois do fechamento)
- Checks de governança: `python3 sdd/tools/validate.py --root .` exit 0; `python3 tools/governance/scripts/run-tests.py` exit 0 (logs `.local/tasks/SDD-AJUSTES-20261124/close-*.log`)
- Pendências: verificação completa via Toolbox não executada (exige pedido explícito); Ruff e Bandit não instalados localmente, pins renovados por revisão das regras → confirmar na verificação completa; o `validate.py` não detecta task marcada concluída sem o `--check --require-all` da etapa 9, nem hash de 64 hex digitado à mão para caminho inexistente em task concluída (limites aceitos em D-06); `evidence --check` da task fechada SDD-ENXUTO-20261123 lista os inputs alterados por esta task (retomada, não falha); nada em stage nem commit
- Estado final: concluída

## Revisão r2 — 2026-11-24 — Evidência versionada

Motivo: a [revisão r2 de SDD-ENXUTO-20261123](SDD-ENXUTO-20261123.md#revisão-r2--2026-11-24--resposta-à-revisão-externa)
respondeu a uma revisão externa com a regra D-09: log citado na seção 8 é versionado em
`sdd/tasks/<ID>/`, e o `validate.py` reprova input em `.local/`. Os AC-06, AC-09 e AC-10 desta task
citavam logs em `.local/`, e a mesma revisão alterou `sdd/workflow.md`, `sdd/templates/task.md`,
`sdd/tools/validate.py`, `sdd/tools/sddtask.py`, `sdd/tools/tests/test_validate.py` e
`scripts/config/automation.json`, inputs de todos os ACs. Escopo e critérios desta task não mudam;
todo AC é reobservado pelo verificador independente com os logs em
`sdd/tasks/SDD-AJUSTES-20261124/r2/`.

### 8. Validação

#### Estado na reabertura (obsoletas)

Na reabertura, todo AC volta a UNVERIFIED até a nova observação.

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

#### Observação r2

Observação do verificador independente (contexto novo, rodadas 3 e 4), que devolveu as linhas sem
hashes; logs versionados em `sdd/tasks/<ID>/r2/`. O escritor do registro atribuiu os IDs `I-n`, gravou
os hashes com `sddtask.py evidence --write` e rodou os ACs que conferem o próprio registro.

| Input | Caminho ou saída | Papel | SHA-256 |
|---|---|---|---|
| I-26 | `sdd/workflow.md` | material | `c3808582075f83a4b46bf08c3958a6a700d136a6fa31da3631b20b63230d6652` |
| I-27 | `.codex/agents/ec_verificador.toml` | material | `8449e20054ea1df0b94441836abd5aa1e2b506c05564af274f7de78d643c1320` |
| I-28 | `.codex/agents/ec_orquestrador_normal.toml` | material | `f10d3e3642d18ef1a4cae2a08b5d7899e00fcdc7319208d7f4b3fd0b12f0f601` |
| I-29 | `.codex/agents/ec_orquestrador_alta.toml` | material | `3a2e31366e1f5a5d44c25e08df8bd9c85d4287adbaeb7e89f2cc5e90cf7f931d` |
| I-30 | `tools/governance/tests/test_instruction_routes.py` | oráculo | `0cf2ef1bb4918dd46e77b0fc1e19a1252d3f62a75dc82beb041483f2681eb503` |
| I-31 | `sdd/tasks/SDD-AJUSTES-20261124/r2/ac01.log` | material | `1f63875789256327018300ea312935f647c411f93cb6e4e9f6e67cbd6948fa18` |
| I-32 | `sdd/tasks/SDD-AJUSTES-20261124/ac02_ac03.sh` | oráculo | `e92e2ce9f327e358709fa690dc01ea34f76f08519c32a513d25ea9e26efe982c` |
| I-33 | `sdd/tasks/SDD-AJUSTES-20261124/r2/ac02.log` | material | `4faf08df73257229d83d5546e9e30e02b16a00afdfaa82b8916c1fac82b3b30c` |
| I-34 | `sdd/templates/task.md` | material | `e4b9dcdeb0f0c2e51bbb97058bd867dc8b8e5dc5e66dfecb4094a83610ebd3f6` |
| I-35 | `.codex/agents/ec_implementador.toml` | material | `c76ca3b940b25758b323a9970ee30792dc0c7ae0e3e7c1dbd4c21350de652f2b` |
| I-36 | `.codex/agents/ec_implementador_extra_alto.toml` | material | `ca64eaa6ec6ddbacb21af9b7a30cd09b09772460afd34f98f6f1838fbde29f11` |
| I-37 | `.codex/agents/ec_planejador.toml` | material | `e8091a9dc41c34a50d994989190051bd9758334d707e19df71ad70487ab94668` |
| I-38 | `sdd/tasks/SDD-AJUSTES-20261124/r2/ac03.log` | material | `4faf08df73257229d83d5546e9e30e02b16a00afdfaa82b8916c1fac82b3b30c` |
| I-39 | `sdd/tasks/SDD-AJUSTES-20261124/r2/ac04.log` | material | `b6d503e346eedec99cc4913373ffc9aa7dd88e6584ca48bd6cc6766a20bb2589` |
| I-40 | `sdd/tools/validate.py` | material | `3908e9d5371cf52a90f8e43846647498e6af9ed9ed41d6d47162da61a243e503` |
| I-41 | `sdd/tools/tests/test_validate.py` | oráculo | `b3e4247d7772e06669535d88e4de0928d78b373f0b805ea4de8516f691dd6ecf` |
| I-42 | `sdd/tools/sddtask.py` | oráculo | `9e30d1c8df59c68f44c3f8ff7b47e6a572f020073270860fa6575800c9fd3224` |
| I-43 | `sdd/tasks/SDD-AJUSTES-20261124/r2/ac05.log` | material | `2b15d7df309035bebe37e06c66fc9b887ccfc6e954a8509ffef0830008e5f86d` |
| I-44 | `tools/governance/scripts/check-ox.py` | oráculo | `a7dfbe0d7571dbde89626a6fe867ddff905ee4dad71f313d86563e9f27bd6604` |
| I-45 | `tools/governance/scripts/run-tests.py` | oráculo | `cc6d9abfa079238390232253f7b6f839b100fa62eedeadd82a29241daaec2df0` |
| I-46 | `sdd/tasks/SDD-AJUSTES-20261124/r2/ac06.log` | oráculo | `9de0c4d78202b016fd01b247d03e71f5b48dff98d350e1354961599b7b0e688d` |
| I-47 | `scripts/config/automation.json` | configuração | `989f268b634b394ea25200d796ada3edaa6ec3ed66b90e62a3f31376df1172ed` |
| I-48 | `sdd/tasks/SDD-AJUSTES-20261124/ac07_pins.py` | oráculo | `a5a8be8c6c61076a3b277d09c51851bc44be0ae41b952b601f76ca3823be72c5` |
| I-49 | `sdd/tasks/SDD-AJUSTES-20261124/r2/ac07.log` | material | `a45ae30296c84879a0a1d7ca878002d36a8832e8ffce78fc591177a8786524b2` |
| I-50 | `AGENTS.md` | material | `dd53cb5f25f71bf3c6e1f72042a7a3628f67e50495b4b15c328ff5ec78158be0` |
| I-51 | `sdd/constitution.md` | material | `ac86e4dc1f9af10da34c5bca1c53dce8a4d7f7a952b432f7f16bfe0bd64947d6` |
| I-52 | `sdd/project.md` | material | `ae1e1881e030ba421b53784a6f738f26e884c2c85221308dba4c3ae97d1c1e57` |
| I-53 | `.codex/skills/prompt/SKILL.md` | material | `98bb62af25b1e62dda471c3ba032c73f45283af96400404db71224afdb3c05d5` |
| I-54 | `sdd/tasks/SDD-AJUSTES-20261124/r2/ac08.log` | material | `7b3c16a4d2fa92b888ee9bc199556ab02893ffd102959e49965df4c40c6e361e` |
| I-55 | `sdd/tools/sddtask.py` | material | `9e30d1c8df59c68f44c3f8ff7b47e6a572f020073270860fa6575800c9fd3224` |
| I-56 | `sdd/tools/tests/test_sddtask.py` | oráculo | `9e3453f89113ee32db60a7e2655df7d3c675a051386cbc8e8db5572714a10e7c` |
| I-57 | `sdd/tasks/SDD-AJUSTES-20261124/r2/ac10.log` | oráculo | `5fc4e8f7dcb2b18fded8605733822ed94556e0276a210b3fb6d4e337f57cc063` |

| AC | Critério (SHA-256) | Método executado | Inputs | Resultado observado | Estado |
|---|---|---|---|---|---|
| AC-01 | `3ba83f7d9d052325e22449e5420d5e02b4c363ac00f0e89f013a59c6ab7285f7` | `python3 -m unittest discover -s tools/governance/tests -p test_instruction_routes.py` (mais `-v` complementar) | I-26, I-27, I-28, I-29, I-30, I-31 | exit 0; 5 testes OK, inclusive `test_stage_8_sequence_and_item_skill` | APPROVED |
| AC-02 | `145ecd9d9ea9bedd3bfa3a58feffaf13630ba7da1d66f5a062161a7ecb0bec74` | `bash sdd/tasks/SDD-AJUSTES-20261124/ac02_ac03.sh` | I-26, I-32, I-33 | exit 0; `AC-02 ok` | APPROVED |
| AC-03 | `45685885c3c4d55e4a3cdab8a27cf85b82d59494c434e8f3412aced479007e26` | `bash sdd/tasks/SDD-AJUSTES-20261124/ac02_ac03.sh` | I-26, I-34, I-27, I-28, I-29, I-35, I-36, I-37, I-32, I-38 | exit 0; `AC-03 ok` | APPROVED |
| AC-04 | `62c69e8ecbd8dbe13f12e6e7e46f59286e49b9758f1ca238e28bdf562d536889` | `python3 -m unittest discover -s tools/governance/tests -p test_instruction_routes.py` (mais `-v` complementar) | I-34, I-26, I-35, I-36, I-27, I-30, I-39 | exit 0; 5 testes OK, inclusive `test_stage_8_sequence_and_item_skill` (coluna `Skill`, gate da etapa 5, Delegação e perfis) | APPROVED |
| AC-05 | `c5714465911eda785a1ed7a7e8ef048de10ef7e7fb41870b4775c727908500f6` | `python3 -m unittest discover -s sdd/tools/tests` (mais `-v` complementar) | I-40, I-41, I-42, I-43 | exit 0; 69 testes OK, inclusive `test_rejects_item_without_valid_skill`, `test_skill_cell_forms`, `test_skill_column_exemption_needs_both_dates_before_cutoff` e `test_task_opened_before_skill_column_passes_without_it` | APPROVED |
| AC-06 | `f8e875486dda4a6a183f853318a64e696de701212cd2d3721fd37a5c784dbfce` | `python3 sdd/tools/validate.py --root .`; `python3 tools/governance/scripts/check-ox.py`; `python3 tools/governance/scripts/run-tests.py`; `python3 -m unittest discover -s scripts/tests` | I-26, I-40, I-44, I-45, I-46 | exit 0 nos quatro: `PASS: estrutura, 2 task(s), 10 spec(s)`; check-ox PASS; run-tests 246 OK (1 skip, Docker); `scripts/tests` 139 OK (1 skip) | APPROVED |
| AC-07 | `b80d502b7082ce9b22c76aa10c6b66d6cd115f52729575ab1d811bc4d16c620d` | `python3 sdd/tasks/SDD-AJUSTES-20261124/ac07_pins.py` (depois da renovação dos 2 pins aprovados pelo verificador) | I-47, I-40, I-41, I-30, I-48, I-49 | exit 0; `25 pin(s); 0 divergência(s)` | APPROVED |
| AC-08 | `2f4fa3f151d917ef30668f2aa4073de1e9e1a16cb06862eec5fcc01225328607` | `wc -w AGENTS.md sdd/constitution.md sdd/project.md sdd/workflow.md .codex/skills/prompt/SKILL.md` | I-50, I-51, I-52, I-26, I-53, I-54; sem oráculo separado: o limite numérico está no próprio critério | exit 0; total 5631 ≤ 5635 | APPROVED |
| AC-09 | `0e7a09e044cb1b07ca223d8460bda81bc438e12122a0869dab4eb4141e28d9c9` | `python3 sdd/tools/sddtask.py evidence --task SDD-AJUSTES-20261124 --check --require-all` (pelo escritor do registro, depois do `--write`) | I-55, I-56 | exit 0; `0 problema(s) em 67 verificação(ões)`; a cópia sem `.local/` (AC-13 de SDD-ENXUTO r2) também passa | APPROVED |
| AC-10 | `44d0dbf5e7f8cfc02443b1a5ce80230fba8b65c0ed28533bda2fbafe31eb7100` | `python3 -m unittest discover -s sdd/tools/tests` (mais `-v`) e mutantes M2 e M2b em cópias (diffs e saídas no log) | I-40, I-41, I-57 | real: exit 0, 69 OK, com `test_concluded_task_tolerates_input_drift_after_closure_only` e `test_concluded_task_still_rejects_inputs_never_hashed` OK; M2 (`"malformed"` em `POST_CLOSE_DRIFT`) sobrevive e é equivalente (a guarda de SHA já recusa hash malformado); M2b (M2 sem a guarda) morre com `FAILED (failures=4)` | APPROVED |

### 9. Fechamento

- Documentação: sem impacto: esta revisão só reobserva os ACs; as mudanças de documentação estão na r2 de SDD-ENXUTO-20261123
- `sdd/project.md`: sem mudança
- Inputs da seção 8 alterados no fechamento: nenhum (`evidence --check --require-all` exit 0, 67 verificações)
- Checks de governança: os do AC-06 (validate, check-ox, run-tests e `scripts/tests`, exit 0) e a cópia sem `.local/` exit 0
- Pendências: verificação completa via Toolbox não rodou (não autorizada); Ruff e Bandit não instalados. Os logs antigos em `.local/tasks/SDD-AJUSTES-20261124/` não são mais citados e podem ser apagados. Nada em stage nem commitado.
- Estado final: concluída
