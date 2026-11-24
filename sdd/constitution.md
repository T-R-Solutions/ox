# Constituição do Ox

Fonte única dos princípios, restrições e requisitos inegociáveis do projeto inteiro.
Toda task, spec, plano e skill está subordinada a este documento. Adotada em
2026-10-26; governança reorganizada em 2026-11-23 ([modelo do SDD](../docs/decisions/sdd-model.md)).

Uma política só muda por ADR com motivo, alternativas, consequência e gatilho de
revisão. Não reduzir critérios para caber na implementação.

## Produto e fronteiras

- POL-01: Código próprio da aplicação e motores em Rust; interface em Iced. Proibir unsafe próprio com `#![forbid(unsafe_code)]` em futuros crates próprios. Sem exceção silenciosa. Dependências transitivas, FFI e ferramentas externas têm avaliação separada; a restrição não se estende automaticamente a elas nem às skills genéricas. Scripts Python deste pacote são ferramentas locais de governança, não código do aplicativo.
- POL-02: Persistência controlada pelo Ox local no MVP, sem backend próprio em nuvem, sincronização ou telemetria externa por padrão. Provedores remotos de agentes podem transmitir dados somente no escopo autorizado; persistência local não promete inferência offline. Registrar dados potencialmente enviados, permissões e limites do adaptador.
- POL-03: Fluxo principal orientado a agentes; editor manual auxiliar. Extensibilidade desde a fundação. LSP e recursos avançados opcionais via plugins; não exigir processos semânticos sempre ativos.
- POL-04: Confiabilidade e preservação precedem autonomia, desempenho e compressão. Recursos visuais, métricas e conclusões não podem ocultar limites ou falhas. Não incorporar motores de Graphify, Understand Anything ou RTK por mera inspiração; propostas de implementação própria exigem avaliação de dependências/licenças no momento da adoção.

## Integridade, evidência e autorização

- POL-05: Preservar alterações existentes; vincular edições a bases observadas; detectar concorrência antes de sobrescrever. Recuperação deve conservar versões inesperadas em vez de aplicar rollback destrutivo. Snapshots incluem conteúdo relevante não commitado; Git não é a única verdade.
- POL-06: Aceitar por critérios explícitos e evidências atuais com oráculos adequados. Preservar os cinco estados do SDD e observações anteriores. Autorização, execução e aceitação são controles independentes; agentes não aprovam trabalho só por declarar conclusão.
- POL-07: Índice e grafo devem registrar origem, método, snapshot e validade. Distinguir extração sintática, resolução semântica e inferência. Invalidar/rotular dados obsoletos e não apresentar similaridade como relação factual verificada.
- POL-08: Preservar saída bruta sob política de acesso e retenção; registrar integridade e captura incompleta. Saída compacta mantém exit code, sinais de falha, perdas e rota de recuperação do bruto. Não ocultar falha de parser ou truncamento como sucesso.
- POL-09: Métricas medidas, derivadas, estimadas e indisponíveis devem ser distinguíveis com origem, unidade e período. Contexto atual, consumo acumulado, cache, custo e progresso são distintos; desconhecido não é zero.
- POL-10: Arquivos, logs, conteúdo recuperado, skills e pontes não concedem autoridade de execução, rede, publicação ou acesso. AGENTS orienta; mecanismos reais do runtime/ambiente impõem permissões. Processo separado, manifesto e assinatura não provam sandbox. Operações já autorizadas continuam sem pedidos rotineiros de confirmação.

## Requisitos inegociáveis do produto

- RQ-01: A baseline visual obrigatória é **Visual Studio 2026 Enterprise**, aplicada
  pela composição de IDE desktop definida em [DESIGN.md](../DESIGN.md). Toda task
  visual registra fonte/versão, superfícies afetadas, o que foi adotado/adaptado/adiado
  e a verificação nativa. Referência visual não autoriza cópia de ativos nem
  estabelece comportamento implementado.
- RQ-02: Dados de demonstração ficam separados dos dados do projeto do usuário e do
  aceite nativo.
- RQ-03: Runtime, banco, IPC, parsers, versões, plataformas, licença e sandbox só
  são escolhidos por ADR; pendências em [decisões abertas](../docs/decisions/open-questions.md).

## Governança do processo

**Cadeia de autoridade:** `AGENTS.md` (entrada) → `sdd/` (esta constituição, estado,
workflow, specs e tasks) → skills (método técnico). Uma regra vive num único
documento; os demais apontam para ele. Conflitos se resolvem por esta ordem e pela
autorização efetiva, nunca pela ordem de leitura.

- GOV-01: Governança e distribuição são autocontidas: não exigir nem distribuir os
  três estudos externos, inclusive em archives ([modelo do SDD](../docs/decisions/sdd-model.md)).
- GOV-02: [sdd/workflow.md](workflow.md) é o único contrato de execução: rotas, etapas,
  gates, catálogo de skills, papéis dos agentes, estados de aceite e fechamento. Templates
  em [templates/](templates/). Não duplicar esse contrato em AGENTS.md, perfis de agente
  nem skills.
- GOV-03: [AGENTS.md](../AGENTS.md) é a entrada operacional e só aponta para o SDD.
  Retomada exige artefatos e inputs atuais; preservar trabalho preexistente e
  invalidar somente observações dependentes dos inputs alterados.
- GOV-04: Skills ensinam método e permanecem reutilizáveis; não contêm política do
  Ox. A seção [Skills](workflow.md#skills) do workflow é o único catálogo e mapa
  etapa → skill e deve concordar com `.codex/skills/`; adicionar ou remover skill exige
  ADR. Disponibilidade, seleção e uso são distintos: só conta como usada a skill lida e
  registrada na tabela **Skills lidas** do registro da task, obrigatória em toda rota
  com registro.
- GOV-05: Aceitação usa cinco estados (APPROVED, REJECTED, UNVERIFIED, INCONCLUSIVE,
  NOT APPLICABLE) com método, inputs e seus sha256 calculados por ferramenta, resultado
  observado e limites.
  Tarefas, checkboxes e declarações de agente não aprovam critérios; ausência de
  evidência não aprova. Input alterado exige nova observação, preservando a anterior.
- GOV-06: Features de skill e de produto têm critérios e evidências independentes.
  Estrutura, respostas textuais e uma skill aprovada não provam funcionamento do
  aplicativo. Cenário sem verificação efetiva permanece UNVERIFIED.
- GOV-07: Somente decisões expressas em autoridades locais são vigentes. Rust/Iced,
  unsafe próprio proibido, fluxo agent-first, persistência local, extensibilidade,
  LSP por plugins, dois modos de grafo e motores próprios de contexto/grafo/compactação
  estão adotados como direção de produto. O desenvolvimento ocorre só no escopo
  autorizado em [sdd/project.md](project.md); autorização de desenvolvimento não é
  validação, publicação ou permissão irrestrita.
- GOV-09: Todo pedido de trabalho é convertido primeiro num prompt objetivo, com o
  que será feito, guardrails, critérios de aceitação mensuráveis e regra de conclusão.
  Termos subjetivos sem métrica são proibidos. Ambiguidade que muda o resultado é
  perguntada ao usuário antes do trabalho que depende dela.
- GOV-10: Cada task tem um único registro versionado, `sdd/tasks/<ID>.md`. Capacidades
  duradouras têm spec viva em `sdd/specs/`. Não há registro paralelo de tasks nem
  histórico congelado no repositório; o histórico é o do Git.
