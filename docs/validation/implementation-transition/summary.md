# Transição para desenvolvimento por SDD — 2026-10-26

A transição foi implementada. Os cinco critérios de `product-foundation` estão
APROVADO para governança. Fase atual: `implementation-foundation`; aplicativo:
`not-yet-implemented`. Não há crates, compilação ou integração Rust/Iced nesta entrega.

O [plano da feature](../../../sdd/features/product-foundation/plan.md) e a
[ADR](../../decisions/implementation-transition.md) registram a análise e os ajustes.
As 29 skills, 29 pontes, perfil e modelo SDD 1.3.0 foram preservados. O novo
[guia SDD/skills](../../development/sdd-skills.md) explica seleção, consulta, uso,
rotas e transferência de contribuições sem duplicar processo nas skills.
Somente GOV-06/GOV-07 e seus hashes de cobertura mudaram; POL-01..10 permanecem.

O plano v1.0 tinha um conflito: congelar envelopes antigos impediria freshness
depois de mudar seus inputs. A baseline [before.tar.gz](before.tar.gz) e
[before.json](before.json) preserva 392 arquivos anteriores, inclusive os
envelopes e o documento recebido. Os 11 conjuntos de evidência anteriores eram
vinculados amplamente a 320 inputs; mudanças afetaram todos. O
[mapa de impacto](affected-evidence.json) identifica cada observação/input alterado.
Specs/plans/tasks/rastreabilidade anteriores, ADRs e relatórios históricos não mudam.
E-TRANS-* substitui E-EXT-* somente após execução ou inspeção nova, descrita em
[review.md](review.md). Os 36 cenários técnicos continuam NÃO VERIFICADO.

| Verificação observada | Resultado | Registro |
|---|---|---|
| Baseline: SDD, check-ox e 13 testes | SDD/testes passaram; check-ox rejeitou link válido de diretório no plano de entrada | `docs/validation/runs/20261026T212731.499388Z/` |
| Primeira rodada após implementação | Quatro comandos exit 0; 19 testes passaram | `docs/validation/runs/20261026T213221.531227Z/` |
| Primeira qualificação do pacote | Cinco comandos exit 0 em extração independente | [recibo inicial](initial-package/results.json) |
| Rodada com contratos finais | Quatro comandos exit 0; 19 testes passaram | `docs/validation/runs/20261026T213539.079112Z/` |
| Qualificação com contratos finais | Inspeção, manifesto, fonte estável e cinco comandos exit 0 | [recibo](package-qualification/results.json) |

Comandos executados a partir da raiz, com `PYTHONDONTWRITEBYTECODE=1 python3`:
`sdd/tools/validate.py --root .`, `sdd/tools/validate.py --root . --structure-only`,
`src/scripts/check-ox.py`, `-m unittest discover -s src/tests -v`,
`src/scripts/run-checks.py` e `src/scripts/package-ox.py`.
Ambiente exato, saídas, exit codes e hashes estão nos respectivos results.json,
logs e manifests. O runner preserva todas as rodadas, inclusive a falha inicial.

Os seis novos testes cobrem regressões de fase, pacote realmente serializado sem
Cargo/crates, promoção indevida de skill, alteração normativa, imutabilidade e
links internos de diretório. Mantidos os 13 testes anteriores. Restaurar as
fixtures recupera os resultados válidos. Gates textuais não provam a semântica
de qualquer paráfrase; revisão do executor não equivale a avaliação independente.

O artefato é `ox-governance.zip`; tanto o ZIP quanto seu recibo declaram
`package_kind=governance` e `product_included=false`. A distribuição final inclui
estes registros e será acompanhada pelo recibo próprio em `dist/<rodada>/results.json`.
Os envelopes finais são saídas da coleta: o validador com `--require-fresh` e a
extração final os conferem após a escrita, sem hashes circulares. Seus logs finais
ficam junto do recibo de entrega. A aceitação não exige aprovação global das skills.

Para recuperar a baseline, extraia em pasta vazia e compare hashes; nunca
sobrescreva alterações posteriores por rollback indiscriminado. Para iniciar
código de produto, delimite a feature correspondente e resolva as ADRs pertinentes.
Os gates atuais de fase/estado deverão acompanhar essa mudança explícita.
Não houve ensaio novo de agente, sandbox real, definição de versões/plataformas
ou publicação. O pacote e a transição continuam separados de uma release do aplicativo.
