# Tarefas

- T001 concluída: inspecionar autoridades e chamadores; migrar wrapper/backend/registro e remover config/lock obsoletos.
- T002 concluída no contrato local: validar diagnósticos, relatórios, seleção, integridade e metadados; atualizar testes e guias.
- T003 pendente operacional: executar scanners reais após ativação central, API pública de idade e manutenção RustSec. Preflight real executado sem revisões ativas; zero scans.

- T004 concluída: confirmar recusa por SELinux com controle antes/depois; habilitar rótulos compartilhados no exec do Ox, preservar overrides e controles; executar testes reais, concorrência e regressões; manter aprovação operacional completa pendente.

- T020: Registrar sucessão, inventariar contratos/imagens/bases e preparar recuperação.
- T021: Implementar metadados públicos vinculados às bases e recusas por idade/integridade; testar contratos e execução real.
- T022: Atualizar RustSec oficialmente, verificar commit/data/integridade e consumidores offline.
- T023: Executar matriz isolada real de scanners/relatórios/bases/concorrência/cancelamento, conferir hashes e limpeza; qualificar e ativar revisões.
- T024: Executar comandos públicos e checks afetados, registrar evidências sucessoras por critério. Depende de T021..T023.

- T025 concluída por implementação/inspeção: confrontar README e guias consolidados da Toolbox com os consumidores Ox; remover seleção SELinux implícita, adaptar teste de contrato, orientar ambiente/CI, paths, volumes e resultados; preservar preimagens. Não executou verificadores, testes, scanners ou manutenção central. Aceite executado e T024 permanecem pendentes.

- T026 concluída no contrato local (29 testes aprovados, 1 opt-in ignorado): aplicar o guia obrigatório atual, remover argv local obsoleto de scanners centrais, exports ineficazes e branches inalcançáveis; corrigir o contrato OSV e preservar configs nativas usadas. Conferir planos, descoberta, códigos, relatórios, integridade e sintaxe com a suíte focada; registrar resultado e limites sem renovar aprovação operacional anterior.

- T027: Corrigir ambiente explícito SELinux/cache, chamadas de testes, sucessão
  documental e evidências obsoletas com preimagens; validar scanners reais e
  comando completo sem afrouxar política ou alterar Ec/Toolbox. Implementação e
  controles focados concluídos; execução integral e resultado final no relatório
  docs/validation/ox-operational-repair-20261109/report.md.
