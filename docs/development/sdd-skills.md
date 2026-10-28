# Usar skills em uma mudança SDD

O contrato da mudança está na spec; decisões no plan/ADRs; execução nas tasks;
aceitação nas evidências e na convergência. A skill fornece o método técnico.
Consulte o [workflow](../../sdd/workflow.md) para escolher a rota e o
[contrato de evidência](../../sdd/evidence.md) para registrar resultados.

Na rota local, uma pergunta delimitada pode usar uma skill sem criar feature,
plan ou ponte nova. Se a mudança afeta uma feature existente, reavalie os critérios
e inputs afetados. Contratos, autorização, dados, concorrência e recuperação
podem exigir rota completa mesmo em alterações curtas.

Na rota completa, parta do requisito e do risco. Encontre a competência no
[catálogo](../../.codex/skills/README.md), consulte sua
[ponte](../../sdd/chain/README.md), confira nome/caminho e leia a entrada real.
Registre no plan ponte/versão, caminho, papel, pergunta e contribuição esperada.
Selecione uma primária pertinente; auxiliares resolvem perguntas distintas.
Uma referência a outra skill não exige sua ativação nem instalação.

| Estado | Registro observável |
|---|---|
| Disponível | Entrada presente no catálogo/ambiente |
| Indicada | Candidata para uma pergunta ainda não resolvida |
| Selecionada | Escolhida para um papel e escopo |
| Consultada | Entrada real lida e identidade confirmada |
| Usada | Método aplicado a uma tarefa, decisão ou artefato identificável |

Não inferir uso a partir de consulta. Ferramenta ausente é lacuna explícita;
continuar as partes independentes. Nenhum desses estados é aceitação ou grant.

Forneça à skill os IDs REQ/AC, decisão/risco, tarefa, inputs e limites autorizados
pertinentes. Integre o resultado ao artefato que o possui: comportamento na spec,
alternativa no plan, trabalho nas tasks, observação na evidence/converge. Evite
repetir constituição ou workflow dentro de cada SKILL.md. As 29 pontes atuais já
mapeiam essas contribuições; não exigem que toda competência use SDD isoladamente.

Exemplo local: corrigir um link com destino conhecido requer inspeção do destino,
check pertinente e registro curto; não selecionar software-architecture só porque
o link aparece no mapa arquitetural. Exemplo completo: mudar cancelamento de
processos exige critérios e riscos; agent-runtime-engineering pode tratar o ciclo
de vida, e software-testing só entra se houver uma questão distinta de oráculo.
São exemplos de seleção, não autorização para implementar esses componentes.

Na retomada, leia spec, plan, tasks, converge e inputs reais. Compare os bytes com
os observados. Preserve o registro anterior antes de substituí-lo por evidência
nova; não renove hashes de uma execução antiga. Mantenha APROVADO, REPROVADO,
NÃO VERIFICADO, INCONCLUSIVO e NÃO APLICÁVEL justificado conforme o contrato SDD.

As features skill-* avaliam autoria e ensaios delimitados. Os quatro cenários
técnicos de cada especialização permanecem sem integração verificada. Uma feature
product-* precisa de seus próprios requisitos, oráculos e observações; a aprovação
de uma skill não certifica o aplicativo nem libera publicação.

## Identidade das especializações

As nove especializações usam apenas name e description no frontmatter por preferência
do projeto. Para registrar caminho/versão no plan, use caminho e SHA-256 do conteúdo
consultado (incluindo recursos utilizados), não metadata.version. As versões anteriores
continuam nas baselines e revisões históricas; bridge_version identifica a ponte.
