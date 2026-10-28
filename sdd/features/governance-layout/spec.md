# Organização das ferramentas de governança

Ator: mantenedor do Ox. Pedido autorizado: retirar a governança de src/ e
atualizar referências e consumidores. Escopo: ferramentas Python, configuração,
fixtures, documentação, rastreabilidade, pacote e evidências afetadas.
Não implementa a aplicação nem altera o conteúdo das skills ou do núcleo SDD.

- REQ-01: Reservar src/ para fontes futuras da aplicação; ferramentas em tools/governance/scripts/, testes em tools/governance/tests/ e dados de avaliação em tests/fixtures/ dessa ferramenta.
- REQ-02: Separar configuração vigente (perfil e cobertura normativa) em config/governance/ e atualizar comandos, imports e referências operacionais.
- REQ-03: Distribuir somente a governança, incluindo seus novos caminhos e excluindo fontes do aplicativo e ferramentas/configurações alheias.
- REQ-04: Preservar observações históricas e substituir evidências ativas afetadas somente após novas execuções ou inspeções.
- AC-01 → REQ-01: src/ fica sem arquivos de governança; os 23 arquivos originais têm destino identificado, sem perda; fixtures e perfil mantêm conteúdo e a cobertura muda somente nas referências afetadas.
- AC-02 → REQ-02: Comandos documentados executam na raiz e em cópia independente; referências ativas e rastreabilidade resolvem para os novos locais; guards continuam rejeitando alterações indevidas.
- AC-03 → REQ-03: ZIP real inclui tools/governance/ e config/governance/, exclui src/, Cargo, crates e caminhos alheios; manifesto confere e cinco comandos passam na extração independente.
- AC-04 → REQ-04: Baseline recuperável, histórico anterior preservado, observações novas vinculadas aos inputs atuais e freshness válido; 36 cenários técnicos das skills continuam NÃO VERIFICADO.

Compatibilidade: os comandos Python mudam de caminho intencionalmente; não há
aliases em src/. Logs, archives e decisões históricas conservam caminhos da época.
O validador original permanece em sdd/tools/validate.py. Não se escolhe a futura
estrutura de crates, runtime, plataforma ou dependência do produto.
