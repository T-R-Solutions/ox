# Autoria e avaliação de iced-engineering

Origem histórica: estudo externo; contrato vigente autocontido nesta spec. O estudo não integra a distribuição nem a validação. Ator: mantenedor/avaliador da skill. Precondição: autoria autorizada e avaliação em ambiente permitido. Esta feature pertence à biblioteca; não é feature do produto Ox.

## Contratos técnicos preservados

As declarações abaixo mantêm IDs, cenários e oráculos propostos. REQ-01..03 são competências que a skill deve ensinar. AC-01..04 exigem exercitar entregáveis concretos; revisão textual sozinha não os aprova. Integrações de produto/plataforma permanecem futuras quando não disponíveis.

- REQ-01: A UI não bloqueia em processos, busca, indexação ou eventos de agentes.
- REQ-02: Estados, foco, redimensionamento e navegação são previsíveis e acessíveis.
- REQ-03: Views customizadas e grafos não executam processamento custoso quando ocultos.

- AC-01 → REQ-01: Operação lenta simulada não bloqueia navegação/interação; oráculo: teste de integração com heartbeat de UI.
- AC-02 → REQ-02: Painel expandido/recolhido preserva conteúdo e foco definidos; oráculo: teste funcional de estados.
- AC-03 → REQ-02: Redimensionamento extremo não perde ações essenciais; oráculo: revisão de layout em tamanhos documentados.
- AC-04 → REQ-03: Grafo oculto não agenda re-layout contínuo; oráculo: instrumentação sob workload controlado.

## Critérios adicionais da autoria

- REQ-04: Entregar método reutilizável com seleção precisa, entradas, referências e cenários verificáveis.
- AC-05 → REQ-04: Revisão de conteúdo e validação local confirmam entrada completa, referências substantivas, fronteiras e ponte válida.
- AC-06 → REQ-04: Ensaio observado com agente distingue pedido positivo, negativo e comportamento adverso; limitações e resposta bruta preservadas.

Não substituir AC-01..04 por AC-05/06. Versões, plataforma, dados e autorização do consumidor precisam ser conhecidos antes da integração. A aprovação da skill não aprova subsistemas do produto.
