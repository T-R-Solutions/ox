# Convergência — product-bootstrap

28/10/2026. Linux x86_64, Rust/Cargo stable observados 1.99.1; Iced 0.14.0,
tiny-skia e X11 em sessão XWayland. Os 16 crates compilam a partir de application.
Toolchain stable conforme pedido do mantenedor. Fonte e evidências identificadas
por SHA-256 em evidence.json, incluindo contratos e oráculos da feature.

| Critério | Requisito / decisão / risco / tarefas | Alteração | Evidência | Estado |
|---|---|---|---|---|
| AC-01 | REQ-01 / D-01 / R-01 / T001–T005 | `application/Cargo.toml` | E-STRUCTURE-LAYOUT, E-CHECK-LAYOUT | APROVADO |
| AC-02 | REQ-02 / D-01 / R-01 / T001–T005 | `application/crates/ox-ui/src/desktop.rs` | E-GUI-LAYOUT, E-REVIEW-LAYOUT | APROVADO |
| AC-03 | REQ-03 / D-01 / R-01 / T001–T005 | `application/crates/ox-app/src/main.rs` | E-REVIEW-LAYOUT, E-TEST-LAYOUT | APROVADO |
| AC-04 | REQ-04 / D-01 / R-01 / T001–T005 | `application/crates/ox-core/src/lib.rs` | E-STRUCTURE-LAYOUT, E-DEPS-LAYOUT | APROVADO |
| AC-05 | REQ-05 / D-01 / R-01 / T001–T005 | `application/crates/ox-ui/src/lib.rs` | E-STRUCTURE-LAYOUT | APROVADO |
| AC-06 | REQ-06 / D-01 / R-01 / T001–T005 | `application/crates/ox-task/src/state.rs` | E-TEST-LAYOUT, E-DISCOVERY-LAYOUT, E-GUI-LAYOUT | APROVADO |
| AC-07 | REQ-07 / D-01 / R-01 / T001–T005 | `application/Cargo.toml` | E-STRUCTURE-LAYOUT, E-CHECK-LAYOUT, E-REVIEW-LAYOUT | APROVADO |
| AC-08 | REQ-08 / D-01 / R-01 / T001–T005 | `application/crates/ox-workspace/src/root.rs` | E-REVIEW-LAYOUT, E-TEST-LAYOUT | APROVADO |
| AC-09 | REQ-09 / D-01 / R-01 / T001–T005 | `sdd/features/product-bootstrap/plan.md` | E-SDD-LAYOUT, E-REVIEW-LAYOUT | APROVADO |
| AC-10 | REQ-10 / D-01 / R-01 / T001–T005 | `tools/governance/scripts/check-ox.py` | E-GOV-LAYOUT | APROVADO |
| AC-11 | REQ-11 / D-01 / R-01 / T001–T005 | `application/crates/ox-plugin/src/protocol.rs` | E-REVIEW-LAYOUT, E-TEST-LAYOUT | APROVADO |
| AC-12 | REQ-12 / D-01 / R-01 / T001–T005 | `tools/governance/scripts/governance_support.py` | E-GOV-LAYOUT, E-REVIEW-LAYOUT | APROVADO |
| AC-13 | REQ-13 / D-01 / R-01 / T001–T005 | `application/crates/ox-agent/src/session.rs` | E-REVIEW-LAYOUT, E-CHECK-LAYOUT, E-GUI-LAYOUT | APROVADO |

9 testes Cargo descobertos: 7 comuns passaram; 2 gráficos são ignorados na suíte
comum e passaram na execução explícita. Sem duplicação entre unitários e integrações.
Teste de inicialização sem display rejeita sucesso e exige diagnóstico em filho limitado.
Check, fmt e Clippy com -D warnings passaram. Governança: 23 testes e os três checks
passaram, incluindo exportação independente; recuperação preserva os 439 inputs históricos.

Janela real: Mostrar detalhes → Ocultar detalhes, pixels e título alterados;
reversão observada. Sair e fechamento nativo retornaram zero. Capturas em
`docs/validation/product-bootstrap/collapsed.png` e `expanded.png`.
Tentativas anteriores com timeout, erro de configuração de executor e erro de tipo
do título estão preservadas nos logs. O harness gráfico passou após usar foco
explícito e espaçar press/release; nenhum critério foi reduzido para encobrir as falhas.

Limitações: Wayland nativo, outras plataformas, acessibilidade e operação sob carga
não exercitados. Unsafe transitivo identificado separadamente; nenhuma auditoria
integral ou autorização de distribuição. UUID não foi introduzido porque nenhuma
entidade persistente global existe. IPC, agentes, armazenamento e motores são futuros.

Esta entrega conclui o bootstrap delimitado, não toda a F0. Próxima fatia: especificar
handshake/transportes, autorização e falhas do host de plugins antes de executar IPC.
As aprovações históricas foram conservadas em bytes; evidências correntes dependentes
das autoridades alteradas foram invalidadas seletivamente (invalidation.json), sem
transferir a aprovação destes testes para aquelas features.

Reproduzir: comandos Cargo no README e em evidence.json; teste gráfico requer sessão
X11 e pode mover temporariamente o ponteiro. Ao retomar, executar validador com
--require-fresh; não exigir aprovação global das features históricas/skills pendentes.

## Ajuste local — diretórios vazios

Após observação do mantenedor, removidos application/src e application/tests,
ambos preexistentes e vazios (listagem observada; rmdir concluído). O manifesto
virtual mantém fontes e testes nos crates. Verificação: ambos os caminhos ausentes;
nenhum arquivo ou input de compilação alterado, sem necessidade de repetir Cargo.

## Revisão local — referências de layout

Pedido do mantenedor: varrer arquivos fora de application/. Inventário: 849 arquivos,
818 textos UTF-8 e 31 binários; 25 archives com membros imediatos catalogados.
Metadados .git/.aws/.agents, symlinks e caches Python não integram o conteúdo auditado.
Correspondências em 212 arquivos; 7 arquivos ativos corrigidos (changes.json).
README, contexto, índice de features, arquitetura, compartilhamento e licenciamento
agora apontam para application/crates; fixtures testam a exclusão da estrutura atual.
Históricos e exemplos genéricos conservados, sem alterar suas decisões ou hashes.
Binários catalogados por hash, sem alegar leitura semântica de seu conteúdo.

Método, arquivos/linhas e hashes: docs/validation/product-bootstrap/layout-audit/
(inventory-before.json, matches-before.json, changes.json, report.json).
Cópias anteriores e envelope de evidências preservados nesse registro.
Observações Rust/gráficas reexaminadas: inputs de implementação e testes de produto
inalterados; execuções anteriores não foram repetidas nem apresentadas como novas.
Observações de governança reexecutadas: 23 testes passaram e checks deram exit 0.
Recuperação: 439/439 inputs históricos íntegros. Nenhuma mudança em application/.
