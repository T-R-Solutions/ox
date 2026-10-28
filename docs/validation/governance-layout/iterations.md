# Observações intermediárias — 2026-10-27

Antes das edições, `PYTHONDONTWRITEBYTECODE=1 python3 src/scripts/check-ox.py`
passou na árvore original. A baseline foi capturada antes da primeira alteração.

Primeira tentativa de estrutura: o validador original rejeitou dois links novos
de arquivos em sdd/ para docs/. Seu contrato exige destinos dentro de sdd/.
As referências foram convertidas em caminhos textuais; o método SDD não mudou.

Primeira execução direta de unittest no destino novo: 20 testes, três falhas e
um erro. As falhas apontaram os dois links novos; o erro apontou uma referência
sem barra final a src/scripts no teste de isolamento. A inspeção também encontrou
src/tests sem barra final em comandos de discovery. Corrigidos os consumidores,
mantendo os critérios. A execução ocorreu antes dessas correções e não é usada
como evidência de aprovação. Este é um registro resumido da observação da
ferramenta; não se afirma preservação de um log bruto dessa primeira tentativa.

Rodada após correções: `docs/validation/runs/20261027T121306.233493Z/` conserva
logs e hashes; os quatro comandos passaram e os 20 testes concluíram com OK.
Os envelopes estavam pendentes nessa rodada: ela demonstra funcionamento dos
comandos e não a aceitação final dos envelopes.

A primeira coleta final omitiu o vínculo de docs/validation/normative-coverage.md,
oráculo de adoption-governance. Freshness rejeitou o envelope; foi acrescentado
o hash já observado no manifesto daquela execução, sem renovar resultado antigo.
O detalhe da rejeição está em final-checks/00-first-freshness.log.

Primeira tentativa de pacote com envelopes consolidados:
dist/20261027T121946.828791Z/inspection-errors.json.
A inspeção recursiva rejeitou o ZIP por ultrapassar o orçamento de expansão
de 128 MiB. O backup novo completo duplicava os archives históricos que já
estavam na distribuição. A cópia completa original foi preservada localmente
em dist/governance-layout-recovery/full-before.tar.gz; o archive distribuído
passou a guardar as 55 versões alteradas/movidas, com os 384 inputs inalterados
retidos e identificados em recovery.json. A recuperação não depende de dist/.
Limite de inspeção e critérios foram preservados; foi exigida nova qualificação.
