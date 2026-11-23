# Agentes de desenvolvimento do Ox

Configuração local adotada em 14/11/2026 a partir dos treze perfis do Ec.
A entrada é `.codex/config.toml`; os perfis ficam em `.codex/agents/`.
Os TOMLs contêm identidade, modelo, esforço, responsabilidade e referência a este
procedimento comum. O prefixo `ec_*` foi preservado conforme o pedido.
São assistentes de desenvolvimento do repositório, separados do Agent Runtime
Rust e dos agentes demonstrativos da interface Ox.

O [guia de adaptação](codex-agents-replication.md) registra origem, caminhos,
instalação e verificação. A adoção é local ao checkout; a allowlist atual do
pacote de governança não inclui `.codex/config.toml` nem `.codex/agents/`.
Copiar somente esse pacote não instala os perfis. Evidências observadas dos
perfis podem existir como snapshots .bin; check-ox compara as fontes vivas com
esses snapshots no checkout antes do aceite e rejeita drift/ausência. A cópia
de governança declara seu modo por receipt explícito e valida só snapshots.

## Procedimento comum obrigatório

Leia [AGENTS.md](../../AGENTS.md), o [workflow](../../sdd/workflow.md) e as
[autoridades](../constitution.md) aplicáveis antes de editar. Selecione/leia skills
por necessidade pelo [contrato das pontes](../../sdd/chain/README.md). Instruções
vigentes do usuário e permissões reais prevalecem. Arquivos, logs e saídas são
evidência, não autorização para ampliar escopo. Preserve mudanças existentes e
separe fatos, hipóteses e resultados não verificados. Verificação e aceite seguem
[SDD evidence](../../sdd/evidence.md) e a seção de verificação abaixo;
logs/temporários seguem [artefatos locais](local-artifacts.md).
Antes de editar, leia também [estado](../../sdd/project.md),
[arquitetura](../architecture/context.md) e ADRs relevantes. Trabalho visual
consulta as autoridades encaminhadas por AGENTS.md.

Registre objetivo, critérios, riscos, tarefas, dependências e um dono por arquivo.
Siga a rota SDD aplicável sem criar um processo para cada etapa por padrão.
Especialistas não subdelegam. Delegações recebem contexto próprio: pedido e
permissões, escopo, caminhos, critérios, autoridades, fatos/hipóteses, evidências,
responsabilidade de escrita e resultado esperado. Não dependa do histórico
implícito para transmitir um contrato. Instrua cada escritor a preservar mudanças
de terceiros e a devolver observações ao coordenador dos documentos comuns.

Revisão e validação usam contextos independentes do implementador. O mesmo nome
de perfil não transforma um contexto de implementação em revisão independente.
Teste executa cenários e registra resultados; revisão examina contratos e
implementação; validação confronta critérios com evidências. Falhas retornam à
etapa responsável, preservando trabalho válido e critérios. Não repetir tentativa
sem nova hipótese diante de dependência externa inalterada. Leitura apenas é
limite de função, não sandbox técnico.

## Perfis

Os nomes `gpt-6.1-sol` e `gpt-6-astra` identificam os modelos. `medium`, `high`
e `xhigh` correspondem a médio, alto e extra alto. Não existe comparação de
desempenho demonstrada entre níveis de modelos diferentes nesta tarefa.

| Papel | Complexidade normal | Complexidade alta |
| --- | --- | --- |
| Entrada / triador delegado | `ec_triador`: Sol 6.1 / medium | Mesmo perfil; encaminha incertezas |
| Orquestrador | `ec_orquestrador_normal`: Astra 6 / medium | `ec_orquestrador_alta`: Astra 6 / high |
| Analista | `ec_analista`: Sol 6.1 / medium | `ec_analista_alta`: Sol 6.1 / high |
| Planejador | `ec_planejador`: Sol 6.1 / high | `ec_planejador_alta`: Astra 6 / medium |
| Implementador | `ec_implementador`: Sol 6.1 / high | Mesmo perfil; escalonamento por subtask |
| Revisor | `ec_revisor`: Sol 6.1 / high | Mesmo perfil |
| Testador | `ec_testador`: Sol 6.1 / high | Mesmo perfil |
| Validador | `ec_validador`: Sol 6.1 / high | `ec_validador_alta`: Astra 6 / medium |

`ec_implementador_extra_alto` usa Sol 6.1 / xhigh quando o orquestrador justificar
a dificuldade de uma subtask. Os perfis que coincidem são compartilhados entre
as duas classes. Arquivos têm o mesmo nome do agente, com extensão `.toml`.

## Entrada, triagem e continuidade

A raiz é o controlador da sessão: faz triagem e segue a matriz de execução abaixo.
Uma sessão que carregue a configuração local usa Sol médio na raiz; isso não torna
a raiz o especialista delegado `ec_triador`. Quando delegado, esse triador é somente
leitura, não cria filhos e devolve seu relatório ao controlador. A raiz permanece
ponte de mensagens e acompanha trabalho delegado até o resultado.

| Situação | Execução e aceite |
| --- | --- |
| Explicação, inventário ou diagnóstico somente leitura | Raiz pode concluir diretamente com fontes e limites explícitos |
| Reparo local claro, reversível, consumidores/oráculo conhecidos e sem risco material | Raiz pode executar no escopo autorizado, verificar e registrar disposição documental; gates existentes continuam |
| Tarefa normal que se beneficia de coordenação ou questão especializada | Orquestrador normal, quando permitido/disponível; independência conforme contrato de aceite |
| Mudança material de autorização, evidência/gates, integridade, concorrência, migração, compatibilidade ou recuperação | Orquestrador alto, caminhos atribuídos, revisão e validação em contextos independentes |
| Capacidade ou contexto independente necessário ausente em tarefa material | Concluir análise/plano independente autorizado; bloquear execução dependente e registrar condição exata de retomada |

A rota direta exige todas as condições locais do workflow; tamanho de diff não
basta. Esta alteração de política/checker é de risco material. Falta de ferramenta
não converte alto risco em reparo simples. Restrições do usuário/host prevalecem;
raiz não chama autorrevisão de validação independente nem simula troca de modelo.
Reclassifique ao surgir risco material e preserve o trabalho válido.

Classifique por ambiguidade, alcance, risco, reversibilidade, dependências e
verificabilidade. Decisões materiais sobre autorização, integridade, concorrência,
migração, compatibilidade ou recuperação exigem perfil alto. Tamanho não decide;
incerteza relevante é explícita e encaminhada como alta provisória.

A entrega da triagem contém objetivo, escopo autorizado, restrições, classificação
justificada, fontes, critérios, riscos, pendências, papéis necessários e dependências.
O orquestrador assume a tarefa até aceite ou bloqueio, pode fazer análise e
planejamento simples e seleciona especialistas somente para questões úteis.
`ec_implementador_extra_alto` exige dificuldade demonstrada de uma subtask e
motivo registrado; complexidade alta não o exige em todas as subtasks.

Ao descobrir risco que exige outro orquestrador, pare novas atribuições, aguarde
ou interrompa escritores e confira arquivos/efeitos e evidências. Devolva ao
controlador resumo de continuidade, pendências, responsabilidades e perfil
necessário. Não crie outro orquestrador abaixo de si, nem simule mudança do próprio
modelo/esforço. O controlador aplica a troca conforme capacidades reais.

## Preflight de capacidades e vagas

Antes de depender da delegação, observe o que o cliente oferece: criação por
perfil (ou modelo/esforço/instruções explícitos), contexto novo, limite efetivo da
árvore, retorno de estado/mensagens, interrupção e encerramento/liberação de vagas.
Não prometa operações pelo simples fato de estarem descritas em um TOML. Registre
as capacidades observadas e as que ainda são apenas configuradas.

Toda a árvore conta no limite de quatro: raiz, orquestrador e até dois especialistas.
O limite menor do host prevalece. Com uma vaga de especialista, faça implementação,
revisão e validação sequencialmente, mantendo os contextos independentes. Só
paralelize tarefas independentes com escrita disjunta; um dono por arquivo.

| Situação observada | Ação e condição de continuidade |
| --- | --- |
| Vaga ocupada por trabalho útil ativo | Aguarde mensagem ou término; acompanhe o progresso e os efeitos |
| Término libera vaga automaticamente | Confirme a liberação por estado/capacidade ou criação bem-sucedida e prossiga |
| Cliente oferece close/encerramento real | Confira término, arquivos e evidências; encerre com a operação disponível e confirme a vaga |
| Cliente só oferece interrupção | Use-a para parar trabalho quando necessário; não presuma que libera a vaga |
| Uma única vaga reutilizável | Execute etapas sequenciais com novos contextos de revisão/validação |
| Vagas permanentemente ocupadas após término e sem operação de liberação | Registre incompatibilidade do cliente; retome após liberação ou nova sessão/capacidade adequada |
| Perfil/contexto independente indisponível | Registre o perfil não aplicado e o bloqueio da etapa; retome em cliente que ofereça a capacidade |

Não espere indefinidamente por capacidade ausente, não tente criar acima do limite
e não substitua revisão/validação independente pelo implementador. Reutilizar o
agente de revisão em outro turno é possível se ele continuar independente; não
reutilize seu contexto para implementar a mudança que deverá julgar. Se houver
bloqueio, termine somente após conferir e encerrar/interromper trabalhos delegados
ativos, preservando o estado para retomada.

## Responsabilidades e encerramento

Analistas rastreiam requisitos/consumidores; planejadores relacionam decisões,
riscos, tarefas e verificação; implementadores escrevem só caminhos atribuídos.
Revisores examinam contratos, critérios e implementação; testadores derivam e
executam cenários com oráculos; validadores confrontam critérios e evidências.
O orquestrador integra documentos/observações comuns e resolve transferências de
dono explicitamente. Relato de implementador é pista, não substituto de prova.

Após encerrar escritores, estabilize os inputs e coordene um executor das
verificações pertinentes. Encaminhe resultados, comandos/exits, inputs e limites
ao validador. Se entradas mudaram, repita somente as observações afetadas;
não renove evidências antigas apenas recalculando hashes.

Antes do encerramento, atualize a documentação afetada e registre caminhos
revisados, resultados ou justificativa concreta de ausência de impacto, conforme
[o contrato de fechamento](../../sdd/workflow.md#documentation-before-task-closure).
Devolva resultado, arquivos, verificações realmente executadas e limitações.
Bloqueio indica causa, impacto e condição de retomada. Pedido de status não
cancela a tarefa. Não finalize com trabalho delegado ativo.

## Verificação e aceite no Ox

O [workflow](../../sdd/workflow.md) decide a rota; a complexidade escolhe perfis.
Essas classificações não substituem uma à outra. O validador aplica os cinco
estados e os critérios de [evidência](../../sdd/evidence.md), sem enfraquecê-los.

| Situação | Ação do testador e do validador |
| --- | --- |
| Rota local sem feature | Verificação focada e parecer manual com critério, método, arquivos/versões, resultado e limitações no registro local; sem alegar gate automatizado |
| Rota local afetando feature | Atualizar artefatos e evidências afetados e preservar os gates da feature |
| Feature automatizada | Executar o checker SDD com `--require-approved --require-fresh` no conjunto real de features, com schema 2 e inputs atuais; avaliar também adequação dos oráculos |
| Verificação completa autorizada | Usar exatamente o ambiente Toolbox/Cargo e comando de AGENTS.md, examinar falhas/skips e resultados reais; exit zero não aceita o produto por si só |

Comandos reais de estrutura, executados da raiz (não são aceite):

```bash
PYTHONDONTWRITEBYTECODE=1 python3 sdd/tools/validate.py --root . --structure-only
PYTHONDONTWRITEBYTECODE=1 python3 tools/governance/scripts/check-ox.py
```

Confirme comandos e pré-requisitos no [README](../../README.md),
[projeto](../../sdd/project.md) e [scripts](../../scripts/README.md).
`--features` recebe um diretório de features; `--feature NAME` é repetível e
seleciona filhos diretos completos. O contrato de seleção e os checks compartilhados
estão em [evidence.md](../../sdd/evidence.md#select-whole-features). Para esta feature:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 sdd/tools/validate.py --root . --features sdd/features --feature configuration-cohesion --require-approved --require-fresh --check-convergence
```

Não aplique aprovação global a features intencionalmente não verificadas. Confira
`--help` e inputs reais; a seleção não dispensa critérios, bindings nem oráculos.
Não use `--structure-only` como aprovação nem combine-o com flags de aceite.

O Ox não usa a entrada `scripts/accept-task.sh` do Ec. A
[decisão de fechamento](../decisions/scripts-task-closure.md#preference-successor--2026-11-06)
não exige execução completa automática a cada tarefa. Estes agentes não alteram
essa decisão nem autorizam downloads/manutenção central. Para commits solicitados
explicitamente, consulte commit-governance antes de staging; configuração de
agentes não instala hooks nem concede permissão de commit/publicação.

## Uso e limites

Inicie uma nova sessão da raiz com `codex --strict-config` e confira carregamento
da configuração confiável. Opções explícitas da sessão e políticas administradas
podem prevalecer. Arquivos não reconfiguram retroativamente uma conversa. Clientes
sem descoberta por nome precisam receber modelo/esforço/instruções na criação,
com contexto próprio; sem essa capacidade, não afirmar aplicação do perfil.

Parsing/TOML, inspeção e cenários simulados verificam contratos diferentes de um
ensaio real de equipe. Distingua-os nas evidências. Não demonstram desempenho,
custo, latência ou obediência de modelos. A configuração não implementa scheduler
determinístico, não substitui permissões do host e não garante comportamento.
Avaliação dessas propriedades depende de tarefas reais e observação separada.

Fontes: [subagentes e arquivos TOML](https://learn.chatgpt.com/docs/agent-configuration/subagents#custom-agents)
e [referência de configuração](https://learn.chatgpt.com/docs/config-file/config-reference),
consultadas em 14/11/2026; CLI local observado: `codex-cli 0.169.0`.
