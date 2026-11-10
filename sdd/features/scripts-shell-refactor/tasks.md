# Tarefas

- T001: Concluída. Contratos e consumidores inventariados; bytes e hashes iniciais preservados. inventory/migration e preimagens em docs/validation/scripts-shell-refactor/.
- T002: Concluída. Dez scripts .sh dividem coordenação, execução, registro, arquivos, relatórios e scanners; wrappers repetidos removidos. Depende de T001.
- T003: Concluída. Consumidores, documentação, testes, sucessão autenticada e evidências afetadas migrados; alterações preexistentes preservadas. Depende de T002.
- T004: Implementação e regressões disponíveis verificadas: 89 testes rápidos, 20 de integração, sintaxe, ShellCheck, Gitleaks e cinco etapas Rust. A validação integral de segurança/qualidade continua pendente de sete ferramentas externas e seus pré-requisitos; AC-04 INCONCLUSIVE. Depende de T003.
