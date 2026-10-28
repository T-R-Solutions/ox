# Registro do titular — 27/10/2026

Rota local, vinculada a maintenance-001 REQ-03/T005. Entrada autorizadora:
“a licença é GLP-3.0; Titular - Rodrigo Batista”. Mantida a identificação GNU
GPL-3.0-only já adotada, sem acrescentar versões posteriores. Nome registrado
no NOTICE como Copyright (C) 2026 Rodrigo Batista; ano consistente com os
registros de autoria do projeto em 2026. Não se alterou o texto de LICENSE.

Método observado: leitura das autoridades e ADRs; diff das oito alterações
textuais contra cópias prévias e SHA-256 de todos os arquivos existentes.
Resultado: somente NOTICE, README, análise de licença, três ADRs/pendências e
plan/tasks da manutenção mudaram antes da atualização dos envelopes.
A identidade do titular passa a ser informada, por declaração do mantenedor.
Direitos de terceiros, distribuição e demais itens OPEN-07 não foram aprovados.

Reexame dos critérios afetados: os envelopes anteriores vinculavam documentos
com a antiga pendência de titularidade. affected.json lista exatamente os inputs
alterados. Antes de atualizar as identidades atuais, comparei os bytes:
implementações Python, testes, perfil, skills, recursos, pontes, spec e
traceability permanecem idênticos. Plan/tasks mudam apenas o avanço de T005.
Assim, os resultados técnicos anteriores continuam observações históricas sobre
as mesmas implementações; não são alegados como novos testes nesta rodada.
As conclusões de preservação, autoria, fronteiras e método permanecem sustentadas
por essa comparação, sem novas funcionalidades ou alteração de critérios.
AC-03 da manutenção foi reexaminado: licença e titular são decisões do mantenedor;
a análise continua distinguindo contribuições próprias e materiais copiados.
AC-05 permanece NÃO VERIFICADO por falta dos termos dos materiais de terceiros.
Todos os critérios técnicos pendentes conservam seus estados.

Preservação: before.json identifica a árvore antes desta atualização; previous
contém os oito documentos e os envelopes substituídos, sem alterar observações
antigas ou seus hashes. Para recuperar, copiar a distribuição em pasta vazia,
repor somente previous/<path>.bin no path original e conferir before.json.
Não sobrescrever trabalho inesperado. As baselines anteriores seguem intactas.

Verificação desta rodada: logs separados para check-ox, validate --require-fresh,
verify-maintenance e cópia independente via export-clean/isolated-run. Os resultados
são registrados em results.json; a revisão semântica acima não equivale a testes
novos do produto ou a uma auditoria jurídica. Nenhum ZIP ou publicação é necessário.
