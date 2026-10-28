# ADR — Transição para implementação delimitada por SDD

Estado: adotada em 2026-10-26 após revisão, 19 testes e qualificação inicial
em extração independente (cinco comandos com exit 0). Proposta anterior
preservada no pacote inicial da transição. Aceitação corrente em
`sdd/features/product-foundation/`; envelopes finais sujeitos a freshness.

O mantenedor pediu a implementação/refatoração do plano de correção v1.0 e
autorizou os ajustes necessários à integração das skills com SDD. A preparação
da biblioteca não constitui implementação de Rust/Iced.

Decisão: fase `implementation-foundation` em sdd/project.md; AGENTS orienta;
constituição conserva políticas; cada entrega tem escopo autorizado e segue a
rota SDD proporcional ao risco. O pacote atual continua exclusivamente de
governança. Não são escolhidos runtime, IPC, banco, plataformas, sandbox, versões
ou licença, nem concedidas permissões externas por esta decisão.

Alternativas rejeitadas: manter a restrição de fase bloquearia trabalho futuro;
repetir políticas/SDD nas skills e em AGENTS criaria deriva; promover observações
de biblioteca a testes do aplicativo não teria oráculo válido. Preservamos as
29 entradas e pontes e acrescentamos orientação de integração no projeto.

Ajuste explícito ao plano v1.0: os envelopes ativos evidence.json/converge.md das
features anteriores não podem ficar congelados quando seus inputs mudam. Todos
os bytes anteriores ficam em docs/validation/implementation-transition/before.tar.gz,
com hashes em before.json. Apenas observações afetadas são substituídas após
reexame/execução; specs, plans, tasks, rastreabilidade, ADRs e relatórios antigos
permanecem intactos. Nenhum hash de uma execução antiga é renovado.

O verificador passa a aceitar links internos para diretórios existentes, pois
o plano fornecido contém um desses links. Escape continua rejeitado. A correção
preserva a entrada do usuário e será testada com destino ausente e externo.

Consequência: desenvolvimento delimitado fica permitido, sem criação de produto
nesta entrega. Os 36 cenários técnicos das skills continuam NÃO VERIFICADO.
O nome público do ZIP muda para ox-governance.zip; scripts mantêm seus caminhos.
Rever ao mudar fase, fronteira de autorização, perfil ou distribuição do produto.
