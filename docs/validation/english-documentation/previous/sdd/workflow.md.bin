# Condução e retomada no Codex

Leia o contexto do projeto e as instruções aplicáveis antes de agir. A autorização
vem do pedido e do ambiente, não deste fluxo. Avance autonomamente nas ações locais
reversíveis autorizadas; pergunte apenas por ambiguidade material, conflito ou ação
que exija autorização. Não solicite aprovação rotineira entre todos os documentos.

## Escolha da rota

Use a **rota local** quando o objetivo e a aceitação forem claros, a superfície e os
consumidores forem conhecidos, a mudança estiver autorizada e for recuperável, sem
incerteza material sobre contratos, permissões, integridade, concorrência ou operação.
Exemplos: correção textual e reparo local que preserva um contrato conhecido.

1. Inspecione instruções, alteração existente, contrato/callers e checks pertinentes.
2. Implemente a mudança delimitada e execute a verificação focada que sustenta o resultado.
3. Corrija falhas causadas pela mudança e relate resultado, observação e limitação material.
   Registre objetivo, arquivos/versões observados e check no artefato já usado pelo projeto
   (issue, revisão ou nota); não crie spec/plan/tasks apenas para preencher pastas.

Use ou amplie para o **fluxo completo abaixo** quando houver decisão material não
resolvida, mudança de contrato/autorização, dados persistidos, concorrência, consumidores
com versões distintas, recuperação incerta ou alcance operacional que exija coordenação.
Uma alteração de uma linha pode exigir esse fluxo. Uma documentação extensa pode ser local.
Ao descobrir novo risco, preserve o que já foi feito, acrescente critérios/decisões/tarefas
necessários e prossiga; não reinicie trabalho comprovado nem reduza a aceitação para caber na rota.

Se a mudança afeta uma feature existente, atualize seus artefatos e evidências afetados,
mesmo pela rota local. Não esconda uma feature dos checks movendo-a de pasta. Mantenha os
cinco estados e compare inputs atuais com os observados segundo [evidence.md](evidence.md).
Uma tarefa pequena só termina quando os critérios aplicáveis estiverem sustentados ou
as lacunas materiais explicitadas; falta de ferramenta não significa aprovação.

As pontes mapeiam o fluxo completo. Na rota local, uma skill pode ser usada isoladamente
para uma pergunta concreta, sem instalar ponte ou criar plan. Em qualquer rota, não
carregue especialistas apenas por menção. [Verificações por rota](evidence.md#verificações-por-rota)
explica os limites da automação sem mudar seus gates.

## Constitution → specify

Identifique a constituição autoritativa. Inspecione o estado real e os contratos
existentes. Escreva ou ajuste a spec com atores, invariantes, cenários normais e
rejeitados, critérios identificáveis e limites. Diferencie requisitos de hipóteses
ou exemplos. Esclareça lacunas que impeçam decisões; avance nas partes independentes.

## Plan

Compare alternativas proporcionais, registre decisões/riscos e seus requisitos.
Consulte apenas as pontes presentes na pasta `chain/` deste SDD que correspondam à
superfície e ao risco. Confirme que o caminho configurado existe e que o nome da skill
confere. Leia a entrada real, escolha uma primária e auxiliares só para perguntas
não resolvidas. Registre ponte/versão, caminho e razão no plan; não importe o catálogo.

Uma skill ou auxiliar ausente não foi executada. Registre a lacuna e continue o que
não depende dela. Se a capacidade for indispensável à aceitação, mantenha esse
critério não verificado e peça a informação/capacidade necessária. Nunca instale,
finja ou percorra recursivamente uma cadeia de skills por mera referência.

## Tasks → implement

Decomponha mudanças e verificações com IDs, dependências, arquivos e condição de
conclusão. Examine a consistência entre spec, decisões e tarefas antes de implementar.
Use checklist apenas quando ajudar a avaliar qualidade dos requisitos; marcar uma
checklist não comprova que o código foi executado. Confirme comandos no projeto.

Aplique o procedimento da skill selecionada, se houver. Use referências somente
quando necessárias. Preserve políticas do produto em seus documentos de autoridade.
Registre alterações, falhas e verificações realmente observadas; não deixe testes
falhos desaparecerem pela alteração silenciosa do requisito.

## Converge e retomada

Percorra requisito → decisão/risco → tarefa → alteração → evidência → aceitação.
Registre os cinco estados definidos em evidence.md. Se houver lacuna executável,
acrescente tarefa delimitada e repita os checks afetados. Se houver impedimento,
registre dependência, impacto e passo exato de retomada. Não faça tentativas idênticas
sem informação nova nem declare conclusão porque o contexto ou orçamento terminou.

Ao retomar, leia spec, plan, tasks e o último registro de convergência; compare-os
com os arquivos atuais. Não confie em estado oculto do chat nem repita trabalho já
comprovado. Atualize evidências afetadas por mudanças de código. A conclusão depende
dos critérios aplicáveis, não da existência das pastas ou do número de documentos.
