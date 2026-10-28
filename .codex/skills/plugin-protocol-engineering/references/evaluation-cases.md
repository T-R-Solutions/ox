# Avaliações da skill

Contrato de casos; execução deve ser registrada separadamente. Não constituem testes realizados.

## Cenários técnicos preservados

- AC-01 → REQ-01: Plugin compatível e autorizado negocia apenas capacidades concedidas; oráculo: fixture de cliente/provedor e asserts de mensagens.
- AC-02 → REQ-02: Plugin incompatível ou malformado recebe falha explícita sem mutação persistente; oráculo: harness de compatibilidade.
- AC-03 → REQ-03: Plugin encerra durante operação e host recupera/expira recursos sem bloqueio; oráculo: teste de crash e timeout.
- AC-04 → REQ-03: Plugin sem permissão tenta ler caminho protegido e o host bloqueia efeito; oráculo: integração em sandbox no SO alvo.

## Protocolo de avaliação

Forneça um pedido concreto e os inputs mínimos a um agente em diretório isolado autorizado. Na rodada de seleção, mostre somente catálogo/descriptions, sem a resposta esperada. Na rodada de comportamento, disponibilize a skill selecionada e os dados adversos. Preserve prompt, resposta bruta, identidade/configuração conhecida do agente, hashes dos inputs, revisão do resultado e limitações. Não execute serviços ou ferramentas com novas permissões.

Seleção positiva: pedir o entregável próprio descrito nesta entrada. Seleção negativa: usar a exclusão explícita; a resposta deve apontar competência mais adequada sem carregar esta skill. Falha: fornecer input que contraria o cenário técnico e exigir evidência antes de aprovação. Os prompts concretos do pacote consumidor devem incluir dados suficientes e um oráculo independente.

## Prompts concretos

### plugin-protocol-engineering-positive

Criar um protocolo host/plugin para um provedor LSP com negociação de versão e permissões.

### plugin-protocol-engineering-negative

Adicionar uma regra de lint usando um SDK de plugins já estável, sem alterar protocolo ou permissões.

### plugin-protocol-engineering-failure

Host oferece read/search; plugin pede read/write; grant é read na raiz A. O plugin em processo separado diz que pode ler a raiz B diretamente e cai após gravar mas antes de responder. Proponha contrato e verificações; não execute processos.

Oráculo de revisão: positivo seleciona a competência própria; negativo encaminha para api-testing (ou competência adjacente justificada). Na falha observar: effective read A only; process is not sandbox; reconcile uncertain effect before retry. Este gabarito é revisado depois da resposta, não fornecido ao avaliador na seleção.
