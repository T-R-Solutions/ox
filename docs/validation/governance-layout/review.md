# Revisão da organização — 2026-10-27

Revisor: agente executor. Método: inspeção dos consumidores, comparação com a
baseline anterior, leitura dos critérios das features afetadas e revisão de
continuidade dos resultados históricos. Não é revisão humana independente.
As execuções novas têm logs/inputs próprios; não se renovam hashes antigos.

AC-01 de governance-layout: o inventário original tem 23 arquivos: sete scripts,
um teste e quinze JSONs. Treze JSONs são prompts, avaliações e catálogo dos ensaios;
perfil e cobertura são configuração vigente. verify-layout.py compara todos os
membros da baseline e os destinos, confirma src/ sem arquivos de governança,
identidade de perfil/fixtures e ausência de perda. Scripts corrigem a profundidade
da raiz em um nível; imports e subprocessos usam os destinos reais. O validador
skill-quick-validate.py não foi modificado. Não foi criado código Rust nem decidido
um layout de crates. A pasta src/ pode permanecer vazia até existir aplicação.

AC-02: README e project mostram os comandos atuais; a constituição aponta para
o perfil real. Rastreabilidades ativas usam os novos oráculos. O núcleo SDD é
idêntico à baseline; seu validador limita links ao SDD, portanto as referências
novas a docs/ em project/índice são caminhos textuais. As ocorrências antigas em
ADRs, revisões de proveniência, logs, baselines e archives registram os locais
históricos e não são comandos atuais. A nova ADR sucede explicitamente apenas
localização/allowlist. O guard de preservação traduz o perfil e os dois campos
de caminho das rastreabilidades antigas, comparando os bytes originais verificados
do archive; não ignora genericamente arquivos modificados. O teste novo altera
perfil e duas rastreabilidades migradas, observa rejeição e restaura o sucesso.
Os testes anteriores mantêm mutações de skill, ponte, link, autoridade, evidência,
estados de fase, histórico e isolamento de leitura.

AC-03: a allowlist substitui src/ por tools/governance/ e config/governance/.
O teste produz um ZIP real com fontes Rust fictícias em src/ e crates/, Cargo,
ferramenta/configuração alheias, binário e plugin. Esses caminhos são excluídos;
governança e configuração são incluídas e todos os hashes do manifesto conferem.
O pacote inicial passou inspeção recursiva, extração, comparação de manifesto e
cinco comandos reais com exit 0. Durante a qualificação os envelopes estavam
pendentes; a entrega final confere também os envelopes consolidados. O audit hook
Python é um oráculo de leitura da origem, não um sandbox de sistema operacional.

AC-04: before.json, before.tar.gz e recovery.json permitem recuperar os 439
arquivos anteriores: 55 versões alteradas/movidas no archive, incluindo todos
os envelopes anteriores, e 384 arquivos inalterados retidos na distribuição e
verificados por hash. A cópia completa original fica preservada localmente em
dist/, sem dependência de recuperação. A primeira tentativa de pacote final
excedeu o orçamento de inspeção de 128 MiB devido a archives históricos duplicados;
a deduplicação remove essa repetição sem elevar o limite nem perder versões.
O inspector verifica a recuperação, o archive,
histórico, skills, pontes, método SDD e contratos anteriores; permite somente a
tradução especificada e a revisão acrescentada à proveniência. GOV-04 mudou
somente o destino do link, de modo que seu hash foi revisto na cobertura; as
demais regras e POL-01..10 permanecem idênticas. O perfil mantém inclusive a
revisão e o hash já aprovado. A cobertura mudou apenas no oráculo e nesse hash.

Reexame de adoption-governance: AC-01/02 continuam sustentados pela identidade
das cópias e baseline, inventário e pontes; AC-03 pela cobertura local revisada,
cinco estados e separação do produto; AC-04 pelas novas execuções e pela
preservação dos limites dos ensaios. Não se trata de nova implementação.

Reexame de governance-externalization: AC-01/02 usam cópia/extração independente,
inspeção recursiva e testes adversariais; AC-03/04 usam configuração atual,
links, catálogo e mutações/restauração. AC-05 conserva observações anteriores
no archive e as substitui por estas observações novas; AC-06 conserva os 36
cenários técnicos NÃO VERIFICADO; AC-07 usa o ZIP qualificado com inputs próprios.

Reexame de product-foundation: AC-01 permanece com implementation-foundation e
not-yet-implemented, sem nova permissão; AC-02 conserva AGENTS, guia, 29 skills,
29 pontes e SDD; AC-03 conserva critérios independentes e rejeição da promoção
de skills; AC-04 usa o novo pacote e sua exclusão de fontes de produto; AC-05
usa baseline, mutações, preservação e novas evidências. A nova organização
sucede o detalhe histórico de allowlist/caminhos; os requisitos não mudam.

Reexame das nove skill-*: AC-05 conserva os conteúdos e métodos observados na
revisão histórica, com identidade/estrutura verificadas novamente. AC-06 conserva
as mesmas respostas dos três grupos e sua avaliação histórica. Foram relidos os
limites em agent-evals/review.md e implementation-transition/review.md; os dados
de prompts/oráculos apenas mudam de lugar. A comparação de hashes confirma
continuidade, não uma revisão técnica nova linha a linha de todas as skills.
Não houve execução nova de agentes ou consulta externa: continuam os limites de
exposição incidental no grupo 2, README ausente no grupo 1, proximidade de exemplos
e falta de versão/seed imutáveis. Os registros sustentam somente os critérios
textuais delimitados; AC-01..04 técnicos permanecem NÃO VERIFICADO nas nove skills.

Os inputs das execuções são registrados nos manifests antes dos comandos; os
vínculos de evidência nova referem somente bytes efetivamente observados. Envelopes
e converge são saídas de coleta, depois verificadas por freshness/extração para
evitar hashes circulares. A primeira qualificação não é reapresentada como uma
extração dos envelopes finais. Não há teste Rust/Iced, eficácia de modelo, CI,
publicação ou efeito externo nesta aceitação de governança.
