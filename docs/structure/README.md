# Proveniência e sucessão de arquivos

[`files.json`](files.json) é um ledger histórico de cópia, adaptação e sucessão,
com identidades de conteúdo observadas. Não descreve a árvore atual do Ox.
O campo `source_namespace` identifica caminhos relativos à biblioteca de origem;
ausência desses caminhos no checkout não os torna dependências de execução.

Cada revisão conserva seus IDs, origens, destinos e hashes. Registros posteriores
podem estar nos `revision.json` de `docs/validation/`, com consumidores explícitos
em `tools/governance/scripts/`. Consulte a decisão e o checker de cada revisão
antes de interpretar uma cadeia; não há promessa de que este ledger centralize
todos os sucessores. Não atualize hashes históricos para representar bytes atuais.

Para código e diretórios atuais, consulte o [contexto arquitetural](../architecture/context.md),
o guia `application/README.md` (checkout completo; excluído da exportação de governança) e o
[índice de features](../../sdd/features/README.md). Esta explicação não altera o
ledger nem executa sua cadeia de verificação.
