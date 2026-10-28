# Autoria e avaliação de code-knowledge-graph-engineering

Origem histórica: estudo externo; contrato vigente autocontido nesta spec. O estudo não integra a distribuição nem a validação. Ator: mantenedor/avaliador da skill. Precondição: autoria autorizada e avaliação em ambiente permitido. Esta feature pertence à biblioteca; não é feature do produto Ox.

## Contratos técnicos preservados

As declarações abaixo mantêm IDs, cenários e oráculos propostos. REQ-01..03 são competências que a skill deve ensinar. AC-01..04 exigem exercitar entregáveis concretos; revisão textual sozinha não os aprova. Integrações de produto/plataforma permanecem futuras quando não disponíveis.

- REQ-01: Nós/arestas têm tipos, identidade e proveniência ligada ao snapshot.
- REQ-02: Relações inferidas não são apresentadas como fatos extraídos/resolvidos.
- REQ-03: Grafos densos operam com limites de consulta e não bloqueiam a interface.

- AC-01 → REQ-01: Aresta de chamada válida pode ser rastreada a localização e método; oráculo: corpus sintético conhecido.
- AC-02 → REQ-02: Relação inferida marcada incorretamente como verificada é rejeitada; oráculo: schema/assert de proveniência.
- AC-03 → REQ-03: Alteração remove aresta obsoleta no snapshot novo; oráculo: fixture antes/depois.
- AC-04 → REQ-03: Consulta por subgrafo aplica limite e relatórios de truncamento; oráculo: grafo grande gerado determinísticamente.

## Critérios adicionais da autoria

- REQ-04: Entregar método reutilizável com seleção precisa, entradas, referências e cenários verificáveis.
- AC-05 → REQ-04: Revisão de conteúdo e validação local confirmam entrada completa, referências substantivas, fronteiras e ponte válida.
- AC-06 → REQ-04: Ensaio observado com agente distingue pedido positivo, negativo e comportamento adverso; limitações e resposta bruta preservadas.

Não substituir AC-01..04 por AC-05/06. Versões, plataforma, dados e autorização do consumidor precisam ser conhecidos antes da integração. A aprovação da skill não aprova subsistemas do produto.
