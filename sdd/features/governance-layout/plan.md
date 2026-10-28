# Plano — organização da governança

Rota completa: a mudança alcança a allowlist de distribuição, guards de
preservação e consumidores de evidências. Autorização: pedido do mantenedor nesta
sessão. Baseline sem Git em docs/validation/governance-layout/before.tar.gz e
before.json, capturada antes das edições; o check-ox original passou.

| ID | Decisão / risco | Relação |
| --- | --- | --- |
| D-01 | Scripts e testes em tools/governance/; fixtures sob tests/; perfil e cobertura em config/governance/ | REQ-01, REQ-02 |
| D-02 | Atualizar raízes Python, comandos e rastreabilidade; preservar métodos SDD e skills; ADR própria documenta caminhos históricos | REQ-02, REQ-04 |
| D-03 | Allowlist explícita para tools/governance/ e config/governance/, retirando src/ | REQ-03 |
| D-04 | Arquivar envelopes antigos; reexaminar critérios afetados; traduzir somente caminhos na comparação das rastreabilidades históricas | REQ-04 |
| R-01 | Raiz Python incorreta ou fixture tratada como configuração | REQ-01, REQ-02 |
| R-02 | Caminho obsoleto ou guard enfraquecido pela migração | REQ-02, REQ-04 |
| R-03 | Pacote incluir aplicativo ou omitir configuração necessária | REQ-03 |
| R-04 | Reciclar hash de resultado antigo ou promover cenários sem implementação | REQ-04 |

Skill primária selecionada, consultada e usada: software-delivery,
`.codex/skills/software-delivery/SKILL.md`; versão não declarada pela entrada;
ponte `sdd/chain/software-delivery.md`, bridge_version 1. Contribuição:
definir inputs e limites do artefato, ajustar allowlist, conferir identidade do
ZIP e executar os comandos existentes em extração independente. Não há promoção,
publicação, instalação ou necessidade de auxiliares/delegação.

Alternativa rejeitada: scripts/ e tests/ genéricos na raiz dispersariam ferramentas
específicas de governança. Manter src/ na allowlist poderia incluir fontes futuras
do aplicativo. Copiar o perfil para fixtures duplicaria uma autoridade vigente.

Preservação: perfil e fixtures mantêm bytes; cobertura atualiza oráculo e o hash
de GOV-04 após corrigir o link do perfil, sem mudar política. Registros históricos
em docs/validation/, revisions e ADRs antigos permanecem intactos. O guard original
aceita apenas o mesmo perfil no destino novo e a tradução determinística de
caminhos dos JSONs de rastreabilidade, comparada aos bytes da baseline original.
Qualquer outra alteração desses contratos continua falhando.

Recuperação: copiar a distribuição em pasta vazia, conferir os 384 arquivos
inalterados de recovery.json por before.json e extrair por cima as 55 versões
anteriores de before.tar.gz; comparar o conjunto de 439 inputs. O archive contém
somente versões alteradas/movidas para evitar duplicar archives históricos e
exceder o orçamento de inspeção recursiva de 128 MiB. A cópia completa original
fica preservada em dist/governance-layout-recovery/, fora da distribuição e sem
ser necessária à recuperação. Antes de restaurar seletivamente na árvore de
trabalho, preservar versões inesperadas. Não sobrescrever a árvore inteira.
Aceitação: testes existentes, mutações focadas dos guards, inspeção do
mapeamento, revisão de continuidade, freshness e pacote independente. Inputs e
saídas de observações novas são registrados separadamente, sem hashes circulares.
