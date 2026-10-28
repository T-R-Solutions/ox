# Plano — fluxo completo

Contratos e recuperação mudam; rota local não é suficiente. Não há Git.
Baseline integral anterior: /tmp/ox-before-externalization-zj4erab3/before.tar.gz;
inputs.json identifica bytes observados. Restaurar somente em pasta vazia e
comparar, nunca sobrescrever trabalho posterior. Backup temporário externo não
é dependência do pacote. Histórico local de features: previous-features.tar.gz.

| ID | Requisitos | Decisão / risco | Alternativa e gatilho |
|---|---|---|---|
| D-01 | REQ-01, REQ-04 | Substituição incremental dos leitores; retirar estudos e autores antigos; pacote com manifesto explícito | Manter dependência ou renomear estudos viola pedido; rever se scanner achar conteúdo |
| D-02 | REQ-02 | IDs locais POL/GOV, mapeamento individual dos 72 IDs somente histórico; perfil versionado | Copiar pesquisa inteira duplica autoridade; rever ao mudar perfil/política |
| D-03 | REQ-03 | Histórico imutável separado; nova observação após teste ou invalidação explícita | Atualizar hashes antigos falseia execução; rever todos os inputs afetados |
| D-04 | REQ-04 | ZIP local, extração temporária fora da origem, cinco comandos e mutações | Cópia permissiva de todos os Markdown esconderia dependência |
| R-01 | REQ-01 | Conteúdo escondido em archive ou script antigo | Inspeção recursiva por nomes, hashes e sequência de linhas |
| R-02 | REQ-02 | Verificador enfraquecido ou cobertura com IDs inexistentes | Mutações de inventário, IDs, paths e links; SDD preservado byte a byte |
| R-03 | REQ-03 | Evidências obsoletas apresentadas como atuais | Snapshots imutáveis, estados novos, inputs de contratos/implementação/oráculos |
| R-04 | REQ-04 | Extração usa pasta-pai, symlink ou arquivo não distribuído | Processos executados na extração, auditoria de acessos e manifesto |

| Competência | Ponte/versão | Entrada consultada | Papel, pergunta e entrega |
|---|---|---|---|
| software-evolution | sdd/chain/software-evolution.md / 1 | .codex/skills/software-evolution/SKILL.md | Primária: como retirar dependências sem falsificar história? Migração, ordem de corte e recuperação |
| software-testing | sdd/chain/software-testing.md / 1 | .codex/skills/software-testing/SKILL.md | Auxiliar: como demonstrar independência e sensibilidade a falhas? Casos adversariais e smoke test |

Ambas selecionadas, identidade confirmada, consultadas e utilizadas. Referências
de transição/migração da primária lidas. Nenhuma delegação ou agente externo.

Compatibilidade: configuração antiga conserva seus registros no acervo, mas seus
autores/validadores não são suportados na revisão nova. Consumidor novo usa somente
árvore local. Não há runtime, banco, serviço ou implantação concorrente. O ponto
de retorno é o backup completo externo; não misturar evidências entre revisões.

Arquivos afetados: README, contexto/constituição/ADRs, fixtures de perfil/cobertura,
check-ox, testes, runner, empacotamento e evidências das features. Entradas técnicas
das skills, pontes e núcleo SDD são preservados. Testes atuais devem detectar os
defeitos caracterizados antes do corte; falhas de cada rodada serão conservadas.
