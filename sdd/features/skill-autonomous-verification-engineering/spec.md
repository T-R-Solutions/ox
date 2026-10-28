# Autoria e avaliação de autonomous-verification-engineering

Origem histórica: estudo externo; contrato vigente autocontido nesta spec. O estudo não integra a distribuição nem a validação. Ator: mantenedor/avaliador da skill. Precondição: autoria autorizada e avaliação em ambiente permitido. Esta feature pertence à biblioteca; não é feature do produto Ox.

## Contratos técnicos preservados

As declarações abaixo mantêm IDs, cenários e oráculos propostos. REQ-01..03 são competências que a skill deve ensinar. AC-01..04 exigem exercitar entregáveis concretos; revisão textual sozinha não os aprova. Integrações de produto/plataforma permanecem futuras quando não disponíveis.

- REQ-01: Todo veredicto está vinculado a critério explícito, método e snapshot dos inputs.
- REQ-02: Falha, não execução ou evidência obsoleta não são promovidas a aprovado.
- REQ-03: Permissão de execução e aceitação de resultado são controles independentes.

- AC-01 → REQ-01: Critério com teste real e input versionado pode ser marcado APROVADO; oráculo: artefato de execução vinculado.
- AC-02 → REQ-02: Teste ignorado ou indisponível permanece NÃO VERIFICADO; oráculo: fixture sem executável.
- AC-03 → REQ-02: Alteração após validação invalida somente critérios dependentes dos inputs alterados; oráculo: teste de freshness.
- AC-04 → REQ-03: Agente sem autorização para deploy não consegue publicar mesmo quando verificação passou; oráculo: mock de fronteira + integração permitida.

## Critérios adicionais da autoria

- REQ-04: Entregar método reutilizável com seleção precisa, entradas, referências e cenários verificáveis.
- AC-05 → REQ-04: Revisão de conteúdo e validação local confirmam entrada completa, referências substantivas, fronteiras e ponte válida.
- AC-06 → REQ-04: Ensaio observado com agente distingue pedido positivo, negativo e comportamento adverso; limitações e resposta bruta preservadas.

Não substituir AC-01..04 por AC-05/06. Versões, plataforma, dados e autorização do consumidor precisam ser conhecidos antes da integração. A aprovação da skill não aprova subsistemas do produto.
