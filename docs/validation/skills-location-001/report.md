# Correção da localização das skills

Pedido explícito do mantenedor: mover o catálogo para `.codex/skills/` e atualizar referências. Rota local para mudança de endereço recuperável, sem alteração de competência ou permissão de execução; features existentes e evidências afetadas reexaminadas.

Baseline recuperável: before.tar.gz. Mapa de origem/destino e hashes: relocation.json. Todas as entradas e recursos técnicos conservaram os bytes; apenas o README do catálogo ajustou instrução de consulta. As 29 pontes, navegação, SDDs, scripts e testes usam o novo endereço. Não existe cópia ativa no endereço anterior.

Documentos originais, manifestos de revisões anteriores e respostas/logs históricos permanecem intactos. A correspondência entre seus caminhos antigos e os atuais é explícita no mapa; não foram renomeados hashes dentro de evidências antigas para simular reexecução. A revisão atual reexamina os resultados de conteúdo/comportamento anteriores contra os arquivos relocados, sem novo ensaio de agentes.

A revisão confirmou identidade dos bytes das 29 skills e recursos, preservação das declarações normativas e ausência de mudanças semânticas nos contratos. Os 22 critérios anteriormente aprovados conservam seu alcance por esta nova inspeção, apoiada pelos registros históricos arquivados e pelos checks atuais. Os 36 critérios técnicos antes NÃO VERIFICADO permanecem nesse estado. A relocação não é implementação de produto.

## Verificações observadas

`PYTHONDONTWRITEBYTECODE=1 python3 src/scripts/run-checks.py`: quatro comandos passaram; 8 testes passaram, incluindo cópia independente sob `.codex/skills/` e corrupção de recurso. Resultados em `docs/validation/runs/20261026T183739.024276Z/`. Um comando inicial de registro usou cwd incorreto e falhou antes de escrever; foi corrigido, sem ocultar falha de validação ou alterar critérios.

Nova checagem schema 2 será registrada em freshness.log depois de materializar a inspeção atual. Não foram repetidos ensaios de agentes nem integrações de produto.
