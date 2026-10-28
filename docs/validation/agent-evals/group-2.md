# Ensaio interno de agente — grupo 2

Data: 2026-10-26. Executor: agente delegado `/root/evaluate_skills_2`.

Objetivo: responder seis casos de seleção e três de comportamento sem implementar produto. Este registro contém as respostas integrais do ensaio. Não é aprovação da skill, integração real, execução de UI, concorrência real no filesystem nem demonstração de eficácia comparativa. A avaliação independente das respostas cabe ao agente principal; não atribuo aprovação a mim mesmo.

Método: leitura do catálogo e prompts, decisão de seleção registrada antes de ler as skills, seguida de leitura das três entradas indicadas e referências técnicas delimitadas. A leitura inicial do JSON exibiu também os prompts de comportamento; não foram consultados gabaritos nem `evaluation-cases.md`. Para seleção, a evidência técnica usada foi somente nome/descrição do catálogo e enunciados `kind=selection`. Não usei rede, serviços externos nem outros agentes.

## Respostas de seleção

| ID | Primária | Motivo | Auxiliares |
|---|---|---|---|
| `workspace-integrity-engineering-positive` | `workspace-integrity-engineering` | A pergunta central é preservar arquivos sob escritores concorrentes, snapshots, eventos incompletos e recuperação. | Nenhuma; o enunciado não delimita pergunta adicional. |
| `workspace-integrity-engineering-negative` | `database-engineering` | A migração de coluna e a recuperação após crash dizem respeito a esquema e consistência da persistência SQLite. Não há concorrência externa de arquivos a resolver. | Nenhuma. |
| `iced-engineering-positive` | `iced-engineering` | A interação durante indexação e a preservação de foco dependem do estado, efeitos e contratos de widgets Iced. | Nenhuma. |
| `iced-engineering-negative` | `design-review` | A tarefa pede avaliar hierarquia de uma jornada web; seu entregável é crítica de experiência, sem implementação Iced. | Nenhuma. |
| `code-context-engineering-positive` | `code-context-engineering` | A pergunta é sobre identidade, posições, invalidação e proveniência de um índice incremental de código, incluindo degradação sem LSP. | Nenhuma. |
| `code-context-engineering-negative` | `ai-engineering` | A pergunta é avaliar ganho da recuperação por embeddings frente à busca textual, sem alterar o mecanismo de indexação. | Nenhuma; estratégia de avaliação integra a pergunta principal. |

## `workspace-integrity-engineering-failure`

**Dados:** A e B leram H0; A publicou H1; B pretende publicar H2; há destino que escapa por symlink; crash entre staging e rename; watcher perdeu eventos.

**Resposta operacional:**

1. A pré-condição de B é H0, mas o destino contém H1. A gravação direta H2 deve ser recusada como conflito. Preservar H0 recuperável, H1 efetivo e a proposta H2 com autoria/identidade. B pode produzir diff ou proposta de merge a partir desses conteúdos; qualquer publicação do merge deve ter H1 como base observada, revisão da combinação e nova verificação imediatamente no compromisso. Uma nova alteração posterior volta a causar conflito. Não se autoriza restaurar H0 sobre H1.
2. Vincular intenção a raiz autorizada, caminho relativo, identidade do objeto, hash base e hash proposto. Rejeitar o destino que resolve fora da raiz por symlink antes de staging/publicação; nem leitura de conteúdo externo é necessária para validar a rejeição. Comparar strings de prefixo ou canonicalizar uma única vez não protege contra troca de symlink entre checagem e uso. A implementação futura deve escolher primitivas relativas a diretórios/handles que mantenham a operação confinada e testar sua garantia no SO alvo. Se o ambiente não permite garantir a fronteira sob esse modelo de ameaça, suspender a publicação dependente; não prometer portabilidade ou atomicidade que não foi estabelecida.
3. Comparar antes de rename, sozinho, ainda deixa uma janela entre comparação e substituição quando escritores externos não cooperam. A política de concorrência precisa de um ponto de compromisso protegido e mecanismo que de fato cubra os escritores relevantes. Lock cooperativo só cobre participantes cooperantes. Se isso não estiver disponível, manter proposta/conflito sem alegar compare-and-swap do filesystem. A rechecagem de conteúdo é necessária, mas não prova exclusão mútua.
4. O journal deve conter identificação da operação, raiz/caminho, base, novo hash, staging e progresso persistido. No reinício, inspecionar journal e conteúdo real sob fronteiras válidas, sem assumir que o estágio registrado corresponde ao último efeito durável. Se o destino ainda é a base e o staging íntegro corresponde à proposta, a escrita não está confirmada: conservar o staging e só retomar após revalidar conteúdo, destino e autorização. Se o destino já contém os novos bytes, reconciliar como publicação observada sem registro final, conforme a política de durabilidade. Se contém bytes inesperados, como H1 quando a intenção de B ainda parte de H0, preservar candidatos e registrar conflito. Staging ausente não comprova sucesso. Mount inacessível é indisponibilidade; adiar, sem tombstone de exclusão.
5. Staging deve usar filesystem compatível com a substituição planejada. Rename de um caminho não estabelece transação de vários arquivos nem durabilidade após falha de energia. Flush de arquivo/diretório e semântica de substituição são decisões dependentes de plataforma a verificar, inclusive falhas antes/depois de cada ponto.
6. Tratar o watcher como aviso incompleto. Marcar o escopo afetado como incerto e reconciliar conteúdo/identidades por varredura delimitada; construir novo snapshot coerente e invalidar índices dependentes. Representar exclusões confirmadas por tombstones. Para rename não demonstrado, usar remoção/criação, sem inventar identidade pela semelhança do nome. Reconciliar também mudanças não notificadas.

**Operações neste ensaio:** somente ler documentação autorizada e registrar esta resposta dentro de `docs/validation/agent-evals/`. Nenhuma gravação real de H0/H1/H2, simulação de crash ou teste de symlink foi executada.

**Ensaio futuro proposto:** dois escritores sobre a mesma base, troca de symlink durante commit, falha antes/depois de flush/rename/registro final e edição com evento suprimido. Oráculos: H1 preservado diante da proposta obsoleta de B; nenhum acesso externo; candidatos recuperáveis; snapshot reconciliado sem referências atuais a bytes antigos. SO, filesystem, protocolo de escritores e journal real não foram fornecidos; garantias de integração permanecem não verificadas.

## `iced-engineering-failure`

**Dados:** resultado antigo de busca após troca de painel; grafo oculto ainda agenda layout; não há lockfile.

**Resposta operacional:**

Modelar cada painel por identidade estável e por uma época de ativação distinta de sua posição visual. O estado mantém painel ativo/visível, geração de busca, texto da consulta, estados `idle/loading/ready/error`, alvo de foco e geração do grafo. Um resultado carrega painel, época, geração da consulta e identidade da requisição. `SearchFinished` só altera estado se todas as identidades coincidirem com a requisição ainda válida; resultado atrasado da navegação anterior é descartado mesmo se o usuário reabrir o mesmo painel. Trocar consulta, cancelar ou mudar o escopo do painel invalida a geração. Não reutilizar um resultado antigo só porque o texto da consulta coincide.

`update` determina transições e efeitos; `view` projeta estado sem IO bloqueante, busca ou cálculo pesado. Busca e layout usam trabalhadores apropriados ao executor efetivamente adotado, filas limitadas e resultado como mensagem. Uma tarefa assíncrona com cálculo síncrono longo ainda pode bloquear o executor; escolher deslocamento de CPU com evidência do runtime. Cancelar trabalho obsoleto quando possível e manter a checagem de geração, pois cancelamento pode chegar tarde.

Ao ocultar o grafo, a transição suspende produtores/subscriptions relevantes, cancela trabalho de layout de propriedade independente e impede novo agendamento. Resultados tardios não restauram o loop nem alteram outro painel. Conservar o último cache é permitido, mas não conservar um produtor ativo só para mantê-lo. Ao reabrir, reaproveitar cache apenas se a geração dos dados e parâmetros de layout ainda forem válidos; caso contrário, emitir uma única nova geração de trabalho. Atualizações puramente visuais podem ser coalescidas; eventos necessários à evidência de execução não devem ser perdidos.

Ao recolher um painel cujo controle tem foco, mover o foco para o acionador visível de expansão ou outro controle definido pelo fluxo. Preservar identidade lógica do alvo anterior e conteúdo do painel. Ao reabrir, restaurar foco somente se o alvo existir, estiver visível e habilitado; caso contrário usar fallback visível. Validação da geometria salva deve considerar janela menor e escala de texto. O foco não pode permanecer num nó invisível.

O ensaio proposto separa transições puras de integração: entregar resultados fora de ordem, navegar e reabrir antes do resultado, cancelar já em conclusão e verificar que só a geração ativa altera conteúdo; medir contador de novos layouts com grafo oculto, que deve permanecer sem incrementos após a suspensão, e verificar que conclusão em voo não reagenda; sob indexação lenta e rajadas, medir heartbeat de UI, latência de entrada/quadro e comprimento de fila no hardware escolhido; executar navegação por teclado, recolhimento/expansão, janelas extremas e estados vazio/erro/carregando. Limiares dependem de um orçamento ainda não fornecido; não inventar percentis ou conformidade de acessibilidade.

As referências consultadas descrevem Iced 0.14.0; isso não demonstra versão instalada. Antes de código, obter manifest/lockfile/features/executor do consumidor e confirmar assinaturas de `Task`, cancelamento, identidade/lifetime de `Subscription`, foco e operações de widget, callbacks de pane-grid e, se houver widget customizado, contratos de layout, eventos, desenho e acessibilidade. Não proponho assinaturas como se estivessem compiladas. Não há UI executada, teste de scheduling, medição ou teste com tecnologia assistiva neste ensaio; compilação e integração permanecem não verificadas.

## `code-context-engineering-failure`

**Dados:** dois módulos definem `run`; AST encontra chamada sem resolução; rename e caractere multibyte antes do símbolo; LSP indisponível.

**Resposta operacional:**

A consulta retorna a ocorrência sintática da chamada e as duas definições como candidatos distintos, cada uma com identidade de documento/módulo, nome qualificado quando disponível e identidade de símbolo. A chamada deve registrar `resolution=unresolved`, método de extração AST e motivo `semantic_provider_unavailable` ou equivalente. A lista é de candidatos encontrados, sem promessa de exaustividade. Não produzir aresta factual de chamada para nenhum dos dois `run`; igualdade do nome não decide imports, escopo, sobrecarga ou despacho. Busca textual/caminhos continua disponível, explicitamente com garantias reduzidas.

Cada resultado deve conter workspace, snapshot/geração, caminho relativo atual, hash do conteúdo, método e versão/configuração do parser, range com unidade declarada e estado de freshness. Se o snapshot também inclui conteúdo não salvo, esse conteúdo deve ter identidade própria verificável. Separar identidade de documento, identidade do símbolo e hash; mesmo conteúdo em outro caminho não prova identidade contínua. Incluir truncamento/indisponibilidade quando ocorrerem. Campos desconhecidos ficam desconhecidos, não preenchidos por suposição.

O rename e a edição invalidam as posições antigas e os registros derivados do documento, incluindo definições, ocorrências e referências cujo contexto depende dele. Só preservar identidade conceitual por rename se houver evidência do vínculo; sem isso, tombstone para o caminho antigo e adição do novo. Não reciclar offsets antigos no novo caminho. Preparar a nova geração com conteúdo atual, extração refeita ou atualização incremental conforme contrato do parser, remoções e dependências invalidadas; publicá-la coerentemente, sem misturar definições novas com referências antigas apresentadas como atuais.

O caractere multibyte exige recalcular posições a partir dos bytes efetivos. Não somar um em offsets de bytes supondo que um caractere vale um byte; tampouco equiparar offsets UTF-8, caracteres e posições UTF-16. Declarar a codificação de ranges do índice e converter por mapa de linhas/unidades conferido contra o conteúdo. Se LSP voltar, negociar capabilities/position encoding e vincular resultados à versão do documento e servidor; não presumir a unidade do protocolo.

Antes de extrair ou apresentar trecho clicável, comparar o hash esperado com os bytes lidos. Em divergência, atualizar/reconsultar ou retornar `stale`/indisponível sem apresentar o range antigo como válido. Enquanto a nova geração não está pronta, é possível consultar explicitamente o snapshot anterior preservado, claramente marcado como antigo, ou responder que o índice atual está pendente. Falha de parsing não promove automaticamente a geração anterior a atual. Com watcher incerto, reconciliar o escopo por conteúdo antes de afirmar freshness.

Ensaio futuro: corpus versionado com dois homônimos e posições conhecidas, rename mais inserção não ASCII, consulta com/sem LSP, parser falhando e watcher omitido. Oráculos independentes devem comparar identidade e texto exato do intervalo, ausência do caminho removido na geração atual, ambiguidade preservada e fallback rotulado. Neste ensaio, não houve execução de parser/LSP/índice nem medição de precisão ou ganho de recuperação; não há offsets numéricos calculáveis sem os bytes reais.

## Arquivos consultados e limites

Todos os caminhos abaixo são relativos à raiz `ox/`, salvo a instrução da raiz fornecida na conversa.

- Instruções da raiz `AGENTS.md` fornecidas na conversa; `AGENTS.md` de Ox.
- `sdd/project.md`, `docs/constitution.md`, `docs/architecture/context.md`, `docs/decisions/adoption.md`, `sdd/workflow.md`, `sdd/evidence.md` (saída conjunta parcialmente truncada; usados os trechos de estados/evidência disponíveis, sem reivindicar leitura integral do trecho truncado).
- `src/fixtures/selection-catalog.json` e `src/fixtures/agent-prompts-2.json`.
- `skills/workspace-integrity-engineering/SKILL.md`, `skills/workspace-integrity-engineering/references/file-operations.md`, `skills/workspace-integrity-engineering/references/watcher-and-recovery.md`.
- `skills/iced-engineering/SKILL.md`, `skills/iced-engineering/references/message-update-state.md`, `skills/iced-engineering/references/layout-and-custom-widgets.md`, `skills/iced-engineering/references/desktop-performance-and-accessibility.md`.
- `skills/code-context-engineering/SKILL.md`, `skills/code-context-engineering/references/incremental-indexing.md`, `skills/code-context-engineering/references/symbols-and-resolution.md`.

Inspeção anterior à gravação confirmou que o diretório de avaliação existia e `group-2.md` ainda não existia; não foi sobrescrito artefato anterior. A única escrita deste agente é este arquivo. Não consultei arquivos de gabarito, não executei comandos de aplicação e não alterei critérios ou resultados de aceitação. As respostas são observações de comportamento textual do agente com base nos inputs citados; a avaliação de adequação e os gates existentes ficam a cargo da etapa externa a este ensaio.
