# Plano: product-bootstrap

Autoridades lidas: AGENTS, constituição, workflow/evidence, contexto, ADRs de transição/layout/open-questions. Rota completa. Sem Git operacional; arquivos existentes preservados por comparação de bytes.

D-01 / R-01: todos REQ-01 a REQ-13 usam workspace explícito, contratos pequenos e validação proporcional. Risco: skeleton confundido com operação. Oráculos Cargo, inspeção de contratos e execução gráfica separada. Rever ao implementar capacidades.
D-02: Iced 0.14.0, edição 2024, toolchain stable por instrução explícita do mantenedor (observada 1.99.1); MSRV conservador 1.99 (piso deliberado desta primeira entrega, não alegação de mínimo técnico). Tiny-skia + X11 + Wayland + fira-sans + thread-pool (exigido pela compilação do Iced), sem Tokio ou runtime adicional. Confirmar resolução/build. Alternativa wgpu adiada por não haver GPU necessária nesta janela.
D-03: sem entidades persistentes na F0; não introduzir UUID ou serde sem consumidor. Plugin usa nome e versão; transporte IPC permanece não selecionado.
D-04: detalhes expansíveis da fundação são interação de UI real; não simulam execução de agentes. Sair retorna tarefa iced::exit, fechamento nativo usa comportamento padrão.
R-02: mantenedor confirmou Linux x86_64 inicialmente. Windows/macOS não são suportados nesta fatia. Execução gráfica continua exigindo observação independente.

## Skills consultadas e utilizadas
Primária .codex/skills/rust/SKILL.md: ownership, manifests, APIs públicas e descoberta de testes. Auxiliar .codex/skills/iced-engineering/SKILL.md: Message/update/view e efeito de encerramento. Pontes sdd/chain/rust.md e sdd/chain/iced-engineering.md, bridge_version 1. Identidades SHA-256 no arquivo skills.json desta feature (entradas sem versão semântica). Contribuição: estado puro, módulos externos, efeitos fora de view e distinção de teste de estado versus janela. Nenhuma delegação.

## Execução
T001 especificar; T002 workspace/contratos; T003 GUI; T004 validar; T005 evidências. Testar toggle repetido, política sem grant, plugin incompatível, bytes brutos e falhas. Não criar processos, banco, IPC ou executor fictício. Logs em docs/validation/product-bootstrap. Nenhuma mudança de distribuição pública.

## Resultado das decisões
Linux x86_64, stable e configuração descrita na ADR product-bootstrap. X11/XWayland exercitado; Wayland nativo só compilado. Teste gráfico usa x11rb 0.13.2 com xtest apenas como dev-dependency; não é IPC de produto. O harness restaura a posição do ponteiro após cliques e encerra seus próprios filhos no cleanup. Captura somente a própria janela.
Dependências: Iced declara MIT e rust-version 1.88; piso próprio 1.99 é conservador, não uma inferência de mínimo técnico. Inventário Linux em dependency-review.json; winit/softbuffer e bibliotecas de plataforma possuem unsafe/FFI. Revisão limitada a manifestos e varredura, sem afirmar auditoria integral ou autorização de distribuição.
A mudança de autoridades invalida observações históricas E-HOLDER-REVIEW. Bytes e aprovações anteriores preservados em docs/validation/bootstrap-governance/previous; invalidation.json registra exatamente os critérios pendentes. Os testes atuais não promovem automaticamente esses critérios.
