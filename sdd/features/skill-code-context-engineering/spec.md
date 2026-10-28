# Autoria e avaliação de code-context-engineering

Origem histórica: estudo externo; contrato vigente autocontido nesta spec. O estudo não integra a distribuição nem a validação. Ator: mantenedor/avaliador da skill. Precondição: autoria autorizada e avaliação em ambiente permitido. Esta feature pertence à biblioteca; não é feature do produto Ox.

## Contratos técnicos preservados

As declarações abaixo mantêm IDs, cenários e oráculos propostos. REQ-01..03 são competências que a skill deve ensinar. AC-01..04 exigem exercitar entregáveis concretos; revisão textual sozinha não os aprova. Integrações de produto/plataforma permanecem futuras quando não disponíveis.

- REQ-01: Consultas retornam contexto ligado a uma versão identificável do repositório.
- REQ-02: Modificações incrementais invalidam resultados dependentes sem exigir varredura completa por padrão.
- REQ-03: Dados sintáticos, resolvidos semanticamente e inferidos permanecem distinguíveis.

- AC-01 → REQ-01: Consulta de símbolo relata arquivo, intervalo, snapshot e método; oráculo: fixtures com posições verificadas.
- AC-02 → REQ-02: Renomeação/edição invalida entradas antigas e atualiza as afetadas; oráculo: mutações controladas de repositório.
- AC-03 → REQ-03: Chamada ambígua sem semântica não é rotulada como referência verificada; oráculo: código homônimo e imports.
- AC-04 → REQ-03: LSP ausente resulta em degradação explícita, sem resultado inventado; oráculo: servidor deliberadamente indisponível.

## Critérios adicionais da autoria

- REQ-04: Entregar método reutilizável com seleção precisa, entradas, referências e cenários verificáveis.
- AC-05 → REQ-04: Revisão de conteúdo e validação local confirmam entrada completa, referências substantivas, fronteiras e ponte válida.
- AC-06 → REQ-04: Ensaio observado com agente distingue pedido positivo, negativo e comportamento adverso; limitações e resposta bruta preservadas.

Não substituir AC-01..04 por AC-05/06. Versões, plataforma, dados e autorização do consumidor precisam ser conhecidos antes da integração. A aprovação da skill não aprova subsistemas do produto.
