# Fundação do produto Ox — transição de fase

Ator: mantenedor e agentes autorizados. Pedido: examinar e implementar o plano
de transição v1.0, corrigindo sua integração com SDD quando necessário.
Escopo desta feature: contrato de desenvolvimento, biblioteca integrada ao SDD,
verificadores e distribuição da governança. Não entrega crates ou aplicativo.

- REQ-01: Registrar fase e escopo na autoridade de contexto, preservando permissões efetivas.
- REQ-02: Manter AGENTS como entrada e integrar competências ao SDD sem duplicar políticas nas skills.
- REQ-03: Separar aceitação de produto, autoria de skills e observações históricas.
- REQ-04: Identificar e qualificar a distribuição exclusivamente como governança.
- REQ-05: Preservar baseline recuperável e reexaminar evidências dependentes dos inputs alterados.
- AC-01 → REQ-01: Contexto registra implementation-foundation e not-yet-implemented; autoridades permitem desenvolvimento delimitado e não concedem execução irrestrita.
- AC-02 → REQ-02: AGENTS remete às autoridades; guia de integração distingue seleção, consulta e uso, rota local/completa e contribuição das pontes; 29 skills, 29 pontes e SDD 1.3.0 permanecem íntegros.
- AC-03 → REQ-03: Critérios de product-foundation são próprios; os 36 cenários técnicos de skill permanecem NÃO VERIFICADO e mutações que os promovam são rejeitadas.
- AC-04 → REQ-04: ZIP ox-governance.zip e recibos declaram governança sem produto; manifesto exclui Cargo/crates e extração independente passa os cinco comandos de qualificação.
- AC-05 → REQ-05: Checks e testes adversariais passam; histórico imutável e baseline mantêm bytes; observações afetadas são arquivadas e substituídas por reexame/execução novos com schema 2 e inputs atuais.

Rejeitar: aprovação de aplicativo por documentação, atualização de hashes para
reciclar resultados antigos, alteração de POL-01..10, instalação/publicação por
menção no roadmap. A rota local continua disponível conforme sdd/workflow.md.
Os gates textuais detectam regressões representativas, sem provar semântica de
qualquer paráfrase. Aceitação desta feature é exclusivamente da transição.
