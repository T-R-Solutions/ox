# Tarefas: progresso no terminal

- [x] T001 [REQ-01, REQ-02, D-01, R-01]: ler contratos, inspecionar estado, definir escopo e métrica; responsável coordenador. Disposição documental: spec/plan registram decisões e limites atuais, sem aceite operacional.
- [x] T002 [REQ-01, REQ-02, REQ-03, REQ-04, REQ-05, REQ-06, D-01, D-02, D-03, D-04, R-01, R-02, R-03, R-04]: implementar apresentação e integração; dono implement nos caminhos de produção do plan; depende de T001. Concluir após cenários focados e disposição documental em scripts/README.md pelo coordenador.
- [x] T003 [AC-01, AC-02, AC-03, AC-04, AC-05, AC-06]: criar e executar fixtures controladas; dono tests em scripts/tests/test_terminal_progress.py, sem executar scanners completos. Depende do contrato T001 e integração T002. Registrar comandos, códigos, entradas e limites no relatório.
- [x] T004 [AC-01, AC-02, AC-03, AC-04, AC-05, AC-06]: revisão independente somente leitura após implementação; revisor com contexto próprio. Corrigir achados pela responsabilidade original, sem autorrevisão declarada independente.
- [x] T005 [AC-01, AC-02, AC-03, AC-04, AC-05, AC-06]: estabilizar entradas, verificar documentação e executar validação independente; coordenador integra evidência schema 2 e convergência. Relatório e documentação registram limitações e exemplos observados, não aprovação do produto.
- [x] T006 [REQ-06, AC-06, D-05, R-05]: revisar independentemente ocorrências Bandit reais do novo teste; coordenador integra somente ocorrências justificadas e hashes atuais no mecanismo estático existente, seguido de execução nativa focada e regressões de rejeição. Depende do freeze de T003; nenhum skip de regra ou severidade autorizado.

Documentação afetada: scripts/README.md, esta feature e
docs/validation/terminal-progress-20261115/report.md. Evidências históricas de
scripts-centralization e demais features relacionadas não recebem novos hashes
sem reexecução. Disposição e verificações finais serão registradas no relatório.

O projeto sdd/project.md foi revisado e preservado: a autorização desta mudança está
na feature, sem necessidade de alterar o conteúdo de autoridade autenticado.

Disposição final de T002/T003/T004/T006: scripts/README.md atualizado e conferido
com implementação; relatório registra 21 testes atuais + 49 regressões, lints
nativos e três defeitos corrigidos após revisão independente. review.json e
review-security.json preservam métodos e inputs; baseline recebeu somente as oito
ocorrências observadas/revisadas, com Bandit posterior exit 0. Nenhum documento
histórico foi revalidado trocando hashes. T005 recebeu parecer independente APPROVED para AC-01–06 e gate selecionado
--require-approved --require-fresh --check-convergence com exit 0. Este fechamento
administrativo recebe adendo independente e novo gate para os bytes finais; não
constitui execução completa de scanners ou aceitação do produto.

- [x] T007 [REQ-03, AC-03, D-02, R-02]: esclarecer mensagem de aceitação conforme pedido de 15/11, verificar fixtures e regressões atuais e submeter a revisão/validação independente. Disposição: scripts/README.md e relatório history-correction-20261115 explicam a frase; preservar envelope anterior e reobservar inputs afetados.

T007: 21 testes de terminal e 49 regressões passaram; revisão independente sem achados e validação semântica independente aprovou AC-01–06. Comandos, preimages e parecer em history-correction-20261115. O gate dos envelopes finais é registrado separadamente, sem alterar fatos históricos.
