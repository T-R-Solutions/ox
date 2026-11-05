# Autoria e avaliação de plugin-protocol-engineering

Origem histórica: estudo externo; contrato vigente autocontido nesta spec. O estudo não integra a distribuição nem a validação. Ator: mantenedor/avaliador da skill. Precondição: autoria autorizada e avaliação em ambiente permitido. Esta feature pertence à biblioteca; não é feature do produto Ox.

## Contratos técnicos preservados

As declarações abaixo mantêm IDs, cenários e oráculos propostos. REQ-01..03 são competências que a skill deve ensinar. AC-01..04 exigem exercitar entregáveis concretos; revisão textual sozinha não os aprova. Integrações de produto/plataforma permanecem futuras quando não disponíveis.

- REQ-01: Negociar versão e capacidades sem executar operações ainda não autorizadas.
- REQ-02: Rejeitar mensagens, plugins e chamadas inválidas sem corromper estado do host.
- REQ-03: Definir compatibilidade e recuperação quando plugin trava, desconecta ou muda versão.

- AC-01 → REQ-01: Plugin compatível e autorizado negocia apenas capacidades concedidas; oráculo: fixture de cliente/provedor e asserts de mensagens.
- AC-02 → REQ-02: Plugin incompatível ou malformado recebe falha explícita sem mutação persistente; oráculo: harness de compatibilidade.
- AC-03 → REQ-03: Plugin encerra durante operação e host recupera/expira recursos sem bloqueio; oráculo: teste de crash e timeout.
- AC-04 → REQ-03: Plugin sem permissão tenta ler caminho protegido e o host bloqueia efeito; oráculo: integração em sandbox no SO alvo.

## Critérios adicionais da autoria

- REQ-04: Entregar método reutilizável com seleção precisa, entradas, referências e cenários verificáveis.
- AC-05 → REQ-04: Revisão de conteúdo e validação local confirmam entrada completa, referências substantivas, fronteiras e ponte válida.
- AC-06 → REQ-04: Ensaio observado com agente distingue pedido positivo, negativo e comportamento adverso; limitações e resposta bruta preservadas.

Não substituir AC-01..04 por AC-05/06. Versões, plataforma, dados e autorização do consumidor precisam ser conhecidos antes da integração. A aprovação da skill não aprova subsistemas do produto.
