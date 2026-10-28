# Autoria e avaliação de workspace-integrity-engineering

Origem histórica: estudo externo; contrato vigente autocontido nesta spec. O estudo não integra a distribuição nem a validação. Ator: mantenedor/avaliador da skill. Precondição: autoria autorizada e avaliação em ambiente permitido. Esta feature pertence à biblioteca; não é feature do produto Ox.

## Contratos técnicos preservados

As declarações abaixo mantêm IDs, cenários e oráculos propostos. REQ-01..03 são competências que a skill deve ensinar. AC-01..04 exigem exercitar entregáveis concretos; revisão textual sozinha não os aprova. Integrações de produto/plataforma permanecem futuras quando não disponíveis.

- REQ-01: Todas as mudanças em arquivos respeitam raiz autorizada e versão observada.
- REQ-02: Edições concorrentes são detectadas antes de sobrescrita silenciosa.
- REQ-03: Queda durante escrita permite detectar o estado parcial e recuperar sem perda silenciosa.

- AC-01 → REQ-01: Tentativa de escrita fora da raiz via .. ou symlink é rejeitada; oráculo: fixture com caminhos adversos.
- AC-02 → REQ-02: Dois agentes editam mesma versão: segunda gravação conflita ou aplica merge verificado; oráculo: teste concorrente.
- AC-03 → REQ-03: Falha injetada entre arquivo temporário e rename não deixa registro “concluído” incorreto; oráculo: teste de crash.
- AC-04 → REQ-03: Arquivo externo alterado invalida hash/snapshot; oráculo: watcher + verificação por leitura real.

## Critérios adicionais da autoria

- REQ-04: Entregar método reutilizável com seleção precisa, entradas, referências e cenários verificáveis.
- AC-05 → REQ-04: Revisão de conteúdo e validação local confirmam entrada completa, referências substantivas, fronteiras e ponte válida.
- AC-06 → REQ-04: Ensaio observado com agente distingue pedido positivo, negativo e comportamento adverso; limitações e resposta bruta preservadas.

Não substituir AC-01..04 por AC-05/06. Versões, plataforma, dados e autorização do consumidor precisam ser conhecidos antes da integração. A aprovação da skill não aprova subsistemas do produto.
