# Avaliações da skill

Contrato de casos; execução deve ser registrada separadamente. Não constituem testes realizados.

## Cenários técnicos preservados

- AC-01 → REQ-01: Evento fora de ordem não produz conclusão indevida; oráculo: teste de transição com sequência adversa.
- AC-02 → REQ-02: Morte do processo gera status e cleanup de recursos associados; oráculo: processo controlado com falha injetada.
- AC-03 → REQ-02: Cancelamento durante saída intensa não deixa tarefas órfãs; oráculo: harness com streams e deadline.
- AC-04 → REQ-03: Mensagem “concluído” sem artefato validado não muda veredicto para aprovado; oráculo: caso adverso determinístico.

## Protocolo de avaliação

Forneça um pedido concreto e os inputs mínimos a um agente em diretório isolado autorizado. Na rodada de seleção, mostre somente catálogo/descriptions, sem a resposta esperada. Na rodada de comportamento, disponibilize a skill selecionada e os dados adversos. Preserve prompt, resposta bruta, identidade/configuração conhecida do agente, hashes dos inputs, revisão do resultado e limitações. Não execute serviços ou ferramentas com novas permissões.

Seleção positiva: pedir o entregável próprio descrito nesta entrada. Seleção negativa: usar a exclusão explícita; a resposta deve apontar competência mais adequada sem carregar esta skill. Falha: fornecer input que contraria o cenário técnico e exigir evidência antes de aprovação. Os prompts concretos do pacote consumidor devem incluir dados suficientes e um oráculo independente.

## Prompts concretos

### agent-runtime-engineering-positive

Projetar adaptador CLI com streaming, cancelamento, reconexão e supervisão de processos.

### agent-runtime-engineering-negative

Comparar qualidade de respostas de dois modelos sem ferramentas nem processos.

### agent-runtime-engineering-failure

Execução A declarou concluído, encerrou sem testes, e seu evento atrasado chegou depois do início de B. B produz stdout/stderr intensamente e ignora cancelamento cooperativo. Descreva transições, controle e evidência; não execute processos.

Oráculo de revisão: positivo seleciona a competência própria; negativo encaminha para ai-engineering (ou competência adjacente justificada). Na falha observar: generation isolation; done not accepted; bounded drain and observed cleanup. Este gabarito é revisado depois da resposta, não fornecido ao avaliador na seleção.
