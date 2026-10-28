# Revisão dos ensaios observados

Data: 2026-10-26. Revisor: agente principal autor da biblioteca; avaliadores: três subagentes internos, configuração herdada do ambiente, identificados nos registros. A ferramenta não expôs versão imutável do modelo nem seed; repetibilidade de modelo é limitada. Não se alegam avaliação humana, comparação A/B, taxa geral de acerto ou eficácia em produção.

Método: comparar os 27 IDs/respostas integrais dos grupos 1–3 com os prompts e oráculos de `src/fixtures/evaluation-*.json`, depois da resposta. Na seleção foram fornecidas descrições, não gabaritos. No comportamento foram fornecidas skills e referências; existem exemplos próximos aos casos. Grupo 2 viu incidentalmente prompts de comportamento na leitura inicial e teve truncamento parcial de autoridades. Grupo 1 consultou README antes de sua criação. Essas limitações ficam preservadas nos registros brutos; não afetam a existência das respostas, mas impedem chamar o ensaio de avaliação cega rigorosa ou de generalização.

Inputs das skills/catálogo/prompts foram capturados em `observed-inputs.json` e `observed-inputs.tar.gz` a partir dos bytes que permaneceram estáveis durante o ensaio. Autoridades operacionais evoluíam durante a preparação; não se atribui a elas uma versão completa inferida retroativamente. Os relatórios informam o que foi lido e a lacuna de README. O snapshot comprova identidade local, não autentica externamente a sessão.

| Skill / três casos | Seleção positiva | Seleção negativa observada | Comportamento adverso revisado | Resultado limitado |
|---|---|---|---|---|
| plugin-protocol-engineering | Própria | software-design, justificada: SDK estável e linguagem ausente | Só read A; processo não é sandbox; gravação contradiz grant; reconciliação antes de replay | APROVADO para estes três prompts |
| agent-runtime-engineering | Própria | ai-engineering | Evento antigo ligado a A, aceitação separada, streams drenados, cancelamento observado e limpeza por SO | APROVADO para estes três prompts |
| autonomous-verification-engineering | Própria | software-testing | A obsoleto, B preservado somente se todos inputs atuais, C não verificado, build não autoriza publicar | APROVADO para estes três prompts |
| workspace-integrity-engineering | Própria | database-engineering | Conflito H0/H1, escape negado, janela TOCTOU explicitada, recuperação por conteúdo, watcher como hint | APROVADO para estes três prompts |
| iced-engineering | Própria | design-review | Geração/época, suspensão de grafo oculto, foco visível, versão/API não inventada | APROVADO para estes três prompts |
| code-context-engineering | Própria | ai-engineering | Homônimos não resolvidos, offsets recalculados, rename invalidado, LSP ausente rotulado | APROVADO para estes três prompts |
| code-knowledge-graph-engineering | Própria | Nenhuma do catálogo, justificada: marketing estático não exige design system | Inferência não verificada; snapshot invalidado; ciclo/hub limitados; números declarados exemplos, não metas ou medições | APROVADO para estes três prompts |
| tool-output-engineering | Própria | observability-and-diagnostics | exit=1 conservado, fallback e perdas explícitos, instrução maliciosa tratada como dado, custo indisponível | APROVADO para estes três prompts |
| agent-usage-accounting | Própria | observability-and-diagnostics | 120 tokens sem dupla contagem; acumulado 15 separado sem categoria; tarifa/fuso não inventados | APROVADO para estes três prompts |

Os dois encaminhamentos negativos distintos do nome sugerido no gabarito não são defeitos: a condição normativa é não selecionar a especialização fora de seu escopo e justificar a alternativa. Não se alteraram os critérios técnicos originais para aprovar o ensaio.

Resultado observado: 9 seleções positivas, 9 exclusões negativas e 9 respostas adversas revisadas, sem violação material encontrada nos oráculos delimitados. Isso sustenta somente AC-06 de resposta textual observada. Os 36 critérios AC-01..04 permanecem NÃO VERIFICADO para os entregáveis/integrações que seus oráculos exigem. As respostas propostas não são testes de processos, UI, sandbox, índices ou provedores executados.

Retomada de avaliação: em novo diretório de `docs/validation/agent-evals/`, fornecer apenas catálogo e prompts de seleção antes de revelar skills; escolher casos inéditos que não reproduzam exemplos; registrar modelo/configuração/versionamento quando disponíveis; preservar respostas e comparar com gabarito depois. Integração exige consumidor autorizado e execução dos quatro cenários da spec de cada skill. Não executar serviços pagos ou agentes externos por este registro.
