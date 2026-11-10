# Dependências e política de verificação — 09/11/2026

## Implementado

- AGENTS.md registra a regra explícita do mantenedor para toda suíte completa
  autorizada: TOOLBOX_BIN=/home/rodrigo/Projetos/dev_audit/shared-toolbox/bin/toolbox
  seguido de bash scripts/automate.sh --scope full. scripts/README reproduz a
  orientação. Isso não inicia testes automaticamente nem muda o wrapper portátil.
- Licenças: revisados 264 pacotes do candidato contra os manifests e avisos do
  inventário anterior autenticado por archives/checksums. Zero divergências.
  Allowlist agora contém os oito identificadores adotados na política, incluindo
  GPL-3.0-only própria; nenhuma dependência ou contribuição foi relicenciada.
- Audit e OSV ignoram somente RUSTSEC-2026-0441 e RUSTSEC-2026-0192, aceitos
  temporariamente pelo mantenedor. Categorias, outros avisos, severidades e
  pacotes permanecem sob análise. Não foi inventado prazo de expiração: revisão
  na próxima alteração de dependências ou retomada do mantenedor.
- Três versões redundantes foram removidas do lockfile: skrifa 0.44.0,
  read-fonts 0.41.0 e font-types 0.12.7. A resolução conserva skrifa 0.37.0 já
  usada por cosmic-text e aceita por swash. Não houve download, fork, alteração
  da toolchain, Iced ou suas features.

Política, obrigações e lacunas de avisos estão em
[dependency-policy-20261109.md](../../licensing/dependency-policy-20261109.md).
Os dez subcrates Iced sem aviso standalone localizado permanecem como pendência
do acervo de redistribuição. Allowlist do build não constitui liberação pública.

## Execuções e resultados

| Método | Resultado e limite |
| --- | --- |
| cargo update -p skrifa@0.44.0 --precise 0.37.0 --offline em cópia isolada | Código 0; três remoções, nenhum pacote adicionado; lock promovido somente após conferir a preimagem do produto. |
| cargo test --workspace --locked --offline em application/ após a alteração | Código 0; seis testes gráficos ignorados conforme protocolo dedicado. Não revalida a matriz visual F0. Saída observada na sessão de ferramentas; não há stream integral persistido desta chamada. |
| checks/run.sh --check audit com configuração nova, antes e depois do lock | Código 0; warnings vazios, dois IDs explicitamente em settings.ignore; categorias unmaintained/unsound/notice permanecem. |
| checks/run.sh --check deny com lock anterior | Licenças 0 erros; bans 12 erros. Não foi declarado gate agregado aprovado. |
| checks/run.sh --check deny com lock reduzido | Licenças 0 erros, fontes 0 erros, bans 9 erros; retorno 2. Três famílias duplicadas realmente eliminadas, nove ainda presentes no grafo Linux do Deny. |
| checks/run.sh --check deny após disposição do mantenedor | Código 0, finding_count 0; nove skips por versão exata, sem permissão geral. |
| Fixtures nativas independentes de licença | GPL-3.0-only aceita (exit 0); AGPL-3.0-only não aprovada rejeitada (exit 4). A primeira tentativa usou --config em posição inválida e foi preservada; r2 usa a sintaxe corrigida. |
| Check OSV no sandbox | Recusado por falta de escrita do diagnóstico no volume externo da Toolbox. Sem classificação de scan limpo. |
| Check OSV com permissão aprovada e seleção explícita shared para mounts dedicados | Native exit 0, cleanup removed, 280 pacotes inventariados, ambos IDs filtrados com motivo. O gate Ox retornou 2: base upstream de 08/11/2026 11:02 UTC excede 24h. Não foi ampliada a validade nem feita manutenção da base. |

Registros nativos e streams copiados sem alteração para observed/, com origem e
SHA-256 em observations.json. Permanecem também nos runs privados originais:
security-IxtDSjHn, security-Z6uoCT5R, security-0stvPZvX, security-Ar1pZ3rO e
security-BEnhoYIK, security-YoN67NpR (Audit atual) e security-mfDPwe7z (Deny final).
Os hashes de todos os originais e suas cópias foram comparados na inspeção final,
sem divergências. Controles de licença têm streams próprios nesta pasta.
As configurações mantêm controles offline, formatos e rejeição de outras licenças.

## Duplicidades mantidas por decisão explícita

Famílias restantes no Deny Linux: calloop, calloop-wayland-source,
smithay-client-toolkit, rustix, linux-raw-sys, rustc-hash, syn, thiserror e
thiserror-impl. O arquivo duplicate-resolution.json mostra antes/depois do
lockfile completo, incluindo plataformas fora do alvo Deny Linux.

Evidência de restrição incompatível: iced_graphics/iced_tiny_skia 0.14 dependem
de cosmic-text ^0.15 e rustc-hash ^2; cosmic-text 0.15 exige rustc-hash ^1.1.0.
Winit 0.30.13 requer calloop ^0.13/rustix ^0.38; outros componentes requerem as
gerações posteriores. Syn 2 e 3 vêm de geradores de macros distintos. Eliminar
essas famílias exige migrar consumidores/stack, manter patches, ou deliberar
exceções específicas. Não se pode apagar os pacotes necessários do lockfile.

O mantenedor respondeu: preservar Iced 0.14 e documentar exceções específicas.
Foram adotados skips para as nove versões antigas exatas, com motivos em cada
entrada de deny.toml. Não há skip-tree ou permissão geral; multiple-versions=deny
continua ativo. As nove famílias continuam fisicamente no grafo e foram aceitas
na seleção conservada; três foram realmente eliminadas. AC-04 fica APPROVED
nesse critério explícito de redução mais disposição, não como eliminação total.
O Deny final (deny-final.stdout/stderr e assessment apontado) retornou zero.

## Estado e recuperação

AC-01 APPROVED por inspeção da regra; AC-02 APPROVED no componente de licenças;
AC-03 APPROVED para configuração e filtragem dos dois IDs, sem aceite da base
vencida; AC-04 APPROVED para três eliminações e nove exceções exatas autorizadas. A suíte
completa e os commits continuam pendentes, inclusive pelas falhas de governança
já registradas em commit-preflight-20261109. Não foram renovados hashes de
aceitações anteriores de produto/governança após mudar o lockfile.

before.json registra preimagens de arquivos preexistentes em before/*.bin.
Mudanças de outros autores, logs e histórico foram preservados. Compare os
hashes atuais com changes.json antes de restaurar; se diferirem, reintegre apenas
os trechos pertinentes, sem sobrescrever mudanças posteriores. A resolução
isolada permanece em .local/build/dependency-hygiene-20261109, excluída das fontes.
Nenhum commit, push, publicação, atualização de base ou instalação foi realizado.

### Restauração sem sobrescrever trabalho posterior

`changes.diff` compara somente esta etapa às preimagens, incluindo alterações
preexistentes mantidas. Para reverter os trechos desta etapa, examine o patch e
execute primeiro `git apply --reverse --check docs/validation/dependency-hygiene-20261109/changes.diff`.
Somente se a checagem passar e a comparação com `changes.json` confirmar que os
arquivos continuam com os hashes `after_sha256`, aplique
`git apply --reverse docs/validation/dependency-hygiene-20261109/changes.diff`.
Não force se houver divergência: há trabalho posterior a preservar.

Para recuperar uma preimagem à parte, por exemplo o lockfile, use
`cp --no-clobber docs/validation/dependency-hygiene-20261109/before/application/Cargo.lock.bin .local/Cargo.lock.dependency-hygiene-recuperado`
e compare com o arquivo atual antes de reintegrar os trechos desejados. O destino
separado e `--no-clobber` evitam sobrescrever tanto o produto quanto uma recuperação
existente. Os backups incluem os bytes e metadados copiados antes das alterações.
