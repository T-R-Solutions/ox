# Acervo visual da documentação

Este diretório contém as imagens incorporadas aos READMEs e guias, suas fontes
editáveis, o tema compartilhado e os avisos de terceiros. Os visuais explicam a
fundação existente; não representam interfaces futuras ou funcionalidades ausentes.

## Escolha uma explicação

| Figura | Pergunta | Fonte editável |
| --- | --- | --- |
| [Visão do produto](ox-overview.svg) | Quais são os três pilares da demonstração? | SVG vetorial próprio |
| [Arquitetura](architecture.svg) | Quem chama quem e quais processos acessam os arquivos? | [Modelo Mermaid](diagrams/architecture.mmd) e [composição vetorial](architecture-layout.mjs) |
| [Ciclo resumido](task-cycle.svg) | Como separar execução de aceitação? | [Fluxo](diagrams/task-cycle.mmd) |
| [Primeiro uso](first-run.svg) | Como executar e distinguir os possíveis resultados? | [Fluxograma](diagrams/first-run.mmd) |
| [Execução](execution.svg) | Em que ordem produtor e oráculo trabalham? | [Sequência](diagrams/execution.mmd) |
| [Runtime](runtime-states.svg) | Quando o supervisor realmente termina? | [Estados](diagrams/runtime-states.mmd) |
| [Plugin Host](plugin-protocol.svg) | Como handshake, grant e echo se relacionam? | [Protocolo](diagrams/plugin-protocol.mmd) |
| [Documentação](documentation.svg) | Qual guia responde à minha pergunta? | [Navegação](diagrams/documentation.mmd) |

Cada export SVG tem superfície branca opaca, título e descrição acessíveis. As
figuras permanecem com essa superfície em temas claros ou escuros. Os links
permitem abrir o arquivo integral; em telas estreitas, use essa ampliação e o texto
adjacente como alternativa. Não há dependência de CDN, icon font ou script para
exibir as imagens no Markdown.

## Capturas reais

| Arquivo | Origem | SHA-256 | Tratamento |
| --- | --- | --- | --- |
| [ox-approved.png](ox-approved.png) | Captura F0 de 2026-11-03 (corpus Linux x86_64/Wayland), resultado aprovado | `5b3c14acdf0bf4e1a174920bdd28c78f17eb26658109658d342ea75149253762` | Cópia exata, sem corte, anotação ou alteração de pixels |
| [ox-rejected.png](ox-rejected.png) | Captura F0 de 2026-11-03 (corpus Linux x86_64/Wayland), resultado rejeitado | `633848ef2e724fb362919c09c25d1978035532f0cd23491cf0d573caf26c532f` | Cópia exata, sem corte, anotação ou alteração de pixels |

Capturas de 03/11/2026, corpus Linux x86_64 / Wayland, janela lógica 900×700,
escala 100%, captura 1200×900. A barra de título identifica a sessão de validação.
São registros históricos da implementação, não uma nova execução ou teste de
usabilidade desta revisão.
Material próprio sujeito ao [LICENSE](../../LICENSE) e [NOTICE](../../NOTICE).

## Mermaid e compatibilidade

Os guias incorporam **SVGs já renderizados**. A arquitetura usa uma composição
vetorial de posições explícitas sobre o mesmo modelo, para evitar rótulos minúsculos;
o [export automático Mermaid](architecture-mermaid.svg) também é conservado. Também conservam fontes `.mmd` e,
quando não há dependência de ícones, blocos Mermaid recolhíveis. O renderer do
editor determina a aparência desses blocos nativos; os exports mantêm o tema
reproduzível em [mermaid.json](mermaid.json).

A extensão local VS Code `bierner.markdown-mermaid` 1.32.1 declara Mermaid
11.12.2, a mesma versão selecionada para os exports. Sua existência não prova o
comportamento de uma webview específica. A revisão usa Markdown local em Chromium,
sem alterar configurações do editor. Diagramas com ícones exigem o registro do
pack pelo exportador; não dependem de registro implícito no editor.

## Reprodução local

O aplicativo não depende destas ferramentas. Para reproduzir a renderização,
prepare um diretório separado, por exemplo `/tmp/ox-doc-visual-tools`, com este
[manifesto de ferramentas](tooling.json). A execução observada usou:

```bash
bun add --cwd /tmp/ox-doc-visual-tools mermaid@11.12.2 @iconify-json/lucide@1.2.74 playwright@1.56.1 markdown-it@14.1.0
PLAYWRIGHT_BROWSERS_PATH=/tmp/ox-doc-visual-tools/browsers node /tmp/ox-doc-visual-tools/node_modules/playwright/cli.js install chromium
node docs/assets/render.mjs
```

Execute o último comando na raiz do repositório. O renderizador usa apenas um
servidor efêmero em `127.0.0.1`, escreve SVGs em `docs/assets/` e observações em
`.local/docs-assets/`. `OX_DOC_TOOLS` permite outro
diretório de ferramentas; `OX_DOC_CHROMIUM` permite um executável de teste já
disponível. A ferramenta pode substituir os exports e capturas da revisão corrente;
preserve um registro anterior antes de gerar uma revisão histórica nova.
Instalação/download e lançamento do browser dependem das permissões do ambiente.

## Ícones, licença e manutenção

Ícones **Lucide**, pacote `@iconify-json/lucide` **1.2.74**: subconjunto de dez
ícones em [icons.json](vendor/lucide/icons.json), grid 24, stroke 2, sem mistura de
famílias. Cada ícone de papel tem rótulo visível. O pacote identifica licença ISC;
o [aviso completo](vendor/lucide/LICENSE) conserva também a licença MIT das partes
derivadas de Feather. Aviso obtido do pacote local `lucide@0.548.0`; a identidade
dos ícones usados é a do subconjunto Iconify, não uma alegação de igualdade com
essa outra distribuição. [Metadados de origem](vendor/lucide/info.json).

Diagrama, modelo, captura, tema, fonte ou versão do renderer alterados exigem nova
renderização e inspeção. Responsáveis: contribuinte da mudança e mantenedor Ox.
A revisão de 2026-11-04 separou parsing, export e inspeção visual; a prévia local usou
Chromium 141.0.7390.37 a 360/768/1280 px CSS, claro/escuro, sem webview real do VS Code.
