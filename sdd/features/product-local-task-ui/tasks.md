# Tarefas: product-local-task-ui

- [x] T001 [D-01..06, R-01..06]: concluir inspeção e revisão dos contratos e decisões.
- [x] T002 [D-01, R-01]: consolidar os quatro critérios de governança antes do código.
- [x] T003 [D-01..05, R-01..05]: implementar resultado vinculado à tentativa, oráculo independente e interface supervisionada.
- [x] T004 [D-06, R-06]: executar testes de domínio/processos, Cargo e interação gráfica real.
- [x] T005 [D-06, R-06]: preservar evidências anteriores, registrar inputs atuais e aceitação por critério.


- [x] T901 [D-ROBUST, R-ROBUST]: preservar inputs, reproduzir FIFO e modelo de erros do filho; corrigir captura/limpeza e testar processos reais e falhas simuladas.
- [x] T902 [D-ROBUST, R-ROBUST]: executar checks pertinentes e registrar evidências antes/depois e limites em robustness-20261105.
- [x] T903 [D-ROBUST, R-ROBUST]: observar UI X11/Wayland, cancelamento/fechamento e desempenho/F0 nos novos inputs; não reutilizar aprovação histórica como observação atual.


T903 executada parcialmente; permanece aberta. Sucessor: docs/validation/t903-20261105/report.md. Jornadas X11/Wayland, FIFO, worker/processos, matriz de12 e desenho de32 observações observados; falta oráculo adotado de RSS para histórico gráfico cheio (até133,69 MiB). Não ampliar64 MiB nem transferir automaticamente256 MiB do corpus de memória separado. Retomar pela disposição explícita da aplicabilidade; se64 MiB abranger esse corpus, tratar como REJECTED e corrigir/revalidar, sem relaxamento. Sem persistência/commit.


Sucessor de encerramento T903: docs/validation/t903-memory-20261105/report.md. O registro anterior de pendência é histórico. Correção de compartilhamento imutável e captura por blocos preserva orçamento lógico; matriz12 com32 observações, jornadas/FIFO/worker/processos e corpora separados reobservados. Critérios e checks atuais sustentam encerramento no envelope adotado; sem expansão/persistência/commit.

- [x] T904 [AC-05]: reobserve the current native criterion with the maintained harness, bind the new build and independently inspected captures, and preserve all historical results. This does not close the feature or R3 as a whole.
