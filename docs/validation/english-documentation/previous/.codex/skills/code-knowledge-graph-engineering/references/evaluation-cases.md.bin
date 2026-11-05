# Avaliações da skill

Contrato de casos; execução deve ser registrada separadamente. Não constituem testes realizados.

## Cenários técnicos preservados

- AC-01 → REQ-01: Aresta de chamada válida pode ser rastreada a localização e método; oráculo: corpus sintético conhecido.
- AC-02 → REQ-02: Relação inferida marcada incorretamente como verificada é rejeitada; oráculo: schema/assert de proveniência.
- AC-03 → REQ-03: Alteração remove aresta obsoleta no snapshot novo; oráculo: fixture antes/depois.
- AC-04 → REQ-03: Consulta por subgrafo aplica limite e relatórios de truncamento; oráculo: grafo grande gerado determinísticamente.

## Protocolo de avaliação

Forneça um pedido concreto e os inputs mínimos a um agente em diretório isolado autorizado. Na rodada de seleção, mostre somente catálogo/descriptions, sem a resposta esperada. Na rodada de comportamento, disponibilize a skill selecionada e os dados adversos. Preserve prompt, resposta bruta, identidade/configuração conhecida do agente, hashes dos inputs, revisão do resultado e limitações. Não execute serviços ou ferramentas com novas permissões.

Seleção positiva: pedir o entregável próprio descrito nesta entrada. Seleção negativa: usar a exclusão explícita; a resposta deve apontar competência mais adequada sem carregar esta skill. Falha: fornecer input que contraria o cenário técnico e exigir evidência antes de aprovação. Os prompts concretos do pacote consumidor devem incluir dados suficientes e um oráculo independente.

## Prompts concretos

### code-knowledge-graph-engineering-positive

Definir schema de arestas de código e consultas de impacto com limites e duas projeções do mesmo grafo.

### code-knowledge-graph-engineering-negative

Criar um diagrama estático de marketing sem relações extraídas de código.

### code-knowledge-graph-engineering-failure

Aresta inferida com similaridade 0.98 veio marcada verified=true; seu arquivo mudou. Consulta passa por ciclo e um hub com dez mil arestas. Especifique validações, invalidação e limites sem presumir desempenho.

Oráculo de revisão: positivo seleciona a competência própria; negativo encaminha para design-system (ou competência adjacente justificada). Na falha observar: reject false verified; snapshot invalidation; visited plus limits and truncation. Este gabarito é revisado depois da resposta, não fornecido ao avaliador na seleção.
