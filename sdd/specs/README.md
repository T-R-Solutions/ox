# Specs vivas

Uma spec por capacidade duradoura do produto, no formato de [../templates/spec.md](../templates/spec.md).
A task que altera uma capacidade atualiza a spec e cita a task na tabela **Estado atual**.

| Spec | Capacidade |
|---|---|
| [agent-runtime](agent-runtime.md) | Runtime local de agentes (adaptador controlado, cancelamento, prazos) |
| [bootstrap](bootstrap.md) | Bootstrap do workspace Rust e janela inicial |
| [f0-gate](f0-gate.md) | Fronteira e fechamento da fatia F0 |
| [foundation](foundation.md) | Fundação do produto e transição de fase |
| [ide-shell](ide-shell.md) | Casca de IDE desktop (menus, abas, dock) |
| [local-persistence](local-persistence.md) | Histórico local durável de tasks (proposta, UNVERIFIED) |
| [local-task-ui](local-task-ui.md) | Interface local de tasks |
| [plugin-host](plugin-host.md) | Host de plugins |
| [verification-engine](verification-engine.md) | Motor de verificação |
| [visual-workbench](visual-workbench.md) | Bancada visual nativa e superfícies |

As specs migradas em 2026-11-23 marcam os ACs como `(herdado)`: o estado vem do modelo anterior
e a evidência bruta não existe mais. Reavaliar exige reescrever o AC com método e esperado.
