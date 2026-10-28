# Revisão e evidências — maintenance-001

Observação em 27/10/2026, Python 3.13.16/Linux. Escopo: governança; sem produto.
Métodos e inputs: inventário before.json anterior às edições; comparação determinística
com baseline autenticada; runner 20261027T180119.943640Z (quatro comandos exit 0,
22 testes); verify-maintenance.py; inspeção de perfil, autoridades, origem e termos.
A primeira rodada 20261027T175754.169387Z falhou na mutação do perfil: leitura do
JSON corrompido levantava exceção. Correção: usar perfil histórico autenticado no
guard. A segunda passou; após decisão GPL e mudança da allowlist houve nova rodada.
Todas as rodadas e seus hashes permanecem preservados; não são intercambiáveis.

## Critérios atuais

AC-01: comparação byte a byte confirma exatamente retirada de metadata/version
1.0.0 das nove entradas. Testes negativos rejeitam descrição alterada, corpo alterado,
restauração do metadata, versão extra e recurso alterado. As vinte skills copiadas,
29 pontes, métodos SDD e perfil mantêm bytes. A versão anterior permanece na baseline;
identidade atual é caminho/SHA-256. quick_validate confirmou as nove entradas.

AC-02: before.json mede 80.950.232 bytes em 609 arquivos; 69.927.377 em dist.
composition.json discrimina locais e categorias sobrepostas. A exportação usa
allowlist explícita; teste verifica exclusão de dist, inclusão de LICENSE/NOTICE,
recusa de destino existente/interno e recuperação de 439 inputs. Testes da cópia
independente executam Ox e SDD com auditoria de acesso à origem. Procedimento e
limites em sharing.md. A qualificação final separada fica em detached-results.json.

AC-03: inventário de nomes/termos em árvore e archives, revisão de copy-001,
portable-sources e ADRs não revelou concessão explícita para terceiros. GPL-3.0-only
foi escolhida pelo mantenedor; LICENSE foi copiado sem alterações do texto GNU,
NOTICE delimita contribuições próprias e pendências. Não há copyright nominal
inventado. Não há declaração de prontidão pública. AC-05 continua NÃO VERIFICADO:
titular e permissões das cópias ainda precisam ser informados.

AC-04: verify-maintenance reconstrói os 439 inputs de governance-layout e encontra
os 485 arquivos governados anteriores, atuais ou em previous. before.json histórico,
archives e hashes antigos permanecem idênticos; não houve exclusão ou movimentação.
As nove especializações têm AC-01..04 NÃO VERIFICADO. Nenhum ZIP da solução foi
criado; os testes de archives usam buffers em memória. Nenhuma publicação ocorreu.

## Reexame dos critérios anteriores afetados

adoption-governance AC-01..04: checker autentica cópias e baseline, perfil exato,
29 pontes e cobertura local; suíte valida regressões. Relatório distingue validação
estrutural, revisão semântica, testes sintéticos, ensaios históricos e produto.

governance-externalization AC-01..06: cópia independente, inspeção recursiva e
mutações confirmam independência e rejeição; cobertura/link/perfil conferidos;
observações afetadas preservadas em previous e estados honestos. AC-07 exige um
novo ZIP real, portanto permanece NÃO VERIFICADO nesta revisão.

product-foundation AC-01..03 e AC-05: autoridades mantêm fase e escopo delimitado,
AGENTS aponta às autoridades e guia distingue seleção/consulta/uso. Contratos das
29 skills e SDD preservados sob a transformação expressamente autorizada. Testes
rejeitam promoção dos cenários técnicos e demonstram preservação recuperável.
AC-04 exige novo ZIP/recibos: NÃO VERIFICADO.

governance-layout AC-01, AC-02 e AC-04: os 23 caminhos movidos continuam na
organização vigente; perfil/fixtures e registros antigos mantêm bytes, comparação
com before e recuperação cobre todas as versões. Comandos em tools/governance e
config/governance passam; src permanece reservado. AC-03 exige novo ZIP: NÃO VERIFICADO.

Nove features skill-*: AC-05 reexaminado por comparação integral do corpo,
descrição, recursos e pontes com os inputs anteriormente revisados, auditor e teste
novo de preservação. AC-06 exige ensaio observado de agente: a observação anterior
está preservada, mas não foi repetida com o frontmatter atual e fica NÃO VERIFICADO.
Não reexecutar integração de produto inexistente nem promover os 36 cenários técnicos.

Limites: revisão do executor, não revisão humana independente. Hashes não provam
adequação dos oráculos. Auditoria de leitura Python não é sandbox do SO. Recuperação
compara bytes em memória, não executa os estados históricos. Arquivos históricos de
dist permanecem locais e fora do contrato exportável. Licença própria não sana direitos
de terceiros. Não houve medição do arquivo externo de aproximadamente 73 MB.
