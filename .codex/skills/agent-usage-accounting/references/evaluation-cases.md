# Avaliações da skill

Contrato de casos; execução deve ser registrada separadamente. Não constituem testes realizados.

## Cenários técnicos preservados

- AC-01 → REQ-01: Uso sem preço disponível retorna custo desconhecido, não zero; oráculo: fixture de modelo sem tarifa.
- AC-02 → REQ-02: Reenvio duplicado de evento com mesmo ID não duplica soma; oráculo: teste de replay.
- AC-03 → REQ-03: Tokens em cache, entrada e saída são agregados conforme contrato observado; oráculo: fixture de provedor.
- AC-04 → REQ-03: Intervalo diário usa timezone explicitado e não altera valor de contexto atual; oráculo: fronteira de dia/hora.

## Protocolo de avaliação

Forneça um pedido concreto e os inputs mínimos a um agente em diretório isolado autorizado. Na rodada de seleção, mostre somente catálogo/descriptions, sem a resposta esperada. Na rodada de comportamento, disponibilize a skill selecionada e os dados adversos. Preserve prompt, resposta bruta, identidade/configuração conhecida do agente, hashes dos inputs, revisão do resultado e limitações. Não execute serviços ou ferramentas com novas permissões.

Seleção positiva: pedir o entregável próprio descrito nesta entrada. Seleção negativa: usar a exclusão explícita; a resposta deve apontar competência mais adequada sem carregar esta skill. Falha: fornecer input que contraria o cenário técnico e exigir evidência antes de aprovação. Os prompts concretos do pacote consumidor devem incluir dados suficientes e um oráculo independente.

## Prompts concretos

### agent-usage-accounting-positive

Modelar ledger de tokens/cache/custo por sessão e dia com idempotência entre provedores.

### agent-usage-accounting-negative

Instrumentar CPU/RAM e latência de processo, sem tokens ou cobrança.

### agent-usage-accounting-failure

Evento r1/e1: input_total=100 incluindo cached=30, output=20, repetido duas vezes. Preço ausente. Outro request informa snapshots cumulativos 10 e 15. Evento chega após meia-noite mas ocorreu antes. Defina totais e incertezas, sem consultar preços.

Oráculo de revisão: positivo seleciona a competência própria; negativo encaminha para observability-and-diagnostics (ou competência adjacente justificada). Na falha observar: 120 not 150/240; cumulative15; missing cost unknown; event timezone; context separate. Este gabarito é revisado depois da resposta, não fornecido ao avaliador na seleção.
