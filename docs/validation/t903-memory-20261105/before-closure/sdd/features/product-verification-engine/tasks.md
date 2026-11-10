# Tarefas: product-verification-engine

- [x] T001 [D-01, R-01]: delimitar requisitos e decisões antes do código.
- [x] T002 [D-01, R-01]: implementar a fatia local delimitada.
- [x] T003 [D-01, R-01]: executar cenários positivos e negativos com oráculos externos ao resultado.
- [x] T004 [D-01, R-01]: registrar inputs, resultados e limitações; consolidar aceitação antes da próxima etapa.


- [x] T901 [D-ROBUST, R-ROBUST]: preservar inputs, reproduzir FIFO e modelo de erros do filho; corrigir captura/limpeza e testar processos reais e falhas simuladas.
- [x] T902 [D-ROBUST, R-ROBUST]: executar checks pertinentes e registrar evidências antes/depois e limites em robustness-20261105.
- [ ] T903 [D-ROBUST, R-ROBUST]: observar UI X11/Wayland, cancelamento/fechamento e desempenho/F0 nos novos inputs; não reutilizar aprovação histórica como observação atual.


T903 executada parcialmente; permanece aberta. Sucessor: docs/validation/t903-20261105/report.md. Jornadas X11/Wayland, FIFO, worker/processos, matriz de12 e desenho de32 observações observados; falta oráculo adotado de RSS para histórico gráfico cheio (até133,69 MiB). Não ampliar64 MiB nem transferir automaticamente256 MiB do corpus de memória separado. Retomar pela disposição explícita da aplicabilidade; se64 MiB abranger esse corpus, tratar como REJECTED e corrigir/revalidar, sem relaxamento. Sem persistência/commit.
