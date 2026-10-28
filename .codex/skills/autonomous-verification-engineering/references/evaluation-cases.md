# Avaliações da skill

Contrato de casos; execução deve ser registrada separadamente. Não constituem testes realizados.

## Cenários técnicos preservados

- AC-01 → REQ-01: Critério com teste real e input versionado pode ser marcado APROVADO; oráculo: artefato de execução vinculado.
- AC-02 → REQ-02: Teste ignorado ou indisponível permanece NÃO VERIFICADO; oráculo: fixture sem executável.
- AC-03 → REQ-02: Alteração após validação invalida somente critérios dependentes dos inputs alterados; oráculo: teste de freshness.
- AC-04 → REQ-03: Agente sem autorização para deploy não consegue publicar mesmo quando verificação passou; oráculo: mock de fronteira + integração permitida.

## Protocolo de avaliação

Forneça um pedido concreto e os inputs mínimos a um agente em diretório isolado autorizado. Na rodada de seleção, mostre somente catálogo/descriptions, sem a resposta esperada. Na rodada de comportamento, disponibilize a skill selecionada e os dados adversos. Preserve prompt, resposta bruta, identidade/configuração conhecida do agente, hashes dos inputs, revisão do resultado e limitações. Não execute serviços ou ferramentas com novas permissões.

Seleção positiva: pedir o entregável próprio descrito nesta entrada. Seleção negativa: usar a exclusão explícita; a resposta deve apontar competência mais adequada sem carregar esta skill. Falha: fornecer input que contraria o cenário técnico e exigir evidência antes de aprovação. Os prompts concretos do pacote consumidor devem incluir dados suficientes e um oráculo independente.

## Prompts concretos

### autonomous-verification-engineering-positive

Projetar motor que atribui veredictos por critério a entregas de agentes, vinculando evidências ao snapshot.

### autonomous-verification-engineering-negative

Criar testes unitários de uma função de soma e diagnosticar um teste flaky, sem motor de aceitação.

### autonomous-verification-engineering-failure

Critério A tinha teste passando sobre arquivo X; X mudou. Critério B testa arquivo Y inalterado. O teste de C está ausente. Há uma verificação de build aprovada, mas nenhum grant de publicação. Classifique e proponha retomada; não publique.

Oráculo de revisão: positivo seleciona a competência própria; negativo encaminha para software-testing (ou competência adjacente justificada). Na falha observar: invalidate A not unrelated B; C unverified; no deploy authorization. Este gabarito é revisado depois da resposta, não fornecido ao avaliador na seleção.
