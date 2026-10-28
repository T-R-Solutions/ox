# Avaliações da skill

Contrato de casos; execução deve ser registrada separadamente. Não constituem testes realizados.

## Cenários técnicos preservados

- AC-01 → REQ-01: Consulta de símbolo relata arquivo, intervalo, snapshot e método; oráculo: fixtures com posições verificadas.
- AC-02 → REQ-02: Renomeação/edição invalida entradas antigas e atualiza as afetadas; oráculo: mutações controladas de repositório.
- AC-03 → REQ-03: Chamada ambígua sem semântica não é rotulada como referência verificada; oráculo: código homônimo e imports.
- AC-04 → REQ-03: LSP ausente resulta em degradação explícita, sem resultado inventado; oráculo: servidor deliberadamente indisponível.

## Protocolo de avaliação

Forneça um pedido concreto e os inputs mínimos a um agente em diretório isolado autorizado. Na rodada de seleção, mostre somente catálogo/descriptions, sem a resposta esperada. Na rodada de comportamento, disponibilize a skill selecionada e os dados adversos. Preserve prompt, resposta bruta, identidade/configuração conhecida do agente, hashes dos inputs, revisão do resultado e limitações. Não execute serviços ou ferramentas com novas permissões.

Seleção positiva: pedir o entregável próprio descrito nesta entrada. Seleção negativa: usar a exclusão explícita; a resposta deve apontar competência mais adequada sem carregar esta skill. Falha: fornecer input que contraria o cenário técnico e exigir evidência antes de aprovação. Os prompts concretos do pacote consumidor devem incluir dados suficientes e um oráculo independente.

## Prompts concretos

### code-context-engineering-positive

Projetar índice incremental de símbolos com offsets e proveniência por snapshot e fallback sem LSP.

### code-context-engineering-negative

Testar se embeddings melhoram localização de código comparados a busca textual, sem mudar mecanismo de indexação.

### code-context-engineering-failure

Dois módulos definem run; AST achou chamada run sem resolução. Arquivo foi renomeado e ganhou um caractere multibyte antes do símbolo; LSP está indisponível. Defina retorno de consulta e invalidação.

Oráculo de revisão: positivo seleciona a competência própria; negativo encaminha para ai-engineering (ou competência adjacente justificada). Na falha observar: syntax not resolved; byte/encoding bounds; rename invalidation; explicit fallback. Este gabarito é revisado depois da resposta, não fornecido ao avaliador na seleção.
