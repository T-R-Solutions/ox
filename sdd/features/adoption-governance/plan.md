# Plano de adoção — rota completa

Registro anterior à cópia/adaptação de conteúdo autoral. Rota completa por contratos, governança, consumidores independentes e integridade. Baseline inicial já capturada; nenhuma alteração preexistente será sobrescrita.

| ID | Requisitos | Decisão / risco | Alternativa e custo | Reavaliar |
|---|---|---|---|---|
| D-01 | REQ-01 | Cópias completas e snapshots locais com SHA-256 | Referências à biblioteca externa quebrariam portabilidade | Atualização upstream |
| D-02 | REQ-02 | 20 existentes e 9 novas; autoria começa PLUG, AGENT, VERIFY | Duplicar competências absorvidas aumenta ambiguidade | Avaliação real de seleção |
| D-03 | REQ-03 | Constituição única em docs; sdd/constitution.md aponta autoridade | Duas políticas concorrentes causariam deriva | Mudança autorizada de política |
| D-04 | REQ-04 | Checks stdlib e casos controlados; integração futura separada | Implementar o produto excederia o pedido | Disponibilidade do produto |
| R-01 | REQ-01 | Escrita fora da raiz ou perda de origem | Comparar baseline local de recursos; estudos retirados pela ADR governance-externalization | Qualquer divergência |
| R-02 | REQ-02 | Novas skills vagas ou sobrepostas | Referências concretas e prompts positivos/negativos | Falha observada |
| R-03 | REQ-03 | Proposta promovida a decisão; aprovação falsa | Mapa normativo e convergência por AC | Mudança de contrato |
| R-04 | REQ-04 | Oráculo só testa palavras ou confunde simulação e produto | Testes de mutação do validador e avaliação delimitada | Evidência insuficiente |

Competência primária consultada: skill-creator do ambiente, versão não declarada. Conteúdo histórico de origem preservado em docs/validation/governance-externalization/historical-authoring.tar.gz; sem ponte no Ox, sem instalação. Pergunta: como autorar competências reutilizáveis com seleção precisa e referências progressivas? Entrega: nove entradas, referências e casos. Inspeção das entradas da biblioteca serve à comparação, não declara uso de todas elas. Novas skills não foram consultadas durante sua própria autoria. Auxiliares não selecionadas automaticamente.

Ordem: baseline e contratos; PLUG → AGENT → VERIFY; workspace e Iced; contexto → grafo; output e contabilidade sobre contratos de eventos. Essa dependência orienta autoria, sem impor bibliotecas em runtime.

Revisão vigente: critérios substituídos pela ADR governance-externalization. Plano histórico acima descreve a autoria inicial; nova aceitação usa inputs locais e nova evidência. Competências atuais e riscos da migração registrados no plan da feature governance-externalization.
