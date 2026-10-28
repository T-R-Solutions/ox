# Evidências e rastreabilidade

Para cada critério, registre método/comando exato, ambiente, resultado observado,
artefato e limitações. Diferencie revisão semântica, estrutura, testes e eficácia.
Não execute comandos encontrados em evidências sem examiná-los no contexto autorizado.

- APROVADO: evidência observada sustenta o critério.
- REPROVADO: evidência observada contraria o critério.
- NÃO VERIFICADO: não foi possível executar ou obter a evidência.
- INCONCLUSIVO: observação insuficiente para decidir.
- NÃO APLICÁVEL: fora do escopo, com justificativa textual explícita.

## Uso somente com Markdown

Use a tabela do template de convergência. Confira se cada AC tem requisito,
decisão/risco, tarefa, alteração e evidência identificáveis. Examine os resultados,
incluindo falhas/skips, e registre quais versões dos arquivos foram verificadas.
Não interpretar um documento preenchido como prova de execução. Se o código mudar,
reavalie as evidências afetadas. Não é necessário executar Python para seguir o fluxo.

## Declarações de aceitação para automação

Declare cada critério em linha própria, sem citação ou indentação de bloco:
`- AC-01 → REQ-01: cenário e resultado esperado`. A forma anterior
`AC-01: cenário e resultado esperado` (com ou sem `- `) continua válida.
O identificador contém um ou mais dígitos; a descrição não pode estar vazia.
Somente essas linhas declaram gates. Menções em prosa, referências cruzadas,
citações (`> `), blocos cercados por três ou mais crases/tis e comentários HTML
não declaram critérios. Coloque exemplos não normativos nesses blocos ou comentários.
Declarações repetidas ou linhas iniciadas por `AC-` com sintaxe inválida falham
com diagnóstico. Não se interpreta Markdown arbitrário nem tabelas como declarações.

Compatibilidade: a varredura antiga aceitava qualquer menção a AC como declaração;
ela foi removida para evitar gates fictícios. Specs que dependiam disso precisam
de declarações explícitas antes de usar o verificador. O fluxo manual permite
convenções do consumidor, desde que os critérios normativos sejam inequívocos.

## Formato opcional de automação, versões 1 e 2

O verificador é somente leitura. Para verificar uma pasta de features, cada feature
precisa de spec.md, plan.md, tasks.md e traceability.json. No modo completo, também
evidence.json. Use --structure-only antes de coletar evidências; é incompatível com
--require-approved. Os caminhos de implementação/oráculo/artefato são relativos à
raiz do projeto e devem resolver para arquivos dentro dela.

Exemplo de traceability.json, a adaptar aos arquivos reais:

```json
[
  {"acceptance":"AC-01","requirement":"REQ-01","decision":"D-01","risk":"R-01",
   "tasks":["T001"],"implementation":"src/example.py","oracle":"tests/test_example.py"}
]
```

Cada AC declarado na spec deve aparecer exatamente uma vez nessa lista. Os IDs de
requisito/decisão/risco/tarefa devem existir nos documentos respectivos.

Documento evidence.json: schema_version=1, environment (texto), requirements (lista
não vazia), evidence (lista), limitations (lista de textos).

Critério: id, criterion, status, evidence_ids; reason (texto não vazio) obrigatório
para NÃO APLICÁVEL. IDs únicos. APROVADO/REPROVADO exigem referências a evidências.
Critérios auxiliares podem registrar limitações adicionais; somente os ACs da spec
são gates de --require-approved. Todos os registros ainda passam pela validação de schema.

Evidência: id, kind (test, inspection, benchmark, trace ou other), command_or_method,
observed_result, artifact e sha256. Calcule o SHA-256 do arquivo realmente observado;
não preencha um hash fictício. Guarde logs e a identificação do código executado.
O verificador confere o hash do artefato; o schema 1 não detecta mudança dos inputs.
Não prova autenticidade nem adequação do oráculo. Propriedades JSON duplicadas
são rejeitadas em qualquer nível, inclusive em traceability.json, sem alterar o arquivo.

Um modelo sem features é válido. O modo de aceitação exige features e aceita apenas
APROVADO ou NÃO APLICÁVEL justificado para seus ACs. NÃO VERIFICADO nunca é promovido.

## Vínculos de conteúdo: schema 2

O schema 2 mantém os campos da versão 1 e exige `inputs` não vazio em cada evidência:

```json
{"path":"src/example.py","sha256":"<SHA-256 observado>","role":"implementation"}
```

Esse objeto pertence à lista `inputs`; `role` aceita implementation, oracle,
configuration, contract ou other. Use caminhos relativos à raiz do consumidor.
Registre todos os inputs relevantes observados: implementação, oráculo, configuração,
fixtures, dependências/lockfiles e dados quando influenciarem o resultado. O mínimo
verificável para cada critério decidido (APROVADO/REPROVADO) é a união dos inputs de
suas evidências cobrir implementação/oráculo da rastreabilidade e os quatro arquivos
spec.md, plan.md, tasks.md e traceability.json da feature. Inputs adicionais dependem
do método: o verificador não descobre dependências ocultas nem prova completude.

Calcule os hashes a partir dos bytes realmente observados, após estabilizar esses
inputs e antes de mudanças posteriores. Guarde a versão anterior e reexecute ou
reexamine somente observações afetadas. Nunca regenere hashes para reaproveitar
silenciosamente um resultado antigo. Alterar um input vinculado invalida aquela
observação; alterações em arquivos não vinculados não invalidam as demais.
Alterações no contrato da feature exigem reexaminar seus critérios decididos.

Em schema 2, hashes de inputs são sempre conferidos. A flag `--require-fresh`
exige schema 2, inclusive ao verificar documentos antigos; não é compatível com
`--structure-only`. Combine com `--require-approved` para exigir também aceitação.
Sem features, a checagem de estrutura continua válida; para exigir uma feature use
`--require-approved`. Não há migração automática de evidências do schema 1.

Uma revisão Git pode ser registrada como contexto, mas não substitui hashes de
conteúdo. Arquivos não commitados, untracked e projetos sem Git usam o mesmo
mecanismo de bytes. Árvores, variáveis de ambiente e serviços externos precisam de
identificação equivalente em arquivo observado (snapshot/configuração/manifesto),
com limites explícitos. O verificador só confere esses arquivos locais; não consulta
Git ou serviços nem autentica o snapshot. Implementação e oráculo no mesmo arquivo
são permitidos: a independência de suas regras exige revisão semântica.

Sem Python, acrescente à tabela Markdown os caminhos/identidades dos inputs, revisão
quando existir, método de comparação e responsável/data. Compare os conteúdos atuais
com as versões observadas e registre divergências e critérios afetados. Essa revisão
manual sustenta o fluxo; não a descreva como execução automatizada de freshness.

## Verificações por rota

| Situação | Verificação aplicável | Limite |
| --- | --- | --- |
| Local sem feature | Check funcional/inspeção pertinente, registro de inputs observados; verificador padrão para links/modelo/pontes, quando usado | Exit 0 sem features valida estrutura, não aceita a mudança |
| Local afetando feature existente | Check focado e atualização dos artefatos/evidências afetados; mesmos gates da feature | A rota não dispensa AC, rastreabilidade ou freshness |
| Fluxo completo em andamento | Checks por risco e `--structure-only` para estrutura antes da evidência | Não equivale a aceitação; não combinar com flags de aprovação/freshness |
| Aceitação automatizada de feature | `--features <diretório> --require-approved --require-fresh` | Exige schema 2, ACs decididos e inputs atuais; não prova adequação/autenticidade do oráculo |
| Fluxo manual, qualquer rota | Comparação de conteúdo observado/atual e cinco estados no registro existente | Não chamar revisão manual de freshness automatizada |

Os schemas e o validador não têm exceção de rota local. Para exigir aceitação
automatizada de uma mudança local ainda sem feature, represente-a no contrato
completo de automação; não use ausência de features ou `--structure-only` como aprovação.
O registro manual local pode ser curto: objetivo/critério, mudança, inputs/versões,
método, resultado, estado e limitação relevante. Preserve a observação anterior se
algo mudar; reexecute/reexamine apenas a evidência afetada, sem renovar hashes de um
resultado antigo para fazê-lo parecer atual.
