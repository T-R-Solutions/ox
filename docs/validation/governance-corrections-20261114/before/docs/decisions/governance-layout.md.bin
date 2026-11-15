# ADR — Localização das ferramentas de governança

Estado: adotada em 2026-10-27 pelo pedido explícito do mantenedor de mover a
governança de src/ e atualizar seus consumidores. Aceitação na feature
`sdd/features/governance-layout/` e em suas observações vinculadas.

Decisão: reservar src/ para fontes futuras da aplicação. Mover src/scripts/ para
tools/governance/scripts/ e src/tests/ para tools/governance/tests/. De src/fixtures/,
perfil e cobertura normativa vão para config/governance/; prompts, casos de
avaliação e catálogo usado pelos ensaios vão para tools/governance/tests/fixtures/.
O catálogo ativo de skills permanece em .codex/skills/; selection-catalog.json é
input histórico de avaliação, não uma segunda configuração vigente.

Atualizar referências operacionais, raízes Python e rastreabilidade. A allowlist
do pacote substitui src/ por tools/governance/ e config/governance/; não inclui
outras ferramentas/configurações nem fontes de produto. O validador SDD original
permanece em sdd/tools/validate.py. Não há compatibilidade por aliases em src/.

Alternativas e riscos estão no plan da feature. A organização específica evita
misturar testes de governança com futuros testes do produto, sem decidir agora
se o Rust usará um crate ou workspace.

Histórico: ADRs anteriores, logs, manifests de execuções e revisões de proveniência
conservam os caminhos observados na época; esta ADR fornece o mapeamento vigente.
As decisões anteriores sobre permanência dos caminhos/allowlist são sucedidas
somente nesse ponto. O registro files.json ganha revisão, sem reescrever revisões
antigas. As comparações de preservação aceitam somente a tradução determinística
dos caminhos das rastreabilidades e o perfil idêntico no novo destino; continuam
rejeitando mudanças de requisitos, decisões, tarefas, skills e métodos SDD.

GOV-04 muda somente o destino de seu link; a cobertura normativa registra o novo
hash após revisão. Perfil, classes, revisão de perfil e POL-01..10 permanecem.
Observações antigas ficam na baseline; o archive distribui as 55 versões
alteradas/movidas, e recovery.json identifica os 384 inputs inalterados que
permanecem na distribuição com seus hashes. Essa deduplicação preserva os 439
inputs recuperáveis sem duplicar archives e exceder o orçamento de inspeção;
a cópia completa original permanece local em dist/, dispensável à recuperação.
Evidências correntes afetadas exigem
execução/inspeção nova. Não há implementação Rust, avaliação nova de modelos,
publicação, acesso externo ou mudança de permissões. Rever ao mudar o pipeline
de produto ou os contratos/pastas da governança.
