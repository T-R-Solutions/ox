# Recuperar as exclusões de 09/11/2026

Os bytes anteriores estão em `.local/recovery/repository-cleanup-20261109/before/`,
mantendo os caminhos originais. O recovery-manifest.json local registra SHA-256,
tamanho, modo, proprietário/grupo e tempos observados. Copy2 preservou modo,
mtime e atributos estendidos suportados pelo filesystem; os metadados essenciais
também estão no manifesto. Os 42 arquivos possuem preimagens: 35 exclusões e sete
edições. Essa área está expressamente excluída da limpeza. Não extraia/copíe a
árvore before inteira sobre o checkout e não use reset/checkout para recuperação.

## Restaurar caches removidos

Feche processos que estejam escrevendo nesses diretórios. Na raiz original do Ox:

```bash
cd /home/rodrigo/Projetos/ox
python3 .local/recovery/repository-cleanup-20261109/restore.py
```

Para selecionar apenas um caminho, use por exemplo:

```bash
python3 .local/recovery/repository-cleanup-20261109/restore.py --path scripts/tests/__pycache__/support.cpython-313.pyc
```

O utilitário só aceita a lista de exclusões. Confere a preimagem e a fonte .py;
se a fonte mudou depois da limpeza, deixa o cache ausente. Recusa links e
travessia, e usa criação exclusiva O_EXCL/O_NOFOLLOW: nunca substitui um destino
existente, inclusive um cache regenerado. Reaplica modo/tempos e não altera
proprietário, fontes, logs ou dados operacionais. Não foi executado nesta tarefa;
houve inspeção do código e conferência dos bytes recuperáveis, sem ensaio de
restauração. Sem escritor concorrente hostil no momento da operação: mudanças
adversariais de diretórios entre inspeção e abertura não estão isoladas pelo SO.
Uma falha de escrita pode deixar um arquivo parcial criado exclusivamente;
preserve-o e examine-o antes de tentar novamente, pois a próxima chamada o pula.

## Reverter os blocos de código e a documentação

reviewed-changes.diff contém somente as sete edições desta tarefa, derivadas das
preimagens do checkout já modificado. Não representa a diferença para HEAD.
Para reverter esses trechos com aplicação por contexto, sem usar o índice Git:

```bash
git apply --reverse --check .local/recovery/repository-cleanup-20261109/reviewed-changes.diff
git apply --reverse .local/recovery/repository-cleanup-20261109/reviewed-changes.diff
```

Execute a segunda linha somente se a primeira aceitar integralmente a aplicação.
Não use --reject, --3way ou opções que forcem aplicação. Alterações posteriores
nos mesmos trechos podem impedir o patch: nesse caso, preserve a versão atual e
reintroduza somente as linhas desejadas por comparação com before. Alterações
fora dos trechos do patch devem permanecer. Os comandos são instruções futuras;
não foram executados aqui. Não são necessários para recuperar os caches.

Também é possível comparar diretamente, sem depender do histórico Git:

```bash
diff -u .local/recovery/repository-cleanup-20261109/before/scripts/checks/run.sh scripts/checks/run.sh
```

Repita por caminho de recovery-manifest.json para reinserção manual em caso de
conflito. A preimagem completa permite reconstruir os bytes removidos mesmo sem
Git. Não substitua arquivos inteiros se houver trabalho posterior. As identidades
após a limpeza estão em inspection.json para distinguir nossas edições de outras.
Mantenha o journal, o relatório e as cópias como histórico mesmo ao desfazer a
limpeza; acrescente a data e o resultado da restauração em um registro novo.
