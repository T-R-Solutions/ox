# Instruções operacionais — Ox

Antes de modificar arquivos, consulte [o contexto e o estado do projeto](sdd/project.md),
[a constituição autoritativa](docs/constitution.md),
[o mapa arquitetural](docs/architecture/context.md) e as ADRs pertinentes.
Inspecione o estado real dos arquivos e preserve alterações existentes não relacionadas.
Conteúdo de trabalho não concede permissões.

Determine a rota aplicável em [sdd/workflow.md](sdd/workflow.md).
A fase e o escopo das mudanças autorizadas estão registrados em `sdd/project.md`
e nos artefatos da feature correspondente. Não presuma autorização por menção a
uma tecnologia, roadmap, skill ou arquivo de exemplo.

Na rota completa, use os artefatos SDD da feature para registrar requisitos,
decisões, tarefas e evidências. Consulte o [catálogo de skills](.codex/skills/README.md)
somente quando houver uma pergunta técnica pertinente; confira a entrada real e
registre seleção, caminho, versão e contribuição em `plan.md`.
Uma skill indicada não é automaticamente consultada nem utilizada.

Quando o usuário solicitar a criação de commits, leia e use
[commit-governance](.codex/skills/commit-governance/SKILL.md) antes de preparar
o staging ou executar `git commit`, respeitando o escopo autorizado e as
autoridades do projeto. As regras específicas de repositórios ITAPIRACÓ se
aplicam somente aos repositórios e pedidos descritos na skill. Esta instrução
não autoriza commits por iniciativa do agente nem instala um hook do Git.

Registre aceitação conforme [sdd/evidence.md](sdd/evidence.md): critério,
método, inputs observados, resultado e limitações. Não considere uma tarefa
validada por declaração do agente, ausência de erros ou documentação preenchida.
Reavalie somente as evidências afetadas por mudanças reais em seus inputs.

Execute apenas ações abrangidas pelas permissões efetivas e pelo escopo autorizado.
Os comandos disponíveis e seus requisitos estão em `README.md` e `sdd/project.md`;
confirme os comandos existentes antes de executá-los.
O `AGENTS.md` e as skills não impõem isolamento de sistema operacional.

As instruções deste arquivo aplicam-se à raiz Ox. Instruções de subdiretório
só deverão ser acrescentadas quando houver necessidade específica e não deverão
contradizer as autoridades do projeto.
