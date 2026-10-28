# SDD portátil

Versão 1.3.0 (caminhos em minúsculas). Estrutura própria de desenvolvimento orientado a especificações,
utilizável pelo Codex a partir deste documento. Não depende do GitHub Spec Kit,
de Python, de um catálogo fixo de skills ou de comandos especiais do agente.

## Adoção manual

1. Copie o conteúdo desta pasta para `sdd/` na raiz do projeto de destino.
   Se já existir `sdd/`, compare e incorpore
   os arquivos deliberadamente; não sobrescreva decisões, evidências ou instruções.
2. Preencha [project.md](project.md) com o contexto, caminhos e comandos reais.
   Reutilize a constituição e os documentos existentes quando forem a autoridade;
   não crie uma política concorrente.
3. Copie somente as pastas completas das skills necessárias para um local autorizado
   do projeto. Uma pasta de skill inclui seu SKILL.md e seus recursos internos.
   Para uso explícito, basta informar ao Codex o caminho da entrada; esta estrutura
   não instala nem pressupõe descoberta automática pelo agente.
4. Copie as pontes correspondentes do catálogo `sdd/chain/` da biblioteca para a pasta
   `sdd/chain/` do destino. Em cada ponte, ajuste `skill_path` para o caminho relativo à raiz
   do projeto até SKILL.md. Não copie o catálogo inteiro por padrão.
5. No Codex, peça: “Leia sdd/README.md e sdd/project.md. Use este fluxo para
   [objetivo], na feature [caminho], dentro de [escopo autorizado].” Essa frase é
   uma instrução no chat, não um comando de terminal nem uma skill instalada.

Sem skills ou pontes, o fluxo continua utilizável. Uma ponte ausente significa
apenas que a integração daquela especialidade não foi configurada.

## Rota da mudança

Escolha em [workflow.md](workflow.md) entre mudança local delimitada e fluxo completo.
A rota local usa inspeção, implementação, check focado e registro proporcional; riscos
materiais de contrato, autorização, dados, concorrência, consumidores ou recuperação
ampliam o fluxo. Atualize artefatos existentes afetados em ambas as rotas. Nenhuma rota
transforma falta de evidência em aprovação ou dispensa gates do projeto.

## Entradas do modelo

- [Fluxo](workflow.md): condução e retomada de uma feature.
- [Constituição inicial](constitution.md): princípios a conciliar com o projeto.
- [Contrato de evidências](evidence.md): resultados e rastreabilidade.
- [Pontes instaladas](chain/README.md): seleção condicional, sem ativação automática.
- [Templates](templates/README.md): copiar apenas os artefatos pertinentes.

Para acrescentar uma skill depois, copie a pasta e sua ponte, ajuste `skill_path`
e reveja a seleção no plan da feature afetada. Não altere o núcleo deste fluxo.
Para atualizar, compare as versões da skill e da ponte e preserve ajustes locais;
referências técnicas incorporadas a skills diferentes podem evoluir separadamente.

## Verificação opcional

O fluxo e a revisão de evidências funcionam com Markdown. Se Python 3.11+ estiver
instalado, o verificador stdlib incluído pode verificar links, pontes e o formato
JSON opcional das evidências, sem instalar pacotes, executar comandos dos relatórios
ou escrever arquivos:

```bash
python3 sdd/tools/validate.py --root .
python3 sdd/tools/validate.py --root . --features sdd/features --require-approved
python3 sdd/tools/validate.py --require-approved --require-fresh
python3 sdd/tools/validate.py --skill caminho/da/skill
```

O primeiro comando aceita um modelo ainda sem features. O segundo exige pelo menos
uma feature e seus critérios reconciliados. Se o projeto usa outro diretório, informe
`--features caminho/relativo`. Uma feature em andamento pode usar `--structure-only`;
para revisão automatizada completa, forneça os JSONs descritos em evidence.md.
Sem Python, percorra manualmente as mesmas verificações descritas nesse documento.
Este verificador não demonstra eficácia do agente, execução verídica dos testes,
compatibilidade de ferramentas nem proteção de merge.

Na biblioteca de origem, o modelo fica em `sdd/model/`, separado do catálogo de pontes.
Para verificá-lo sem copiar, use `python3 sdd/model/tools/validate.py --root . --model sdd/model`.
No destino, com o conteúdo do modelo em `sdd/`, os comandos acima usam o padrão sem flags extras.
