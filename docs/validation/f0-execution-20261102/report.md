# F0 — execução e decisão em 2026-11-03

**F0 ABERTO.** Houve correções e verificação operacional; os requisitos gráficos e
a aceitação de desempenho ainda têm lacunas. A [matriz completa](matrix.json)
registra cenário, ambiente, resposta, método, limite, responsável, condição de
aprovação, código, oráculo, evidência, inputs e lacuna por requisito. A
[revisão gráfica](graphical-review.md) explica as observações conflitantes.

Decisões adotadas: [F0-D1–D5](../../decisions/f0-boundary-20261102.md), processos
locais controlados sem sandbox, Linux x86_64 com X11/Wayland separados, versões
controladas sem atualização, sucessão delimitada de obrigações históricas,
persistência independente após F0 e antes de F3/MVP. Também foram adotados os
limites do corpus de backend/histórico e a exceção temporária de ttf-parser 0.25.1,
com revisão mensal e antes de distribuição/fontes não confiáveis. O contrato e a
comparação futura de persistência permanecem em
[local-persistence-proposal](../../decisions/local-persistence-proposal.md), sem
escolha ou implementação de tecnologia.

Trabalho executado:

- Cancelamento real do verificador e de chamadas em andamento do host, com propagação
  pela interface e observação de saída do filho; prazo do subprocesso distinguido da
  duração total. Reprodução anterior e teste posterior preservados.
- Histórico limitado a 128 MiB de conteúdo retido, com reserva antes de lançar o
  oráculo, recusa explícita e preservação das observações anteriores.
- Navegação/foco de teclado, contraste de input/foco, linhas adaptáveis e rolagem
  por teclado. Sem alegação de acessibilidade além dos cenários observados.
- Inventário de dependências/licenças/native/unsafe e ameaças com efeitos proibidos;
  três defeitos deliberados detectados em cópias isoladas, sem meta arbitrária de
  mutação. [Cenários e asserções](scenario-inventory.json),
  [segurança e limites](security-review.md), [fontes consultadas](sources.md).
- Reconciliação de evidências com hashes históricos preservados; correção da
  exclusão de F0 operacional da exportação de governança. A regressão falhou antes
  e passou depois. Nenhum pacote foi publicado ou commit criado.

Verificações atuais: `cargo check`, `fmt`, `clippy -D warnings` e suíte comum
passaram: **29 testes, 0 falhas, 6 gráficos ignorados explicitamente**. Os seis
cenários X11 passaram separadamente na build comum. As escalas 150/200% passaram
no corpus visual. Testes instrumentados tiveram timeouts de interação; repetições
isoladas passaram, preservando a instabilidade. Shift+Tab não pôde ser comprovado:
o servidor não honrou o modificador injetado. Wayland identificado fechou com saída
0, mas faltam artefatos que correlacionem a jornada declarada ao workspace.

Governança: **46 testes passaram**, sem ignorados; checks de estrutura/freshness,
perfil/links e cópia independente passaram. Recuperação: **485 arquivos governados,
439/439 inputs históricos**, com mapeamento específico dos
[125 registros de cópia](library-lineage.json) e
[23 realocações](relocation-lineage.json). Os 84 predecessores do inventário inicial
estão preservados; alterações anteriores, falhas e direitos de publicação pendentes
não foram apagados. A [revisão de sucessão](legacy-review.md) não aprova retroativamente
os gates de ZIP/publicação.

| Medição atual | Resultado | Limite / estado |
|---|---:|---|
| Cobertura total | 908/987 = 92,00% | Medida; sem meta total inventada |
| Linhas executáveis alteradas | 199/220 = 90,45% | Meta inicial 80% atendida |
| Execução / verificação, máximo | 10,257 / 3,501 ms | 50 / 50 ms adotados; atendidos |
| Cancelamento runtime / verificador, máximo | 0,119 / 2,315 ms | 100 ms até saída observada; atendido |
| RSS harness | 8,57 MiB | 32 MiB adotados; atendido |
| RSS histórico, 3 execuções corrigidas | 160,72 / 160,78 / 157,02 MiB | 256 MiB adotados; atendido; antes 1,90 GiB |
| Resposta por imagem X11, máximo 100/150/200% | 47,31 / 67,00 / 87,92 ms | Proposta 120 ms, ainda não adotada |
| RSS GUI, máximo do corpus | 35,59 MiB | Proposta 64 MiB, ainda não adotada |
| Desenho/apresentação cliente, máximo 100/150/200% | 51,32 / 68,95 / 98,54 ms | Proposta 125 ms, ainda não adotada |
| CPU ociosa, observação de 10 s | 0–2% de um núcleo | Proposta 5%, ainda não adotada |

Protocolos e limites: Ryzen 9 7900X/openSUSE, build dev, corpus controlado;
3 aquecimentos/20 amostras para backend e resposta visual, 3 execuções de histórico.
[Dados de backend](backend-final-summary.json), [histórico](history-summary.json),
[GUI](gui-metrics-final.json), [frame/CPU](frame-cpu-summary.json) contêm amostras e
variabilidade. O timer de frame usa cópia instrumentada identificada de
iced_winit 0.14.1; mede desenho até retorno da apresentação cliente, não exposição
física nem layout anterior. Seu corpus inclui redimensionamento/ociosidade e falha
final de saída em 100%; é diagnóstico, não aceitação. CPU zero observado tem
resolução limitada. Os limites propostos são margens de engenharia deste corpus,
com revisão se houver workload/plataforma diferente; não foram ajustados para
transformar falha em sucesso.

[Cobertura por componente](coverage-components.json) inclui denominadores zero como
não aplicáveis, nunca 100%. LLVM 23.1.4/rustc LLVM 23.1.1; baseline inclui os bytes
sujos/não rastreados anteriores. Excluídos módulos de testes, fixtures, exemplos e
dependências; UI própria incluída. Filhos terminados à força podem perder contadores.
Percentuais não substituem oráculos nem aprovam Wayland.

| Requisitos | Estado final neste escopo |
|---|---|
| F0-P02, P03, P04, P06, P07 | APPROVED |
| F0-P01, P05 | INCONCLUSIVE |
| Q01, Q02, Q03, Q04, Q09, Q10, Q11, Q12 | APPROVED |
| Q05, Q06, Q07, Q08, Q13 | INCONCLUSIVE |
| Implementação durável em F0; SDK/distribuição; capacidades posteriores | NOT APPLICABLE por D2/D3; obrigações posteriores preservadas |

Reaproveitado: contratos, corpus/oráculos existentes e registros históricos somente
onde seus inputs permanecem pertinentes; observações antigas conservam seus hashes.
Executado agora: medições, novos testes/correções, regressões, mutações, GUI e checks
relatados acima. Apenas proposto: limites novos de GUI/frame/CPU e matriz de suporte,
experimentos/tecnologia de persistência, qualificação de distribuição futura.

Bloqueios e retomada:

1. **Q05/Q06/Q07, P01:** mantenedor disponibiliza sessão/interação gráfica identificada;
   executor correlaciona workspace, resultados, veredictos, teclado/foco, cancelamento
   e saída em Wayland, comprova Shift+Tab e resolve a instabilidade de observação.
   A confirmação humana existente não substitui os artefatos ausentes.
2. **Q08, P01:** mantenedor adota ou revisa os limites propostos e a matriz
   100/150/200%, 640×480/900×700; executor verifica o contrato adotado, separando
   X11/Wayland e duração cliente/apresentação física. Ampliar o envelope exige novas
   medições; adotar o corpus restrito não aprova dimensões não observadas.
3. **Q13, P05 / AC-05 do gate:** após resolver os itens anteriores, executor atualiza
   somente observações afetadas e reavalia a matriz inteira. Até lá, **não encerrar F0**.

[Inputs da decisão final](inputs-acceptance.json) identificam código, oráculos,
configuração, lockfile, ambiente e registros. Identidade não comprova suficiência.
