# Ensaio interno de respostas — grupo 1

Data: 2026-10-26. Este é um ensaio de resposta de agente interno, sem integração real, execução de processos do produto, rede ou serviços externos. Não constitui autoaprovação, evidência de sandbox real, execução dos testes propostos ou comparação de eficácia. O agente não consultou gabaritos nem `evaluation-cases.md` e não delegou trabalho. Os únicos arquivos escritos pertencem a `docs/validation/agent-evals/`.

## Método e arquivos consultados

Os pedidos foram lidos em `src/fixtures/agent-prompts-1.json`. A seleção usa exclusivamente as descrições de `src/fixtures/selection-catalog.json` e os pedidos `kind=selection`; as skills e referências abaixo são utilizadas para as respostas `kind=behavior`. Os caminhos neste registro são relativos a `ox/`.

Autoridades consultadas para o escopo do registro: `AGENTS.md`, `sdd/project.md`, `docs/constitution.md`, `docs/architecture/context.md`, `docs/decisions/adoption.md`, `sdd/workflow.md` e `sdd/evidence.md`, além das instruções da raiz fornecidas no pedido. A rota do registro é local: criação de uma observação documental, sem mudança de contratos ou implementação.

Entradas e referências técnicas consultadas para comportamento:

- `skills/plugin-protocol-engineering/SKILL.md` (1.0.0).
- `skills/plugin-protocol-engineering/references/protocol-negotiation.md`.
- `skills/plugin-protocol-engineering/references/permissions-and-isolation.md`.
- `skills/plugin-protocol-engineering/references/versioning-and-faults.md`.
- `skills/agent-runtime-engineering/SKILL.md` (1.0.0).
- `skills/agent-runtime-engineering/references/session-state-machine.md`.
- `skills/agent-runtime-engineering/references/process-supervision.md`.
- `skills/autonomous-verification-engineering/SKILL.md` (1.0.0).
- `skills/autonomous-verification-engineering/references/acceptance-verdicts.md`.
- `skills/autonomous-verification-engineering/references/evidence-provenance.md`.
- `skills/autonomous-verification-engineering/references/independent-oracles.md`.

## Respostas integrais — seleção

### plugin-protocol-engineering-positive

Pedido: “Criar um protocolo host/plugin para um provedor LSP com negociação de versão e permissões.”

Competência primária: `plugin-protocol-engineering`. O trabalho define contrato entre host e plugin, negociação de versões, capacidades e fronteiras de falha. LSP é o serviço fornecido, mas a decisão principal é o protocolo da extensão. Auxiliares: nenhuma indispensável para a seleção solicitada; uma revisão especializada de isolamento só seria necessária se restasse uma pergunta concreta sobre mecanismos de segurança.

### plugin-protocol-engineering-negative

Pedido: “Adicionar uma regra de lint usando um SDK de plugins já estável, sem alterar protocolo ou permissões.”

Competência primária: `software-design`. O pedido é implementar comportamento local usando um contrato existente; exige delimitar a responsabilidade da regra e sua integração ao SDK. Não existe decisão de protocolo que justifique `plugin-protocol-engineering`. A linguagem não foi informada, portanto não presumiria Rust. Auxiliares: nenhuma indispensável; exemplos válidos, inválidos e ausência de falsos positivos podem ser verificados proporcionalmente sem ativar uma especialidade adicional por padrão.

### agent-runtime-engineering-positive

Pedido: “Projetar adaptador CLI com streaming, cancelamento, reconexão e supervisão de processos.”

Competência primária: `agent-runtime-engineering`. Streaming, identidade de execução, supervisão, cancelamento e retomada formam o ciclo de vida de execução que a competência cobre. Auxiliares: nenhuma indispensável no enunciado.

### agent-runtime-engineering-negative

Pedido: “Comparar qualidade de respostas de dois modelos sem ferramentas nem processos.”

Competência primária: `ai-engineering`. A comparação precisa de critérios de qualidade, exemplos representativos e um método de avaliação de resultados dos modelos. Não envolve supervisão ou efeitos de processos, portanto `agent-runtime-engineering` não se aplica. Auxiliares: nenhuma indispensável; `prompt` só se tornaria necessária se o entregável passasse a incluir redação ou revisão dos prompts.

### autonomous-verification-engineering-positive

Pedido: “Projetar motor que atribui veredictos por critério a entregas de agentes, vinculando evidências ao snapshot.”

Competência primária: `autonomous-verification-engineering`. O objeto é a orquestração de aceitação por critério, com proveniência e validade de evidências, além da simples escrita de testes. Auxiliares: nenhuma indispensável no enunciado.

### autonomous-verification-engineering-negative

Pedido: “Criar testes unitários de uma função de soma e diagnosticar um teste flaky, sem motor de aceitação.”

Competência primária: `software-testing`. O pedido trata de casos, oráculos e diagnóstico de instabilidade da suíte. Não exige motor de aceitação de entregas autônomas. Auxiliares: nenhuma indispensável.

## Respostas integrais — comportamento

### plugin-protocol-engineering-failure

Pedido: “Host oferece read/search; plugin pede read/write; grant é read na raiz A. O plugin em processo separado diz que pode ler a raiz B diretamente e cai após gravar mas antes de responder. Proponha contrato e verificações; não execute processos.”

A capacidade efetiva mediada é somente `read` em A: interseção entre capacidades oferecidas, pedidas e concedidas, preservando o escopo do grant. `search` não foi pedido; `write` não é oferecido nem concedido. Se `write` for obrigatório para o plugin, rejeitar a ativação com motivo explícito; se opcional, negociar apenas leitura. Uma mensagem válida não concede uma operação.

O contrato deve vincular cada grant a identidade do plugin, geração da instância, operação, recurso, validade e revogação. Cada requisição inclui versão negociada, geração, ID único de correlação, operação, recurso e prazo. A fronteira de efeito revalida a autorização, incluindo revogação; caminhos precisam ser resolvidos por mecanismos da plataforma que impeçam escape por `..`, links e troca concorrente de alvos, sem confiar em prefixos de strings. Definir enquadramento do transporte, limite de tamanho e quantidade de mensagens, campos obrigatórios/opcionais, tratamento de versão incompatível e IDs repetidos. Não admitir efeitos antes de completar a negociação.

A declaração de que o processo pode ler B expõe uma fronteira distinta: grants do IPC não restringem acesso direto com credenciais do SO. Não executar esse plugin com expectativa de isolamento até existir mecanismo de contenção validado para a plataforma, como conta ou sandbox com acesso mínimo e recursos explicitamente fornecidos. A escolha depende do SO e do modelo de confiança ainda não informados. Assinatura, manifesto e processo separado não demonstram confinamento. A leitura direta de B permanece não verificada neste ensaio; a declaração do plugin é uma alegação, não uma prova de acesso.

O fato fornecido de uma gravação concluída contradiz a política somente leitura. Se passou pelo host, houve falha no controle mediado; se foi direta, o controle do processo foi insuficiente. Registrar separadamente violação de permissão, local/escopo afetado e desfecho da resposta. A queda depois do efeito e antes da resposta produz resultado incerto para o solicitante que só conhece o IPC: ausência de resposta não significa ausência de gravação. Não repetir a operação automaticamente. Interromper admissão, preservar estado e registros, reconciliar arquivos e eventual diário de operações. Não sobrescrever alterações concorrentes com rollback cego.

Uma operação mutante futura autorizada precisaria de chave de idempotência com semântica persistente, consulta de resultado e proteção contra reutilização da chave com payload diferente; um ID de mensagem sozinho não garante execução única. Isso não autoriza a gravação deste caso.

Estados propostos: descoberto → negociando → pronto → drenando → parado, com falha possível em cada fase. Ao falhar, fechar admissão, concluir ou expirar pendências de forma explícita e registrar efeitos incertos e recursos remanescentes. Reinício cria nova geração e negocia novos grants; respostas antigas ficam registradas como obsoletas e não satisfazem novos pedidos.

Verificações propostas, sem execução: leitura autorizada em A; escrita mediada negada sem alteração do arquivo; leitura mediada de B negada; acesso direto a B negado pelo controle real da plataforma; escapes por links e caminhos rejeitados; revogação aplicada antes do efeito; quadros malformados ou grandes rejeitados; versões compatíveis aceitas e incompatíveis rejeitadas; respostas antigas isoladas; falha antes, durante e depois de um efeito controlado reconciliada sem repetição indevida. Usar recursos descartáveis e observar conteúdo antes/depois para escrita e o resultado real da tentativa de acesso para leitura — conteúdo inalterado não prova que ninguém leu. Registrar método, versão, grants, estado persistente, motivo de saída e limpeza. Mocks sustentam somente a lógica do protocolo; contenção real e recuperação precisam de integração autorizada posterior.

### agent-runtime-engineering-failure

Pedido: “Execução A declarou concluído, encerrou sem testes, e seu evento atrasado chegou depois do início de B. B produz stdout/stderr intensamente e ignora cancelamento cooperativo. Descreva transições, controle e evidência; não execute processos.”

Separar sessão, tarefa, tentativa, identidade do processo e sequência dos eventos. `done` de A é uma declaração do agente. O encerramento é observação do supervisor, registrada com exit code ou sinal quando disponível. Nenhum deles demonstra aceitação funcional; critérios que dependem dos testes ausentes ficam `NÃO VERIFICADO`, sem inventar falha funcional ou sucesso.

Uma tentativa percorre iniciando → executando → encerrada/falhou; cancelamento acrescenta executando → cancelamento solicitado → encerrada/falhou. A tarefa conserva um estado independente de verificação. O evento atrasado contém geração/tentativa A e deve ser anexado ao histórico de A, mesmo recebido durante B, sem reabrir A nem alterar B. Se não houver identidade suficiente, isolar como evento não atribuível e reconciliar; nunca atribuir pela tentativa atualmente visível. Deduplicar por origem/geração/sequência, conservar lacunas e registrar tempos de emissão e recebimento quando disponíveis.

Para B, manter consumidores concorrentes de stdout e stderr, com filas e memória limitadas, retenção de bytes brutos e política de escoamento para armazenamento com quota. Separar a entrega de eventos críticos e comandos de controle da renderização da saída, para que saturação não impeça cancelamento. Erro de armazenamento ou quota esgotada deve aparecer como captura incompleta e provocar a ação definida pela política, inclusive parada controlada quando necessária; não perder evidência silenciosamente. Stderr humano não fornece permissão autoritativa.

Ao cancelar B: fechar admissão de novo trabalho, registrar o pedido e seu prazo, enviar cancelamento somente pela operação realmente suportada e continuar drenando os dois streams. Pedido enviado não significa cancelamento concluído. Como o caso informa que B ignora cooperação, ao expirar o prazo escalar a término da árvore de processos de propriedade do supervisor usando mecanismo adequado ao SO; confirmar saída, recolher o processo e terminar a drenagem. Não matar processos apenas por nome. Se descendentes escaparem da contenção ou não puderem ser inspecionados, registrar limpeza incompleta e manter a lacuna operacional visível. Não supor que terminar o pai encerra todos os descendentes.

Antes de retry, preservar e reconciliar os efeitos parciais de B no workspace e qualquer operação externa conhecida. Nova tentativa recebe geração própria e grants revalidados, sem herança implícita de permissões. Reconexão informa último evento confirmado e lacunas; replay de mensagens não repete efeitos por padrão. Só anunciar retomada se o adaptador a suportar de fato.

Evidência prevista: trilha por tentativa com IDs, sequência, origem, localização e integridade dos bytes brutos; declaração `done` de A; motivo de saída de A; ausência de execução dos testes; recebimento tardio vinculado a A; cancelamento de B, prazos e escalonamento; volume/limite das filas; eventual perda de captura; saída, drenagem e recursos ainda vivos; diferenças do workspace e resultado da reconciliação. Testes futuros controlados devem cobrir saída intensa nos dois pipes, evento atrasado, lacunas, morte antes de drenar, disco cheio e descendentes resistentes. Sem SO, executável e versão do adaptador não há comando concreto seguro nem garantia observada de limpeza. Este texto descreve transições e verificações propostas; nenhum processo foi iniciado ou terminado.

### autonomous-verification-engineering-failure

Pedido: “Critério A tinha teste passando sobre arquivo X; X mudou. Critério B testa arquivo Y inalterado. O teste de C está ausente. Há uma verificação de build aprovada, mas nenhum grant de publicação. Classifique e proponha retomada; não publique.”

| Objeto | Classificação atual | Justificativa e próximo passo |
| --- | --- | --- |
| Critério A | NÃO VERIFICADO para o conteúdo atual | Preservar a observação anterior como histórica e obsoleta. A mudança de X invalida sua utilização para aceitação atual; executar novamente o método pertinente sobre os novos inputs. Não concluir REPROVADO sem observação de violação. |
| Critério B | Manter APROVADO somente se a evidência anterior sustentava B e todos os seus inputs relevantes permanecem iguais | Y inalterado sozinho não prova freshness do oráculo, configuração ou contrato. Conferir o conjunto de dependências; a mudança exclusiva de X não invalida B se B não depender de X. Se não houver evidência anterior ou vínculo suficiente, B fica NÃO VERIFICADO até essa lacuna ser resolvida. |
| Critério C | NÃO VERIFICADO | Teste ausente não significa aprovação nem NÃO APLICÁVEL. Restaurar ou construir oráculo independente adequado ao critério e executar no ambiente autorizado. |
| Verificação de build | APROVADO no snapshot observado; aceitação atual depende de freshness | Conservar a observação e verificar seus inputs. Se o build inclui X alterado, a observação anterior não sustenta o build atual e a verificação deve ser refeita. Seu sucesso não decide A, B ou C automaticamente. |
| Publicação | Não autorizada; não executar | Grant é controle separado de veredicto. Build aprovado não fornece permissão de publicação. |

A retomada começa pelos critérios normativos e mapa de dependências das evidências: implementação, oráculo, configuração, fixtures, contrato e ambiente identificável. Comparar bytes/hashes reais com os registrados, incluindo arquivos não commitados pertinentes. Preservar logs e hashes antigos; não atualizar hashes ao redor de um resultado passado para fazê-lo parecer atual.

Executar somente as verificações afetadas: A, C após disponibilizar seu teste, e build se seus inputs mudaram. B não precisa ser repetido quando sua validade completa for confirmada. Como os comandos e artefatos concretos dos testes não estão no input, a instrução exata de replay depende de localizar o comando autorizado e o ambiente registrados; não inventaria um comando nem declararia execução. Para cada nova observação registrar critério, método/comando exato, tempo, ambiente, resultado/exit code, artefato e hashes da implementação, oráculo e demais inputs.

Desafiar o mecanismo em fixtures descartáveis: alterar X depois de um resultado positivo e verificar a invalidação somente das dependências; simular teste ausente ou wrapper que retorna zero sem executar testes e verificar que não promove C; dar um build aceito a uma simulação de publicação sem grant e verificar a recusa. O oráculo deve derivar dos critérios, sem copiar a resposta do candidato como resultado esperado. Essas são verificações propostas e ainda não executadas. Mocks não demonstram controle do destino real de publicação.

Nenhum agregado de aceitação integral está sustentado enquanto critérios obrigatórios permanecerem sem evidência atual. Se observações forem conflitantes ou não permitirem decidir o comportamento, usar INCONCLUSIVO e investigar; REPROVADO requer evidência de contradição, e NÃO APLICÁVEL requer exclusão justificada pelo escopo. A publicação permanece parada por falta de autoridade mesmo depois de todos os critérios técnicos eventualmente serem atendidos.

## Limitações e lacunas observadas

- A leitura de `README.md`, referenciado por `AGENTS.md`, falhou porque o arquivo não existia no momento da consulta. Não se executaram runners do projeto.
- A inspeção com `git status` confirmou que o diretório não é um repositório Git disponível; nenhum baseline Git foi presumido. O destino do registro não existia antes da escrita, portanto não houve substituição de conteúdo anterior.
- As referências técnicas incluem exemplos próximos aos inputs comportamentais. As respostas mostram aplicação das instruções consultadas; não são uma avaliação cega ou medida de generalização para casos inéditos.
- Não foram consultadas as páginas externas citadas pelas referências locais. Nenhuma alegação depende de conferir versões externas atuais.
- O único resultado observado é a resposta documental do agente. Verificações, testes, isolamento, controle de processos e autorização de publicação descritos nos casos permanecem propostas sem integração real.
- Não há classificação de aprovação deste agente ou das skills neste registro; qualquer julgamento posterior exige critérios e revisão separados.
