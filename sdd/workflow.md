# Workflow do Ox

Contrato de execução do Ox (GOV-02). Cada etapa diz **o que** entrega e **quando** está pronta; o
**como** técnico vem da skill. Permissões: POL-10 e
[AGENTS.md](../AGENTS.md#permissões-que-exigem-pedido-explícito).

## Rotas

Toda etapa é contabilizada; a rota muda o método, não a existência da etapa. Etapa que não se
aplica aparece como `NOT APPLICABLE — <motivo em uma linha>`.

| Rota | Quando | Registro |
|---|---|---|
| **Consulta** | Pergunta, explicação, diagnóstico ou status, sem alterar arquivos do projeto | Nenhum arquivo e nenhuma skill obrigatória. A resposta cita fontes e limites |
| **Local** | Objetivo e aceite claros, superfície e consumidores conhecidos, mudança reversível, sem risco material | Seções 1, 2, 7, 8 e 9; seções 3, 5 e 6 em `NOT APPLICABLE`; seção 4 só com **Skills lidas** |
| **Completa** | Decisão material em aberto, mudança de contrato/autorização, dados persistidos, concorrência, migração, compatibilidade ou recuperação incerta | Todas as seções |

Risco material é o que pode alterar autorização, evidência/gates, integridade, concorrência,
migração, compatibilidade ou recuperação; tamanho do diff não classifica e incerteza relevante
conta como risco. Risco novo reclassifica para a rota Completa (GOV-03).

## Identificação e revisões

`<ID>` = `<TEMA>-<AAAAMMDD>` em maiúsculas, ex.: `IDE-SHELL-20261123`; sufixo `-2`, `-3` se
repetir no mesmo dia. Correção do usuário sobre o **mesmo escopo** é uma revisão `r2`, `r3` no
mesmo arquivo. Escopo novo (objetivo ou requisito novo) é task nova, que cita a anterior.
`python3 sdd/tools/sddtask.py new --task <ID> --route <Local|Completa> --title "<título>"` cria o
registro da rota a partir do [template](templates/task.md) e nunca sobrescreve um existente.

## Etapas

Cada etapa preenche a seção de mesmo número do registro; não avance sem o gate. Os blocos agrupam
a leitura; cada gate continua valendo sozinho.

| Bloco (papel) | Etapa | Gate |
|---|---|---|
| A. Entender (raiz) | 0. Entrada | escopo autorizado identificado no pedido ou em `project.md` |
| | 1. Prompt | cinco divisões, regra de conclusão, AC com método e esperado ou `PENDENTE: Q-n` |
| | 2. Esclarecer | nenhum AC `PENDENTE` usado pela etapa seguinte |
| B. Planejar (planejador) | 3. Especificar | todo AC liga-se a um REQ; todo REQ tem AC |
| | 4. Planejar | todo REQ tem decisão; nenhuma decisão viola a constituição |
| | 5. Itens | todo item tem teste, condição de pronto e skill; todo D é coberto |
| | 6. Coerência | matriz sem falha (exit 0) |
| C. Executar (implementador) | 7. Executar | teste de cada item passando, ou falha registrada; documentação atualizada |
| D. Validar (verificador observa; escritor do registro grava) | 8. Validar | todo AC com estado; evidência atual para todos (exit 0) |
| E. Fechar (raiz ou orquestrador) | 9. Fechar | regra de conclusão cumprida |

### 0. Entrada

Ler [constitution.md](constitution.md) e [project.md](project.md); conferir `git status` (POL-05).
Outras fontes só quando a task as toca.

### 1. Prompt

Converter o pedido, com a skill `prompt`, nas cinco divisões do template:

1. `1 - Objetivos`: resultado pretendido, público e insumos.
2. `2 - Requisitos`: comportamento e entregáveis concretos.
3. `3 - Restrições`: guardrails — o que **não** fazer, escopo, permissões, o que preservar.
4. `4 - Critérios de Aceitação`: uma linha por critério,
   `- AC-01: <condição observável> | método: <comando ou inspeção> | esperado: <resultado>`.
5. `5 - Entrega`: arquivos/saídas e a regra de conclusão do template.

Substituições obrigatórias de termos subjetivos (GOV-09):

| Proibido | Escreva em vez disso |
|---|---|
| bonito, elegante, moderno, limpo | aderência a seção nomeada de `DESIGN.md`/`surfaces.md`; contraste ≥ valor; tokens usados |
| sem erros, robusto, estável | quais testes/checks, com exit 0; quais casos de erro são cobertos |
| rápido, performático, leve | operação, cenário, métrica, unidade e limite (ex.: p95 < 200 ms em N itens) |
| completo, tudo, exaustivo | lista enumerada do que entra |
| simples, intuitivo, fácil | número de passos/cliques, atalho de teclado, estado vazio/erro definidos |
| adequado, correto, bom | o oráculo que decide (teste, spec, comando) |

Não invente números. Métrica, método ou esperado essencial e desconhecido vira AC provisório,
`- AC-02: <condição> | PENDENTE: Q-1`, com a pergunta na seção 2.

### 2. Esclarecer

Perguntas da GOV-09: 1 a 3 por rodada, com opções quando útil, registradas com a resposta.
Lacuna menor vira `SUPOSIÇÃO:` rotulada. Cada resposta reescreve o AC pendente na forma completa.
O trabalho que não depende de AC pendente segue. A etapa 8 nunca começa com AC pendente.

### 3. Especificar (o quê e por quê)

Registrar motivação, atores, cenários normais e rejeitados, requisitos `REQ-n` e ligar cada AC
a um REQ (`- AC-01 → REQ-01`). Spec viva (GOV-10): criar ou atualizar
`sdd/specs/<capacidade>.md` ([template](templates/spec.md)), citá-la na task e registrar a task na
tabela de estado da spec.

### 4. Planejar (decisões técnicas)

Arquitetura, modelo de dados, módulos e interfaces, bibliotecas e versões. Cada decisão `D-n`:
escolha, alternativa descartada e motivo, REQ atendido.

### 5. Quebrar em itens de trabalho

Cada item `T-n`: decisão atendida, arquivos e seu dono (um por arquivo), dependências, teste que o
verifica (cita os AC), condição de pronto e skill (nome do catálogo entre crases ou
`nenhuma: <motivo>`). Cada item pode ser implementado e testado sozinho.

### 6. Verificar coerência

`python3 sdd/tools/validate.py --root . --task <ID> --matrix` deriva a matriz `REQ → D → T → AC`
das seções 3–5 e falha em órfão, item sem teste ou decisão que não atende o REQ do AC testado.
A seção 6 registra o exit e os conflitos com POL/GOV/RQ; a matriz não é redigida à mão.

### 7. Executar

Implementar item a item, na ordem das dependências, com a skill do item. Registrar por item:
arquivos alterados, teste executado, exit code, falhas e tentativas abandonadas. O último item
atualiza a documentação afetada e `sdd/project.md`, ou registra o motivo de não impacto.

### 8. Validar

1. O verificador (na rota Local, a raiz) executa os métodos e devolve, por AC, método executado,
   inputs com papel, resultado observado e estado, sem hashes, além de comandos, exits e lacunas.
2. O escritor do registro grava as linhas, roda `python3 sdd/tools/sddtask.py evidence --task <ID>`
   com `--write` e depois com `--check --require-all`; exit 1 devolve os ACs indicados ao passo 1.

- Inputs mínimos: registre só o que sustenta o AC — o `material` julgado, o `oráculo` que decide
  (teste, script ou referência) e `configuração` (lockfile, perfil, flags) apenas quando altera o
  resultado. Um `I-n` serve a vários ACs da mesma camada; a saída de `evidence` mostra o próximo
  livre. Input derivado (lista gerada) registra o comando e o sha256 da saída. O próprio registro
  da task não é input.
- Célula de caminho com um único `caminho` entre crases (relativo à raiz) ou um link é conferida
  por bytes; outra forma não é verificável. Método e resultado nunca ficam vazios.
- `--write` preenche só células vazias ou `<…>`, com o sha256 da linha do AC e dos bytes de cada
  input; nunca renova hash registrado. `--check` sai com 1 se algum
  estiver desatualizado; `--require-all` exige observação atual para cada AC.
- Estados (GOV-05): `NOT APPLICABLE` exige motivo. APPROVED/REJECTED citam ao menos um input
  `material` e um `oráculo`, ou `sem oráculo separado: <motivo>`.

### 9. Fechar

1. Registrar a documentação e o `sdd/project.md` atualizados na etapa 7.
2. Se a task mudou `AGENTS.md`, `sdd/`, `.codex/` ou skills: rodar
   `python3 sdd/tools/validate.py --root .` e `python3 tools/governance/scripts/run-tests.py`;
   exit diferente de 0 impede a conclusão.
3. Repetir `evidence --check --require-all` com exit 0.
4. Marcar `Estado:` no cabeçalho e responder ao usuário com o resultado, os checks realmente
   executados e as pendências.

**Regra de conclusão:** a da divisão `5 - Entrega`. Se um AC obrigatório não está
APPROVED/NOT APPLICABLE, a task é reportada como **incompleta** ou **bloqueada**, com a condição
que falta e o passo de retomada.

## Evidência e retomada

- Log ou artefato citado na seção 8 é versionado em `sdd/tasks/<ID>/`, até 1 MiB por arquivo;
  acima disso, a seção guarda comando, sha256 e motivo. `.local/tasks/<ID>/` (ignorado pelo Git)
  só guarda saída não citada; o `validate.py` reprova input ali.
- Observação substituída (GOV-05) vai, com o motivo, para uma subseção `### … (obsoletas)`.
- Após o fechamento, correções entram ao final como `## Revisão rN — <data>`, com uma linha
  `Motivo:` e as etapas afetadas como subseções `### <n>. <nome>`. Por ID vale a revisão mais
  recente. IDs `I-n` são únicos no registro inteiro. Blocos cercados e comentários HTML não contam
  como estrutura.
- Retomada (GOV-03, GOV-05): `evidence --check` lista os ACs a reobservar, que ficam UNVERIFIED
  até a nova observação. Em task concluída, input alterado depois do fechamento é retomada, não
  falha do `validate.py`.
- Revisão externa (ex.: Claude) grava `sdd/tasks/<ID>.review.md`; o dono responde com uma
  revisão `rN` no registro.

## Skills

Catálogo e mapa etapa → skill da GOV-04, com as skills em `.codex/skills/<nome>/SKILL.md`.

- Uma skill primária por assunto; auxiliares só para questão distinta, sem carregamento recursivo.
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

Perfis em `.codex/config.toml` (raiz) e `.codex/agents/ec_*.toml`, separados do Agent Runtime do
produto e carregados por sessão nova `codex --strict-config`. Modelo e esforço vivem só nos TOML;
cada perfil aponta para o seu papel abaixo.

| Papel | Perfil | Alternativa e quando |
|---|---|---|
| Raiz (controlador) | sessão raiz | — |
| Orquestrador | `ec_orquestrador_normal` | `ec_orquestrador_alta` ([Triagem](#triagem)) |
| Planejador | `ec_planejador` | — |
| Implementador | `ec_implementador` | `ec_implementador_extra_alto` ([Papel implementador](#papel-implementador)) |
| Verificador | `ec_verificador` | — |

### Triagem

Feita pela raiz, por ambiguidade, alcance, risco, reversibilidade, dependências e
verificabilidade ([Rotas](#rotas)).

| Situação | Quem executa |
|---|---|
| Rota Consulta | A raiz, diretamente, com fontes e limites |
| Rota Local | A raiz, no escopo autorizado, com verificação focada |
| Rota Completa sem risco material | `ec_orquestrador_normal` |
| Risco material | `ec_orquestrador_alta` |
| Contexto independente indisponível | Concluir análise e plano; bloquear a execução dependente e registrar a condição de retomada |

### Delegação

- Vagas: a raiz mais `max_concurrent_threads_per_session` de `.codex/config.toml`, contando o
  orquestrador; limite menor do host prevalece. Com 1 vaga, implementar e verificar em sequência,
  cada um em contexto novo.
- Toda delegação recebe por escrito: ID da task, pedido e permissões, itens `T-n` com a skill,
  arquivos de que é dono, critérios, fatos e hipóteses, resultado esperado. Não depender de
  histórico implícito.
- Paralelizar só itens com escrita disjunta. O orquestrador (ou a raiz, na rota Local) é o único
  escritor de `sdd/tasks/<ID>.md`.
- Especialistas não subdelegam. O mesmo perfil não torna independente um contexto que implementou.
  Não finalizar com trabalho delegado ativo.

### Papel orquestrador

Recebe a triagem e coordena as etapas 3–9 até aceite ou bloqueio: atribui itens e arquivos,
integra os retornos (etapa 8, passo 2), reavalia a rota e escolhe o perfil do implementador. Não
cria outro orquestrador nem simula troca de modelo; para trocar de perfil (ex.: risco material
novo no perfil normal), devolve à raiz um resumo de continuidade.

### Papel planejador

Etapas 3–6: lê autoridades, contratos, consumidores e as skills do assunto; devolve REQ, decisões
com alternativas, itens com donos, dependências, testes e skill, e a saída da etapa 6. Não edita
código nem decide política nova.

### Papel implementador

Etapa 7: edita só os arquivos atribuídos (POL-05) e devolve arquivos, comandos, exits e
pendências. Não altera critérios nem evidência. Item que exige esforço extra alto volta com a
evidência da dificuldade e um resumo de continuidade; o orquestrador usa o perfil extra alto só no
item cuja dificuldade registrou.

### Papel verificador

Revisão, testes e etapa 8 (passo 1), em contexto independente do implementador: examina o código
real contra os REQ (consumidores, invariantes, segurança, falhas) com `software-testing` e a skill
do item, usa oráculos independentes e confronta cada AC com a evidência. Não
edita implementação, critérios, entradas do gate nem o registro; rejeição volta ao orquestrador.
