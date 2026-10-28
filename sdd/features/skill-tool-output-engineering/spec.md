# Autoria e avaliação de tool-output-engineering

Origem histórica: estudo externo; contrato vigente autocontido nesta spec. O estudo não integra a distribuição nem a validação. Ator: mantenedor/avaliador da skill. Precondição: autoria autorizada e avaliação em ambiente permitido. Esta feature pertence à biblioteca; não é feature do produto Ox.

## Contratos técnicos preservados

As declarações abaixo mantêm IDs, cenários e oráculos propostos. REQ-01..03 são competências que a skill deve ensinar. AC-01..04 exigem exercitar entregáveis concretos; revisão textual sozinha não os aprova. Integrações de produto/plataforma permanecem futuras quando não disponíveis.

- REQ-01: Cada saída transformada conserva exit code, sinais de erro e referência ao bruto.
- REQ-02: Falha de parser não converte falha em sucesso nem remove evidência crítica.
- REQ-03: Economia apresentada distingue contagem real de estimativa e preserva limites de método.

- AC-01 → REQ-01: Saída com erro relevante é resumida mantendo falha e localização; oráculo: fixtures de comando.
- AC-02 → REQ-02: ANSI, UTF-8 parcial, output binário e formato inesperado recebem fallback explícito; oráculo: corpus adverso.
- AC-03 → REQ-02: Truncamento é indicado com localização do bruto completo; oráculo: saída acima do limite.
- AC-04 → REQ-03: Contador estimado não é mostrado como tokens faturados; oráculo: caso sem informação de provedor.

## Critérios adicionais da autoria

- REQ-04: Entregar método reutilizável com seleção precisa, entradas, referências e cenários verificáveis.
- AC-05 → REQ-04: Revisão de conteúdo e validação local confirmam entrada completa, referências substantivas, fronteiras e ponte válida.
- AC-06 → REQ-04: Ensaio observado com agente distingue pedido positivo, negativo e comportamento adverso; limitações e resposta bruta preservadas.

Não substituir AC-01..04 por AC-05/06. Versões, plataforma, dados e autorização do consumidor precisam ser conhecidos antes da integração. A aprovação da skill não aprova subsistemas do produto.
