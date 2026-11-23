# Fronteiras de confiança da implementação local

Este registro aplica a [constituição](../constitution.md) sem criar política concorrente.
AGENTS, pontes e skills orientam; não implementam contenção. A inspeção de fontes
em 17/11/2026 substitui as afirmações de ausência de host/runtime da baseline de
governança. Presença de código e testes não demonstra isolamento operacional.
Estados atuais de aceite pertencem ao `evidence.json` de cada feature.

| Fronteira e dados | Implementação e controle local | Limite e verificação necessária |
| --- | --- | --- |
| Plugin → host: frames e operação echo | `application/crates/ox-plugin/src/host.rs`: protocolo 1.0, grant echo, frame de até 1024 bytes, token alfanumérico de até 900 bytes, prazo de até 10 s; socket em diretório exclusivo 0700 sob `temp_dir()` | Host implementado como biblioteca independente. Grant de protocolo não restringe filesystem/rede do processo; autenticação de peer hostil e sandbox não demonstrados |
| Processo → SO: executável, ambiente e diretório | `application/crates/ox-agent/src/runtime.rs`: executável absoluto, diretório de trabalho, streams nulos, cancelamento/prazo e reap do filho direto | Não contém descendentes nem nega acesso externo ao diretório. É supervisão, sem sandbox; filesystem/rede/segredos dependem das permissões do SO |
| UI → auxiliares locais: tarefa e oráculo | `application/crates/ox-ui/src/desktop.rs` deriva o diretório de binários de `current_exe()`; `local_task.rs` seleciona `local-task` e `task-oracle` nessa pasta | Diretório de instalação e binários são inputs confiados; caminho absoluto não autentica bytes nem impede substituição hostil |
| Seletor de pasta → UI: caminho retornado | `application/crates/ox-ui/src/desktop/folder_picker.rs`: `zenity` resolvido por PATH, argumentos separados sem shell, stdout limitado a 64 KiB e cancelamento do filho direto | PATH e executável instalado são confiados. A seleção é um dado; o Controller ainda canonicaliza e valida o diretório. Não executa código do projeto ao selecioná-lo |
| UI → diretório do usuário: artefatos da tentativa | `application/crates/ox-ui/src/local_task.rs`: canonicalização e leitura do workspace, diretório exclusivo de tentativa, request com criação exclusiva | Validar diretório não concede contenção contra troca hostil de caminhos. Tarefa escreve artefatos no workspace selecionado; abertura de projeto não executa a tarefa automaticamente |
| UI → estado local: recentes | `application/crates/ox-ui/src/desktop/project_store.rs`: `XDG_STATE_HOME` ou `HOME/.local/state`, caminho absoluto, `ox/recent-projects.v1`, até 20 caminhos canônicos, lock lateral e publicação por rename após sync | Metadados de conveniência, separados de tarefas/evidências. Há rejeições de symlinks/arquivos especiais; não confina substituição hostil de caminhos nem prova durabilidade após falta de energia |
| Implementação → veredicto: código, inputs e resultado | `application/crates/ox-verification/src/engine.rs`: oráculo local, snapshots por bytes antes/depois, histórico em memória e invalidação | Oráculo e executável fazem parte da base confiada. Exit zero não prova qualquer critério externo ao contrato do oráculo; não há aceite permanente nem armazenamento geral de evidências |
| Logs/arquivos/contexto → agente | Conteúdo permanece dado, sem ampliar autoridade, conforme POL-10 | Regra documental; nenhuma proteção de runtime contra prompt injection é demonstrada por este inventário |
| Agente → provedor remoto | Adaptadores reais e transmissão não implementados nessas fatias locais | Escopo, consentimento, dados enviados e capacidades precisam de verificação na futura integração; não há alegação de agente remoto operacional |

As fontes acima são referências relativas à raiz do checkout; o pacote de governança
exclui o aplicativo. Consulte os [contratos](../architecture/contracts.md), o
[contexto arquitetural](../architecture/context.md) e as features `product-plugin-host`,
`product-agent-runtime`, `product-verification-engine`, `product-local-task-ui` e
`product-visual-workbench` no [índice SDD](../../sdd/features/README.md).

Esta atualização documenta fronteiras presentes por inspeção; não executa novos
ensaios adversariais nem renova aceitação histórica. Para demonstrar um controle,
delimite consumidor/SO e dados descartáveis, execute cenários normais e de recusa,
registre efeitos e versões observadas e confronte-os com o critério da feature.
Não usar mocks como prova de sandbox. Retenção/redação do bruto devem preservar
evidência autorizada sem expor segredos nas visões compactas.
