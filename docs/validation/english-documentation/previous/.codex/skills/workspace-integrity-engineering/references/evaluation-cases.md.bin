# Avaliações da skill

Contrato de casos; execução deve ser registrada separadamente. Não constituem testes realizados.

## Cenários técnicos preservados

- AC-01 → REQ-01: Tentativa de escrita fora da raiz via .. ou symlink é rejeitada; oráculo: fixture com caminhos adversos.
- AC-02 → REQ-02: Dois agentes editam mesma versão: segunda gravação conflita ou aplica merge verificado; oráculo: teste concorrente.
- AC-03 → REQ-03: Falha injetada entre arquivo temporário e rename não deixa registro “concluído” incorreto; oráculo: teste de crash.
- AC-04 → REQ-03: Arquivo externo alterado invalida hash/snapshot; oráculo: watcher + verificação por leitura real.

## Protocolo de avaliação

Forneça um pedido concreto e os inputs mínimos a um agente em diretório isolado autorizado. Na rodada de seleção, mostre somente catálogo/descriptions, sem a resposta esperada. Na rodada de comportamento, disponibilize a skill selecionada e os dados adversos. Preserve prompt, resposta bruta, identidade/configuração conhecida do agente, hashes dos inputs, revisão do resultado e limitações. Não execute serviços ou ferramentas com novas permissões.

Seleção positiva: pedir o entregável próprio descrito nesta entrada. Seleção negativa: usar a exclusão explícita; a resposta deve apontar competência mais adequada sem carregar esta skill. Falha: fornecer input que contraria o cenário técnico e exigir evidência antes de aprovação. Os prompts concretos do pacote consumidor devem incluir dados suficientes e um oráculo independente.

## Prompts concretos

### workspace-integrity-engineering-positive

Projetar gravação concorrente entre editor e agentes, com snapshots, watcher e recuperação de arquivos.

### workspace-integrity-engineering-negative

Planejar migração de uma coluna SQLite local após crash, sem escritores externos no filesystem.

### workspace-integrity-engineering-failure

Dois escritores leram H0; A publicou H1; B tenta gravar H2. Um destino usa symlink para fora da raiz, e houve crash entre staging e rename com watcher perdido. Explique operações permitidas e recuperação; não escreva fora do diretório de avaliação.

Oráculo de revisão: positivo seleciona a competência própria; negativo encaminha para database-engineering (ou competência adjacente justificada). Na falha observar: conflict; reject escape; read actual contents; no blind rollback or TOCTOU claim. Este gabarito é revisado depois da resposta, não fornecido ao avaliador na seleção.
