# Revisão da transição — 2026-10-26

Revisor: agente executor. Método: comparação com a baseline, leitura das
autoridades/contratos e implementação corrente, revisão das respostas históricas
dos três grupos e de seus limites. Não é revisão humana independente nem ensaio
novo de agente. Comandos/resultados automatizados constam das rodadas e recibos.

O plano v1.0 é coerente quanto à separação de fase, política, processo e método.
Corrigimos a interpretação de sua imutabilidade: observações antigas continuam
intactas na baseline, enquanto envelopes ativos afetados precisam mudar para
passar freshness honestamente. O arquivo de entrada permanece inalterado.
Não iniciamos uma segunda feature Rust por inferência do passo final do plano.

AGENTS continua apontando autoridades; project declara fase, estado e escopo;
GOV-06/07 separam desenvolvimento, aceitação e permissões. As dez POL e as outras
seis GOV não mudam. Os estados OPEN-01..11 permanecem; somente orientação de fase
e retomada de OPEN-10 mudam. Nenhuma plataforma, dependência, runtime ou sandbox
passou a ser aprovado.

Integração com skills: a ponte software-evolution realmente transporta IDs,
decisões/riscos e observações para cada artefato. A amostra
autonomous-verification-engineering distingue grants, execução, critérios,
snapshots e resultado; a skill genérica software-evolution permanece utilizável
sem SDD. Esses papéis são compatíveis: SDD é contrato do consumidor, não requisito
universal do método. O guia local resolve a lacuna de orientação sem duplicar
workflow ou exigir leitura indiscriminada da biblioteca. A baseline e os gates
confirmam identidade das 29 entradas/pontes e dos recursos; não se afirma uma
nova revisão técnica linha a linha de toda a biblioteca.

Reexame das features antigas: specs, plans, tasks e traceability permanecem;
E-EXT-* têm inputs alterados em affected-evidence.json e deixam os envelopes
ativos. E-TRANS-* identificam observações novas. AC-05 das skills é reexaminado
pela continuidade dos recursos, critérios e revisão de conteúdo histórica,
com estrutura/identidade testadas novamente no estado atual. Essa revisão
de continuidade não renova referências externas nem certifica APIs atuais.

AC-06: as respostas preservadas tratam grants/efeitos incertos, geração e
cancelamento, invalidação seletiva, conflito H0/H1, foco/épocas Iced, AST sem
resolução, inferência de grafo, falha/raw e cache/cumulativos. A leitura dos
três grupos e review anterior confirma que suas conclusões limitadas não dependem
da nova permissão de fase. A alternativa software-design no caso de SDK estável
e nenhuma skill no diagrama de marketing continuam justificadas. Não reexecutamos
modelos nem atribuímos às respostas conhecimento das novas autoridades.
Preservam-se exposição incidental do grupo 2, README ausente no grupo 1,
proximidade dos exemplos e ausência de versão/seed imutáveis. A existência desses
ensaios sustenta somente o critério textual delimitado. Os 36 cenários técnicos
continuam NÃO VERIFICADO, sem integração de runtime, UI, índices ou provedores.

Os 13 testes anteriores foram mantidos. Os seis adicionais exercitam mutações
de fase/autoridades, serialização real do ZIP e exclusão de Cargo/crates,
promoção indevida de skill, hash normativo, preservação/recuperabilidade e links
de diretório. A suíte restaura as fixtures e confere o retorno ao estado válido.
Os gates textuais cobrem regressões conhecidas, não arbitram autorização natural
nem substituem esta leitura semântica. A baseline registra conteúdos e não
autentica externamente o revisor.

Empacotamento: nome ox-governance.zip, package-scope.json dentro do ZIP e campos
de escopo no recibo externo usam a mesma origem. Teste inspeciona ZIP real com
fontes Cargo fictícias e confirma sua exclusão. A allowlist original é preservada;
um pipeline de aplicativo permanece por implementar. A qualificação completa
executa comandos reais na extração e conserva logs; audit hook Python não é
sandbox de SO. Nenhuma saída Python equivale a compilação ou integração Rust.

Limites: nenhuma nova avaliação de eficácia de modelo, teste do aplicativo,
publicação ou revisão de licença. Não há aprovação global do catálogo. Esta
revisão sustenta a transição da governança e a continuidade dos critérios de
autoria, com execuções e hashes vinculados separadamente no evidence.json.
