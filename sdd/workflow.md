# Workflow do Ox

Único contrato de execução (GOV-02): rotas, etapas, skills, agentes, evidência e fechamento.
Cada etapa diz **o que** entrega e **quando** está pronta; o **como** técnico é delegado à skill
indicada. Autorização vem do pedido do usuário e do ambiente, nunca deste arquivo (POL-10).
Ações locais reversíveis e autorizadas seguem sem pedir confirmação rotineira.

## Rotas

Toda etapa é contabilizada; a rota muda o método, não a existência da etapa. Etapa que não se
aplica aparece como `NOT APPLICABLE` com o motivo em uma linha.

| Rota | Quando | Registro |
|---|---|---|
| **Consulta** | Pergunta, explicação, diagnóstico ou status, sem alterar arquivos do projeto | Nenhum arquivo e nenhuma skill obrigatória. A resposta cita fontes e limites |
| **Local** | Objetivo e aceite claros, superfície e consumidores conhecidos, mudança reversível, sem risco material | `sdd/tasks/<ID>.md` com as seções 1, 2, 7, 8 e 9 e a tabela **Skills lidas** (no mínimo `prompt`); seções 3–6 `NOT APPLICABLE` com motivo |
| **Completa** | Decisão material em aberto, mudança de contrato/autorização, dados persistidos, concorrência, migração, compatibilidade ou recuperação incerta | `sdd/tasks/<ID>.md` com todas as seções; spec viva em `sdd/specs/` quando a capacidade é duradoura |

Risco material é o que pode alterar autorização, evidência/gates, integridade, concorrência,
migração, compatibilidade ou recuperação. Tamanho do diff não classifica. Risco material exige
orquestração alta e verificação em contexto independente do implementador ([Agentes](#agentes)).
Risco novo reclassifica para a rota Completa, preservando o trabalho válido.

## Identificação e revisões

`<ID>` = `<TEMA>-<AAAAMMDD>` em maiúsculas, ex.: `IDE-SHELL-20261123`; sufixo `-2`, `-3` se
repetir no mesmo dia. Correção do usuário sobre o **mesmo escopo** é uma revisão `r2`, `r3` no
mesmo arquivo. Escopo novo (objetivo ou requisito novo) é task nova, que cita a anterior.

## Etapas

Cada etapa preenche a seção de mesmo número do [template](templates/task.md); não avance sem o gate.

| Etapa | Saída | Skill | Papel | Gate |
|---|---|---|---|---|
| 0. Entrada | — | — | raiz | escopo autorizado identificado no pedido ou em `project.md` |
| 1. Prompt | seção 1 | `prompt` | raiz | cinco divisões, regra de conclusão, AC com método e esperado ou `PENDENTE: Q-n` |
| 2. Esclarecer | seção 2 | `prompt` | raiz, com o usuário | nenhum AC `PENDENTE` usado pela etapa seguinte |
| 3. Especificar | seção 3 e spec viva | `domain-modeling` se houver conceito novo | planejador | todo AC liga-se a um REQ; todo REQ tem AC |
| 4. Planejar | seção 4 | skill do assunto | planejador | todo REQ tem decisão; nenhuma decisão viola a constituição |
| 5. Itens | seção 5 | `software-testing` | planejador | todo item tem teste, condição de pronto e skill; todo D é coberto |
| 6. Coerência | seção 6 | — | planejador | `validate.py --root . --task <ID> --matrix` exit 0 |
| 7. Executar | seção 7 | skill do item | implementador | teste de cada item passando, ou falha registrada; documentação atualizada |
| 8. Validar | seção 8 | `software-testing` | verificador observa; escritor do registro grava | todo AC com estado; `evidence --check --require-all` exit 0 |
| 9. Fechar | seção 9 | — | raiz ou orquestrador | regra de conclusão cumprida |

### 0. Entrada

Ler [constitution.md](constitution.md) e [project.md](project.md); conferir `git status` para
preservar mudanças de terceiros (POL-05). Outras fontes só quando a task as toca.

### 1. Prompt

Converter o pedido num prompt com exatamente estas divisões:

1. `1 - Objetivos`: resultado pretendido, público e insumos.
2. `2 - Requisitos`: comportamento e entregáveis concretos.
3. `3 - Restrições`: guardrails — o que **não** fazer, escopo, permissões, o que preservar.
4. `4 - Critérios de Aceitação`: uma linha por critério, no formato
   `- AC-01: <condição observável> | método: <comando ou inspeção> | esperado: <resultado>`.
5. `5 - Entrega`: arquivos/saídas e a **regra de conclusão**: "a task está concluída quando
   AC-01…AC-n estiverem APPROVED ou NOT APPLICABLE com motivo, e a seção 9 estiver preenchida".

Termos subjetivos são proibidos sem métrica (GOV-09). Substituições obrigatórias:

| Proibido | Escreva em vez disso |
|---|---|
| bonito, elegante, moderno, limpo | aderência a seção nomeada de `DESIGN.md`/`surfaces.md`; contraste ≥ valor; tokens usados |
| sem erros, robusto, estável | quais testes/checks, com exit 0; quais casos de erro são cobertos |
| rápido, performático, leve | operação, cenário, métrica, unidade e limite (ex.: p95 < 200 ms em N itens) |
| completo, tudo, exaustivo | lista enumerada do que entra |
| simples, intuitivo, fácil | número de passos/cliques, atalho de teclado, estado vazio/erro definidos |
| adequado, correto, bom | o oráculo que decide (teste, spec, comando) |

Não invente números. Métrica, método ou esperado essencial e desconhecido vira AC provisório,
`- AC-02: <condição> | PENDENTE: Q-1`, com a pergunta registrada na seção 2.

### 2. Esclarecer

Lacuna ou contradição que mudaria o resultado vira pergunta ao usuário: 1 a 3 por rodada, com
opções quando útil. Registrar pergunta e resposta. Lacuna menor vira `SUPOSIÇÃO:` rotulada. Cada
resposta reescreve o AC pendente na forma completa. Trabalho que depende de AC pendente fica
bloqueado; o independente segue. A etapa 8 nunca começa com AC pendente.

### 3. Especificar (o quê e por quê)

Registrar motivação, atores, cenários normais e rejeitados, requisitos `REQ-n` e ligar cada AC
a um REQ (`- AC-01 → REQ-01`). Capacidade duradoura do produto: criar ou atualizar
`sdd/specs/<capacidade>.md` ([template](templates/spec.md)) e citá-la na task.

### 4. Planejar (decisões técnicas)

Arquitetura, modelo de dados, módulos e interfaces, bibliotecas e versões ([Skills](#skills)).
Cada decisão `D-n`: escolha, alternativa descartada e motivo, REQ atendido. A tabela **Skills
lidas** (caminho, motivo, contribuição) existe em toda rota com registro (GOV-04). Decisão de
política ou escolha pendente da RQ-03 exige ADR em `docs/decisions/`.

### 5. Quebrar em itens de trabalho

Cada item `T-n`: decisão atendida, arquivos (um dono por arquivo), dependências, teste que o
verifica (cita os AC), condição de pronto e skill (nome do catálogo entre crases, registrada em
**Skills lidas**, ou `nenhuma: <motivo>`). Cada item pode ser implementado e testado sozinho.

### 6. Verificar coerência

`python3 sdd/tools/validate.py --root . --task <ID> --matrix` deriva a matriz `REQ → D → T → AC`
das seções 3–5 e falha em órfão, item sem teste ou decisão que não atende o REQ do AC testado.
A seção 6 registra o exit e os conflitos com POL/GOV/RQ; a matriz não é redigida à mão.

### 7. Executar

Implementar item a item, na ordem das dependências, com a skill do item. Registrar por item:
arquivos alterados, teste executado, exit code, falhas e tentativas abandonadas. Não enfraquecer
critério para passar. O último item atualiza a documentação afetada e `sdd/project.md`, ou
registra o motivo de não impacto.

### 8. Validar

Tabelas de inputs e de ACs do [template](templates/task.md). Sequência: (1) o verificador
(na rota Local, a raiz) executa os métodos e devolve as linhas sem hashes; (2) o escritor do
registro grava as linhas, roda `--write` e depois `--check --require-all`; exit 1 devolve os ACs
indicados ao passo 1.

- Papéis: `material` (o que é avaliado), `oráculo` (teste, script ou referência que decide),
  `configuração` (lockfile, perfil, flags). Input derivado (lista gerada) registra o comando
  e o sha256 da saída. O próprio registro da task não é input.
- Hashes por ferramenta, nunca à mão:
  `python3 sdd/tools/sddtask.py evidence --task <ID> --write` preenche as células vazias (ou `<…>`)
  com o sha256 da linha do AC e dos bytes de cada input com caminho entre crases; nunca renova hash
  já registrado. `--check` sai com 1 se algum estiver desatualizado; `--require-all` exige
  observação atual para cada AC.
- Estados (GOV-05): APPROVED, REJECTED, UNVERIFIED, INCONCLUSIVE, NOT APPLICABLE (este exige
  motivo). APPROVED/REJECTED citam ao menos um input `material` e um `oráculo`, ou
  `sem oráculo separado: <motivo>`. Rota Completa: validação pelo verificador independente.

### 9. Fechar

1. Registrar a documentação e o `sdd/project.md` atualizados na etapa 7.
2. Se a task mudou `AGENTS.md`, `sdd/`, `.codex/` ou skills: rodar
   `python3 sdd/tools/validate.py --root .` e `python3 tools/governance/scripts/run-tests.py`;
   exit diferente de 0 impede a conclusão.
3. `sddtask.py evidence --task <ID> --check --require-all` exit 0.
4. Marcar `Estado:` no cabeçalho e responder ao usuário com o resultado, os checks realmente
   executados e as pendências.

**Regra de conclusão:** a regra da divisão `5 - Entrega` está cumprida. Se um AC obrigatório não
está APPROVED/NOT APPLICABLE, a task é reportada como **incompleta** ou **bloqueada**, com a
condição que falta e o passo de retomada.

## Evidência e retomada

- Log ou artefato citado na seção 8 é versionado em `sdd/tasks/<ID>/`, até 1 MiB por arquivo;
  acima disso, a seção guarda comando, sha256 e motivo. `.local/tasks/<ID>/` (ignorado pelo Git)
  só guarda saída não citada; o `validate.py` reprova input ali.
- Observação cujo input mudou não é editada: a nova é acrescentada e a antiga vai para
  `### … (obsoletas)`. Check estrutural com exit 0 prova estrutura, não comportamento.
- Após o fechamento, correções entram ao final como `## Revisão rN — <data>`, com as etapas
  afetadas como subseções `### <n>. <nome>`. Por ID vale a revisão mais recente. IDs `I-n` são
  únicos no registro inteiro. Blocos cercados e comentários HTML não contam como estrutura.
- Retomada: `sddtask.py evidence --task <ID> --check`; AC cujo critério ou input mudou volta a
  UNVERIFIED até nova observação. Em task concluída, input alterado depois do fechamento é
  retomada, não falha do `validate.py`.
- Revisão externa (ex.: Claude) grava `sdd/tasks/<ID>.review.md`;
  o dono responde com uma revisão `rN` no registro.

## Skills

As skills ficam em `.codex/skills/<nome>/SKILL.md`; esta seção é o único catálogo e mapa (GOV-04).

- Ler o `SKILL.md` real antes de usar e registrá-lo em **Skills lidas**; menção não é uso.
- Uma skill primária por assunto; auxiliares só para questão distinta, sem carregamento recursivo.
- A skill define o método; política e gates são deste workflow, que prevalece em conflito.
- Skill indisponível: registrar a lacuna; o AC dependente fica UNVERIFIED.

| Skill | Etapa | Usar quando |
|---|---|---|
| `prompt` | 1–2 | Toda task com registro; criar ou revisar um prompt |
| `domain-modeling` | 3 | Conceitos, invariantes ou estados de domínio novos |
| `software-architecture` | 4 | Alternativa estrutural, fronteira entre componentes, migração |
| `software-design` | 4 | Responsabilidades, APIs internas, acoplamento |
| `database-engineering` | 4 | Esquema, persistência, migração de dados |
| `software-evolution` | 4 | Adicionar, atualizar ou remover dependência; depreciação |
| `software-delivery` | 4, 7 | Build, pipeline, empacotamento e release |
| `software-testing` | 5, 7, 8 | Caminho feliz e infeliz, oráculos, sensibilidade do teste |
| `rust` | 4, 7 | Código Rust |
| `iced-engineering` | 4, 7 | Interface Iced nativa |
| `design-review` | 4, 8 | Crítica de fluxo e superfície visual (RQ-01) |
| `design-system` | 4, 7 | Tokens e componentes compartilhados |
| `application-security` | 4, 7, 8 | Segurança, permissões, entrada não confiável |
| `api-testing` | 5, 8 | Contratos HTTP/IPC testáveis |
| `performance-engineering` | 4, 8 | Desempenho medido |
| `reliability-engineering` | 4 | Falhas, retomada, degradação |
| `observability-and-diagnostics` | 4, 7 | Logs, métricas, diagnóstico |
| `distributed-systems` | 4 | Processos com falhas independentes, ordenação, replay; IPC por si só não basta |
| `plugin-protocol-engineering` | 4, 7 | Protocolo de plugins |
| `agent-runtime-engineering` | 4, 7 | Runtime de agentes |
| `autonomous-verification-engineering` | 4, 7 | Verificação autônoma |
| `workspace-integrity-engineering` | 4, 7 | Integridade do workspace, concorrência de escrita |
| `code-context-engineering` | 4, 7 | Contexto de código |
| `code-knowledge-graph-engineering` | 4, 7 | Grafo de conhecimento de código |
| `tool-output-engineering` | 4, 7 | Saída de ferramentas, parsers, compactação |
| `agent-usage-accounting` | 4, 7 | Contabilidade de uso de agentes |
| `ai-engineering` | 4, 7 | Aplicação de IA, RAG, avaliação de modelo |
| `engineering-productivity` | 4, 8 | Avaliação de fluxo humano com baseline; não benchmark do binário |
| `technical-documentation` | 7 | Documentação afetada além do registro |
| `readme-lifecycle-engineering` | 7 | README de entrada |
| `commit-governance` | fora do fluxo | Só com pedido explícito de commit ou tag |

Fora do perfil: `gleam`, `kotlin` e `postgresql` não são instaladas.

## Agentes

`.codex/config.toml` e `.codex/agents/ec_*.toml` (6 perfis), separados do Agent Runtime do
produto. Carregar com sessão nova `codex --strict-config`; TOML não é sandbox nem permissão.

| Papel | Perfil normal | Perfil para risco material | Etapas |
|---|---|---|---|
| Raiz (controlador) | sessão raiz: Sol 6.1 / medium | a mesma | 0–2, triagem, 9 |
| Orquestrador | `ec_orquestrador_normal`: Astra 6 / medium | `ec_orquestrador_alta`: Astra 6 / high | coordena 3–9 |
| Planejador | `ec_planejador`: Sol 6.1 / high | o mesmo | 3–6 |
| Implementador | `ec_implementador`: Sol 6.1 / high | `ec_implementador_extra_alto` (xhigh) só com dificuldade demonstrada e motivo registrado | 7 |
| Verificador | `ec_verificador`: Sol 6.1 / high | o mesmo | revisão, testes e 8 |

### Triagem

Feita pela raiz, por ambiguidade, alcance, risco, reversibilidade, dependências e
verificabilidade; tamanho não decide e incerteza relevante conta como alta.

| Situação | Quem executa |
|---|---|
| Rota Consulta | A raiz, diretamente, com fontes e limites |
| Rota Local | A raiz, no escopo autorizado, com verificação focada |
| Rota Completa sem risco material | `ec_orquestrador_normal` |
| Risco material | `ec_orquestrador_alta`; verificação em contexto independente do implementador |
| Contexto independente indisponível | Concluir análise e plano; bloquear a execução dependente e registrar a condição de retomada |

### Delegação

- Limite: 4 agentes na árvore (raiz, orquestrador e até 2 especialistas); limite menor do host
  prevalece. Com 1 vaga, implementar e verificar em sequência, cada um em contexto novo.
- Toda delegação recebe por escrito: ID da task, pedido e permissões, itens `T-n` com a skill,
  arquivos de que é dono, critérios, fatos e hipóteses, resultado esperado. Não depender de
  histórico implícito.
- Um dono por arquivo; paralelizar só itens com escrita disjunta. O orquestrador (ou a raiz, na
  rota Local) é o único escritor de `sdd/tasks/<ID>.md` e consolida os retornos.
- Especialistas não subdelegam. O orquestrador não cria outro orquestrador; para trocar de perfil,
  devolve à raiz um resumo de continuidade.
- Relato do implementador é pista, não prova. O mesmo perfil não torna independente um contexto
  que implementou. Não finalizar com trabalho delegado ativo.

### Papel orquestrador

Recebe a triagem e coordena a task até aceite ou bloqueio: atribui itens e arquivos, integra os
retornos no registro (etapa 8, passo 2), reavalia a rota e escolhe o implementador extra alto
só com dificuldade demonstrada.

### Papel planejador

Etapas 3–6: lê autoridades, contratos e consumidores; devolve REQ, decisões com alternativas,
itens com donos, dependências, testes e skill, e o resultado de
`validate.py --root . --task <ID> --matrix`. Não edita código nem decide política nova.

### Papel implementador

Etapa 7: usa a skill do item, edita só os arquivos atribuídos, confere precondições antes de
escrever, roda os testes dos itens e devolve arquivos, comandos, exits e pendências. Não altera
critérios nem evidência.

### Papel verificador

Revisão, testes e etapa 8, em contexto independente do implementador: examina o código real
contra os REQ (consumidores, invariantes, segurança, falhas) com `software-testing` e a skill do
item, executa os cenários com oráculos independentes, confronta cada AC com a evidência e devolve
as linhas da seção 8 sem hashes. Não edita implementação, critérios nem o registro; rejeição volta
ao orquestrador.

## Fora deste contrato

Ações que exigem pedido explícito (commit, publicação, downloads, verificação completa) estão
em [AGENTS.md](../AGENTS.md#permissões-que-exigem-pedido-explícito).
