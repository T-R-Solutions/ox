# Revisão externa — SDD-ENXUTO-20261123

- Data: 2026-11-24
- Origem: texto colado pelo usuário na sessão do Claude Code; autor e ferramenta não informados.
- Modo declarado pelo revisor: consulta, sem editar o repositório nem o índice.
- Resposta do dono: [Revisão r2](SDD-ENXUTO-20261123.md#revisão-r2--2026-11-24--resposta-à-revisão-externa).

Texto recebido (literal; os rótulos de link do original ficaram sem destino ao colar):

> O SDD ficou mais centralizado, mas eu reabriria a task antes do commit. Os 12 critérios constam
> como APPROVED e os 61 hashes conferem neste checkout. Ainda assim, o AC-08 deixou passar
> referências a arquivos removidos, o AC-11 depende de logs locais e o validador pode dar exit 0
> ao ignorar uma decisão revisada. Registro da task
>
> ## Achados prioritários
>
> 1. O AC-08 precisa de nova validação. Reproduzi ocorrencias=0, mas o README da aplicação ainda
>    instrui a executar native_review.py e native_composition_review.py, ambos removidos. Dois ADRs
>    também apontam para caminhos removidos em sdd/features/. O padrão de busca omite esses
>    caminhos, e o verificador de links deixa passar referências em texto e código inline. Busca do
>    AC-08 · README da aplicação · ADR do Toolbox · ADR de fechamento
> 2. O aceite depende deste checkout. Em uma cópia temporária com os mesmos arquivos e sem .local/,
>    evidence --check --require-all saiu com código 1 e apontou 11 inputs ausentes. O Git ignora os
>    logs que o registro exige. A revisão precisa definir como recuperar ou reexecutar essas
>    observações em outro checkout para que o aceite continue verificável. Inputs do AC-11 · Regra
>    de retenção
> 3. A matriz ignora revisões do plano e dos itens. Em uma cópia temporária, acrescentei uma r2 que
>    vinculava D-01 ao requisito errado. O validador exibiu a matriz original e saiu com código 0. A
>    mesma mudança na tabela original produziu quatro falhas. As tabelas das etapas 4 e 5 são lidas
>    apenas das seções originais, embora o workflow determine que a revisão mais recente vale por
>    ID. Regra de revisão · Leitura das tabelas
>
> ## O que se confirmou
>
> - O contrato está reunido no workflow. O check confirmou seis perfis, sete TOMLs válidos e nenhuma
>   âncora ausente. A leitura ficou em 5.602 palavras, 33 abaixo da medição anterior. O ganho
>   principal foi concentrar as regras. Workflow · AC-07 e AC-12
> - Os 53 caminhos da lista estão ausentes e os 77 estados herdados das dez specs coincidem com os
>   registros anteriores em HEAD. Repeti validate.py, check-ox.py, os 58 testes do SDD e os 14 da
>   skill de auditoria. Consultei os logs das suítes de governança e scripts, que registram um teste
>   pulado cada. A verificação completa e o carregamento dos perfis em uma sessão nova ficaram fora
>   desta análise. Lista de remoções · Specs · Resultados registrados
>
> Há dois ajustes no encaminhamento. Regenerar o SVG sozinho repetiria o rótulo "governança e
> cópia", que ainda consta nas duas fontes Mermaid. E git add -A incluiria também as alterações
> locais em application/crates/. O índice já contém 330 renomes e 51 exclusões, e o registro novo
> segue não rastreado. Fiz a análise em modo de consulta, sem editar o repositório nem mexer no
> índice. Fonte do diagrama · Diagrama no README

## Revisão externa 2 — 2026-11-24

- Origem: texto colado pelo usuário, depois da r2; autor não informado; modo consulta.
- Resposta do dono: [Revisão r3](SDD-ENXUTO-20261123.md#revisão-r3--2026-11-24--base-fixa-do-ac-08).

> A revisão confirmou as correções no checkout atual. Ainda há um ponto no AC-08 antes do commit:
> a busca perde cobertura quando o HEAD avança.
>
> O script usa o HEAD corrente para descobrir quais caminhos foram removidos. Em uma cópia
> temporária, reintroduzi a referência a sdd/features/scripts-task-closure/plan.md. Com o HEAD
> atual, o teste detectou a referência e saiu com código 1. Com uma lista simulando o HEAD após as
> remoções, a mesma referência passou com ocorrencias=0. Fixar a base da comparação em ea3cf0f e
> reobservar o AC-08 preservaria a cobertura depois do commit. Script do AC-08
>
> - Evidência portátil. A cópia sem .local/ passou para as duas tasks, com 127 e 67 verificações.
>   Os 24 artefatos citados em r2/ podem entrar no Git e estão abaixo de 1 MiB. Teste da cópia ·
>   Exceção no .gitignore
> - Revisões do plano e dos itens. As duas matrizes e os 69 testes do SDD passaram, incluindo os
>   casos de decisão revisada incompatível, ID duplicado e tabela inválida. Testes de regressão
> - Documentação e proveniência. Conferi o novo rótulo dentro do quadro na captura do Firefox. O
>   registro de origem da GPL é idêntico, byte a byte, ao original em ea3cf0f. Captura · Registro
>   da GPL
>
> check-ox.py passou, os 25 pins conferem e a leitura obrigatória ficou em 5.631 de 5.635
> palavras. Consultei os logs das suítes de governança e scripts. A verificação completa via
> Toolbox e a execução com Python 3.11 continuam pendentes. O índice ainda tem os 330 renomes e as
> 51 exclusões anteriores. Fiz a conferência sem editar o repositório nem alterar o índice.
