# Governança independente — revisão 1

Ator: mantenedor e agentes autorizados. Autorização: pedido de aplicar
Ox_Correcoes_Governanca_Independente_v1.1.md. Escopo: governança, biblioteca,
verificadores e distribuição local. Não implementar nem publicar o produto.

- REQ-01: Não exigir nem distribuir os três estudos externos, inclusive em recuperação.
- REQ-02: Manter autoridades locais, catálogo versionado e contratos SDD 1.3.0 íntegros.
- REQ-03: Preservar observações antigas sem reutilizar aprovação de inputs obsoletos.
- REQ-04: Entregar pacote novo com inspeção e execução em extração independente.
- AC-01 → REQ-01: Cópia independente executa verificadores Ox e SDD sem estudos ou biblioteca de origem.
- AC-02 → REQ-01: Inspeção recursiva rejeita nomes e conteúdo integral dos estudos em arquivos e archives, inclusive renomeados.
- AC-03 → REQ-02: Cobertura aponta para IDs de autoridades locais existentes; links e catálogo/perfil concordam.
- AC-04 → REQ-02: Testes rejeitam corrupção de skill, ponte, autoridade, evidência e link; restauração recupera sucesso.
- AC-05 → REQ-03: Observações anteriores preservadas com hashes originais; evidências afetadas substituídas por observações novas ou estado não decidido.
- AC-06 → REQ-03: Os 36 cenários técnicos das nove skills permanecem NÃO VERIFICADO.
- AC-07 → REQ-04: ZIP novo contém inventário verificável, passa inspeção recursiva e os cinco comandos oficiais na extração limpa.

Rejeitar: reintrodução de originais; aprovação por mera contagem de arquivos;
promoção de proposta técnica; alteração retrospectiva de evidência; aprovação
global das skills como implementação. Licença/plataforma do produto continuam
pendentes em docs/decisions/open-questions.md.
