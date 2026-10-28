# Autoria e avaliação de agent-usage-accounting

Origem histórica: estudo externo; contrato vigente autocontido nesta spec. O estudo não integra a distribuição nem a validação. Ator: mantenedor/avaliador da skill. Precondição: autoria autorizada e avaliação em ambiente permitido. Esta feature pertence à biblioteca; não é feature do produto Ox.

## Contratos técnicos preservados

As declarações abaixo mantêm IDs, cenários e oráculos propostos. REQ-01..03 são competências que a skill deve ensinar. AC-01..04 exigem exercitar entregáveis concretos; revisão textual sozinha não os aprova. Integrações de produto/plataforma permanecem futuras quando não disponíveis.

- REQ-01: Registros distinguem medição fornecida pelo provedor, derivação e estimativa.
- REQ-02: Eventos duplicados não ampliam indevidamente total de tokens/custos.
- REQ-03: Contexto, consumo acumulado, custo e progresso são métricas independentes.

- AC-01 → REQ-01: Uso sem preço disponível retorna custo desconhecido, não zero; oráculo: fixture de modelo sem tarifa.
- AC-02 → REQ-02: Reenvio duplicado de evento com mesmo ID não duplica soma; oráculo: teste de replay.
- AC-03 → REQ-03: Tokens em cache, entrada e saída são agregados conforme contrato observado; oráculo: fixture de provedor.
- AC-04 → REQ-03: Intervalo diário usa timezone explicitado e não altera valor de contexto atual; oráculo: fronteira de dia/hora.

## Critérios adicionais da autoria

- REQ-04: Entregar método reutilizável com seleção precisa, entradas, referências e cenários verificáveis.
- AC-05 → REQ-04: Revisão de conteúdo e validação local confirmam entrada completa, referências substantivas, fronteiras e ponte válida.
- AC-06 → REQ-04: Ensaio observado com agente distingue pedido positivo, negativo e comportamento adverso; limitações e resposta bruta preservadas.

Não substituir AC-01..04 por AC-05/06. Versões, plataforma, dados e autorização do consumidor precisam ser conhecidos antes da integração. A aprovação da skill não aprova subsistemas do produto.
