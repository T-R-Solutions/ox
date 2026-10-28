# Autoria e avaliação de agent-runtime-engineering

Origem histórica: estudo externo; contrato vigente autocontido nesta spec. O estudo não integra a distribuição nem a validação. Ator: mantenedor/avaliador da skill. Precondição: autoria autorizada e avaliação em ambiente permitido. Esta feature pertence à biblioteca; não é feature do produto Ox.

## Contratos técnicos preservados

As declarações abaixo mantêm IDs, cenários e oráculos propostos. REQ-01..03 são competências que a skill deve ensinar. AC-01..04 exigem exercitar entregáveis concretos; revisão textual sozinha não os aprova. Integrações de produto/plataforma permanecem futuras quando não disponíveis.

- REQ-01: Sessões e tarefas têm estados legais, identificadores estáveis e transições rejeitadas.
- REQ-02: Cancelamento, encerramento e reinício liberam recursos sem alterar escopo de permissão.
- REQ-03: Ações observadas e conclusões declaradas por agentes têm proveniência distinta.

- AC-01 → REQ-01: Evento fora de ordem não produz conclusão indevida; oráculo: teste de transição com sequência adversa.
- AC-02 → REQ-02: Morte do processo gera status e cleanup de recursos associados; oráculo: processo controlado com falha injetada.
- AC-03 → REQ-02: Cancelamento durante saída intensa não deixa tarefas órfãs; oráculo: harness com streams e deadline.
- AC-04 → REQ-03: Mensagem “concluído” sem artefato validado não muda veredicto para aprovado; oráculo: caso adverso determinístico.

## Critérios adicionais da autoria

- REQ-04: Entregar método reutilizável com seleção precisa, entradas, referências e cenários verificáveis.
- AC-05 → REQ-04: Revisão de conteúdo e validação local confirmam entrada completa, referências substantivas, fronteiras e ponte válida.
- AC-06 → REQ-04: Ensaio observado com agente distingue pedido positivo, negativo e comportamento adverso; limitações e resposta bruta preservadas.

Não substituir AC-01..04 por AC-05/06. Versões, plataforma, dados e autorização do consumidor precisam ser conhecidos antes da integração. A aprovação da skill não aprova subsistemas do produto.
