# Limpeza documental de scripts — 09/11/2026

Inspecionados os 45 arquivos de scripts/, o registro de checks, consumidores
por source/import/unittest, referências na governança e rastreabilidade SDD.
Rota local: documentação delimitada, recuperável, sem alterar runtime ou contratos
de execução. Aplicada workspace-integrity-engineering, entrada local consultada,
para inventário, preimagens, precondições de conteúdo e recuperação.

## Conteúdo retirado da árvore operacional

| Caminho | Conteúdo obsoleto retirado / justificativa | Fonte mantida |
| --- | --- | --- |
| scripts/security/SOURCES.md | Longo histórico de versões/estados anteriores, preparo nativo de bases migradas para Toolbox, locks/adapters substituídos. Não orientam o transporte exec atual. | Arquivo permanece como índice da referência atual, utilitários Cargo, regras e preimagem integral histórica. |
| scripts/README.md | Relatos de tarefas anteriores, inventário central vazio e revisão RustSec datada apresentados junto das instruções operacionais. | Configuração/CLI/limites e recuperação atuais; relatos originais integralmente nas preimagens. |
| scripts/security/NOTICE | Nomes reporting.py/validate-exceptions.py retirados em migrações anteriores. | Nomes shell atuais, mesma atribuição e licença. Nenhuma licença apagada ou reinterpretada. |
| scripts/security/rules/README.md | Orientação de executar Opengrep diretamente no host, superada pelo executor central. | Comando pelo wrapper público; regras, fixtures e limites mantidos. |

Não foi excluído arquivo funcional completo. O desuso comprovado estava nesses
trechos, não nos executáveis/configurações restantes. SOURCES.md é oracle de
AC-04 em scripts-security-quality/traceability.json: apagar seu caminho quebraria
um consumidor vigente. O índice mantido dá acesso aos bytes exatos da pesquisa
original. Referências de evidências anteriores não foram reescritas.

Preservados: módulos shell, wrappers, preparo RustSec, parsers/exceções e resumo
standalone, testes, fixtures, configurações vazias intencionais, regras e licenças.
Registry seleciona configs/regras por nome; support e unittest consomem auxiliares
indiretamente. O empacotador inclui scripts/ dinamicamente. Ausência de execução
ou de scanner instalado não fundamenta retirar seus recursos. Não surgiram caches
ou logs descartáveis adicionais nesta árvore. Nenhum log foi apagado.

## Inspeção e evidência

Métodos: leitura e rg nas fontes/contratos; inventário por bytes; comparação
com preimagens antes de editar e inspeção do conteúdo final. before/ e a cópia
local foram conferidos por SHA-256. Nenhum dos outros arquivos de scripts/ mudou.
Inventários, hashes e diff estão em scripts-before.json, inventory.json,
changes.json e changes.diff; operations.jsonl registra as ações e razões.

Critério de retirada dos trechos superados: APPROVED por inspeção documental e
comparação com o fluxo exec atual. Recuperabilidade por cópia: APPROVED para
existência/integridade, restauração não ensaiada. Aceite funcional: UNVERIFIED;
não foram executados verificadores, testes, automate.sh, scanners ou builds.
Sem commits/publicação. Não se declara auditoria semântica de todo o repositório.

As convergências scripts-security-quality e scripts-toolbox-native receberam
somente sucessores de inspeção. evidence.json e observações antigas permanecem
com seus bytes/hashes originais: inputs documentais modificados não renovam
aprovação nos cinco estados SDD. Nenhum resultado operacional foi produzido.

## Recuperação sem sobrescrever trabalho posterior

Bytes e metadados anteriores estão em
`.local/recovery/scripts-document-cleanup-20261109/before/`, com caminhos originais.
Essa área é excluída da limpeza e da distribuição. Uma cópia histórica adicional
está em before/ deste registro, com sufixo .bin, sem reinterpretar seu conteúdo
como guia vigente. inventory.json identifica hashes, modo e mtime originais.

Da raiz Ox, confira a reversão por contexto com
`git apply --reverse --check docs/validation/scripts-document-cleanup-20261109/changes.diff`.
Somente se aceita integralmente, aplique o mesmo comando sem --check. Se houver
conflito ou mudança posterior, compare a cópia antes/depois e reintegre apenas os
trechos desejados manualmente, sem reset, --reject ou substituição integral.
As cópias independem do histórico Git. Preserve o relatório/journal e registre
eventual restauração como nova observação; nenhuma restauração foi executada.
