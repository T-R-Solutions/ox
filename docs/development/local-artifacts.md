# Artefatos locais: caminhos e retenção

A solicitação de 11/11/2026 substitui a política de cópias preservadas e leases
histórica de repository-maintenance. `.local/` contém
`.local/logs/AAAA-MM-DD/`: arquivos de diagnóstico por execução/ferramenta,
incluindo stdout, stderr, resultados JSON e identidades de inputs, com extensão
`.log`. Os bytes dos streams são preservados. Nomes incluem o identificador único
da execução e o caminho interno escapado, evitando sobrescrever logs do mesmo dia.
`.local/tasks/<ID>/` guarda saída bruta de task que a seção 8 do registro não cita; é
descartável e fica fora da rotação abaixo. Log citado é versionado em `sdd/tasks/<ID>/`
([workflow](../../sdd/workflow.md#evidência-e-retomada)).

São mantidas no máximo duas datas, pelo calendário local no encerramento da
execução. Antes de criar a terceira, remove-se a mais antiga. Publicação e rotação
são serializadas pelo lock do diretório logs; não há backup, lixeira ou recibo
anterior. `bash scripts/local.sh` simula a rotação; `--apply` a executa.
`--path runs|datasets|cargo` consulta os destinos sem criar arquivos.

Os scanners trabalham em diretórios exclusivos do sistema temporário e descartam
fontes copiadas, bases de trabalho e builds ao encerrar. Esses inputs temporários
servem à execução isolada de alterações nas fontes, não à recuperação. SIGKILL ou
queda de energia podem deixar trabalho no temporário do sistema; não há garantia
de limpeza após encerramento não capturável. Falha ao publicar logs é erro, nunca
sucesso do check. A política não promete preservação permanente de evidências.

Caches operacionais Cargo, ferramentas e RustSec ficam em `.cache/ox/`; não são
backups. O preparo RustSec elimina staging com falha e gerações substituídas.
Referências originais de design foram movidas para `.inputs/design/`, sem cópia.
Esses caminhos são ignorados pelo Git. Fontes e alterações não commitadas no
checkout não são apagadas. Não usar `.local` como destino de scripts avulsos,
archives, screenshots, backups ou builds. Recuperação de código usa Git, sem
pressupor que alterações não commitadas estejam disponíveis no GitHub.

Não foi executada verificação full nem nova aceitação de produto nesta mudança.
O wrapper Toolbox e seus parâmetros continuam independentes da política de logs.

## Verificação observada em 11/11/2026

`python3 -m unittest discover -s scripts/tests -v`: 39 testes, 38 aprovados,
um opt-in de ferramentas reais não executado. Inclui sete casos de retenção,
publicação concorrente, bytes brutos, symlinks, relógio regressivo e remoção de
trabalho temporário. Fixtures de adapters verificam falhas e códigos de saída.
`bash scripts/automate.sh --scope governance --check sdd-structure`: exit 0,
publicou logs de 11/11 e removeu 09/11, restando 10/11 e 11/11.
`git diff --check` nas superfícies alteradas: exit 0.

O inventário inicial encontrou ~45 GB em `.local`; a remoção deixou ~4,1 MB
antes da rotação real, ~32 KB depois dela (antes dos logs desta verificação).
Caches operacionais remanescentes somam ~718 MB; referências originais ~253 MB.
As gerações RustSec substituídas também foram apagadas; permanece a ativa.

`python3 tools/governance/scripts/check-ox.py` não passou: os registros de
sucessão e evidências existentes vinculam hashes anteriores de AGENTS, projeto e
scripts. A validação estrutural não elimina essa pendência de atualização das
evidências. Não foram criados backups nem renovados hashes desses relatos antigos.
Os logs de testes e governança ficam na mesma retenção de duas datas; a presente
observação documental não equivale a uma homologação dos scanners reais.
