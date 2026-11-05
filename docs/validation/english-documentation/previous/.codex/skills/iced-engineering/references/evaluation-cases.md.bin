# Avaliações da skill

Contrato de casos; execução deve ser registrada separadamente. Não constituem testes realizados.

## Cenários técnicos preservados

- AC-01 → REQ-01: Operação lenta simulada não bloqueia navegação/interação; oráculo: teste de integração com heartbeat de UI.
- AC-02 → REQ-02: Painel expandido/recolhido preserva conteúdo e foco definidos; oráculo: teste funcional de estados.
- AC-03 → REQ-02: Redimensionamento extremo não perde ações essenciais; oráculo: revisão de layout em tamanhos documentados.
- AC-04 → REQ-03: Grafo oculto não agenda re-layout contínuo; oráculo: instrumentação sob workload controlado.

## Protocolo de avaliação

Forneça um pedido concreto e os inputs mínimos a um agente em diretório isolado autorizado. Na rodada de seleção, mostre somente catálogo/descriptions, sem a resposta esperada. Na rodada de comportamento, disponibilize a skill selecionada e os dados adversos. Preserve prompt, resposta bruta, identidade/configuração conhecida do agente, hashes dos inputs, revisão do resultado e limitações. Não execute serviços ou ferramentas com novas permissões.

Seleção positiva: pedir o entregável próprio descrito nesta entrada. Seleção negativa: usar a exclusão explícita; a resposta deve apontar competência mais adequada sem carregar esta skill. Falha: fornecer input que contraria o cenário técnico e exigir evidência antes de aprovação. Os prompts concretos do pacote consumidor devem incluir dados suficientes e um oráculo independente.

## Prompts concretos

### iced-engineering-positive

Adicionar componente Iced que permaneça interativo durante indexação e preserve foco ao recolher painéis.

### iced-engineering-negative

Avaliar hierarquia visual de uma jornada web sem código Iced.

### iced-engineering-failure

Uma UI Iced recebe resultado de busca antigo após troca de painel. Grafo oculto continua agendando layout. Não há lockfile fornecido. Proponha estado, efeitos, foco e ensaio, indicando APIs que precisam ser confirmadas.

Oráculo de revisão: positivo seleciona a competência própria; negativo encaminha para design-review (ou competência adjacente justificada). Na falha observar: version gap; generation guard; suspend work; measure UI not assert responsive. Este gabarito é revisado depois da resposta, não fornecido ao avaliador na seleção.
