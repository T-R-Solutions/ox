# Validação da governança independente

Revisão governance-externalization-001, 2026-10-26. Correções aplicadas ao repositório. Escopo: governança e biblioteca; aplicativo Ox não implementado. Estudos externos retirados de autoridades, verificadores e distribuição, inclusive originals.tar.gz. A baseline da biblioteca permanece intacta.

## Critérios do pacote

| Critério | Resultado observado | Evidência / limite |
|---|---|---|
| PKG-01 | PASSA: três estudos ausentes | Inspeção da árvore e ZIP |
| PKG-02 | PASSA: conteúdos integrais ausentes em arquivos/archives | Scanner recursivo por nomes, hashes e sequência de linhas; não detector de ofuscação arbitrária |
| PKG-03 | PASSA: ferramentas locais independentes | Inspeção de código; execução na extração com origem/pasta-pai negadas por audit hook Python |
| PKG-04 | PASSA: links Markdown operacionais | check-ox; referências históricas ficam em snapshots identificados |
| PKG-05 | PASSA: validador SDD padrão, exit 0 | Runner e extração independente |
| PKG-06 | PASSA: SDD structure-only, exit 0 | Runner e extração independente |
| PKG-07 | PASSA: check-ox, exit 0 | Contratos locais, integridade, perfil e archives |
| PKG-08 | PASSA: 13 testes | Mutações e restaurações, com diagnóstico de falhas |
| PKG-09 | PASSA: runner, exit 0 | Rodadas imutáveis em docs/validation/runs |
| PKG-10 | PASSA: cópia independente | Cópia explícita; subprocessos na árvore copiada |
| PKG-11 | PASSA: falhas relevantes detectadas | Recurso, ponte, autoridade, perfil, catálogo, IDs, evidência, link e observação histórica |
| PKG-12 | PASSA: 18 IDs locais vigentes | POL-01..10/GOV-01..08; 72 IDs antigos somente no mapa de decisão |
| PKG-13 | PASSA: história preservada | 59 artefatos protegidos; E-RELOCATION obsoleto arquivado; novos E-EXT-* |
| PKG-14 | PASSA: 36 cenários NÃO VERIFICADO | Nove specs mantêm todos os REQ/AC; nenhum teste de produto foi alegado |
| PKG-15 | PASSA: 29 skills/29 pontes | Perfil versionado; 20 cópias com todos os recursos preservados |
| PKG-16 | PASSA: novo ZIP e smoke test | Cinco comandos exit 0 na extração; manifesto e SHA-256 por arquivo |

[Inspeção e limites](governance-externalization/inspection.md), [qualificação de pacote](governance-externalization/package-qualification/results.json), [cobertura normativa](normative-coverage.md) e [ADR/mapeamento](../decisions/governance-externalization.md).

## Rodadas e estado vigente

A rodada 20261026T200610.956828Z conserva as falhas iniciais encontradas durante a migração. As correções de links históricos e leitura gzip/tar foram seguidas por rodadas verdes. A revisão adicional ampliou a suíte para 13 testes e corrigiu referências de origem nas specs/plans, sem alterar critérios. Rodadas de fechamento conferem os novos envelopes schema 2; não reaproveitam hashes de resultados antigos.

As observações de qualificação precedem a escrita dos envelopes de aceitação. O pacote final é gerado novamente após o fechamento; seu recibo em `dist/<rodada>/results.json` identifica o ZIP e o hash exatos, todos os arquivos e logs da extração. Esse recibo fica ao lado do ZIP, evitando hash circular do próprio pacote. O ZIP inclui manifesto e resultados de qualificação internos. `package-ox.py` falha se a origem mudar durante sua construção.

A nova inspeção de AC-05/06 das skills reexamina conteúdo e respostas históricas preservadas, sem alegar nova execução de agentes nem conhecimento da constituição nova por agentes antigos. Há 36 pendências técnicas legítimas; testes de governança não as aprovam. As quatro aceitações de adoção e sete da migração usam critérios locais e evidências novas. Não usar require-approved global.

Licença/plataforma/sandbox do produto permanecem decisões abertas, conforme o escopo. O audit hook prova rejeição dos acessos exercitados pelas ferramentas Python; não oferece isolamento de processos arbitrários. Backup completo anterior em `/tmp/ox-before-externalization-zj4erab3/`, externo e temporário; não é dependência de operação. Restauração deve ocorrer em diretório vazio.
