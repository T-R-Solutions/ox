# Plano — transição da fundação

Rota completa: muda o contrato operacional e a forma de distribuir/aceitar o
pacote. Baseline real sem Git: docs/validation/implementation-transition/before.tar.gz
e before.json. Recuperar em pasta vazia, comparar bytes e preservar qualquer
versão inesperada antes de aplicar uma restauração seletiva.

| ID | Decisão / risco | Relação |
|---|---|---|
| D-01 | Fase em project, política em constitution, entrada em AGENTS; apenas GOV-06/07 mudam | REQ-01, REQ-02 |
| D-02 | Skills/pontes/modelo preservados; guia de uso no projeto; critérios do produto independentes | REQ-02, REQ-03 |
| D-03 | Allowlist inalterada; nome e metadados explícitos no ZIP e recibos | REQ-04 |
| D-04 | Arquivar bytes anteriores e substituir somente envelopes de evidência/convergência afetados após observações novas | REQ-05 |
| D-05 | Aceitar links internos para diretórios existentes; preservar o documento de entrada | REQ-05 |
| R-01 | Interpretar fase como permissão irrestrita ou obrigar fluxo completo a toda correção | REQ-01, REQ-02 |
| R-02 | Confundir skills disponíveis, usadas e aprovadas com implementação do produto | REQ-02, REQ-03 |
| R-03 | Distribuir ZIP de governança como release Rust ou usar metadados divergentes | REQ-04 |
| R-04 | Congelar evidência obsoleta ou renovar hash de resultado antigo | REQ-05 |
| R-05 | Oráculo rejeitar histórico legítimo ou aceitar mutações normativas | REQ-05 |

| Competência | Ponte / versão | Entrada consultada | Papel, pergunta e entrega |
|---|---|---|---|
| software-evolution | sdd/chain/software-evolution.md / 1 | .codex/skills/software-evolution/SKILL.md | Primária: migrar contratos conservando consumidores e história; sequência, compatibilidade e recuperação |
| skill-creator | Sem ponte; ambiente; versão não declarada | /home/rodrigo/.codex/skills/.system/skill-creator/SKILL.md | Auxiliar: integrar skills ao SDD sem copiar processo/políticas; análise das responsabilidades e guia local |

As duas foram selecionadas, identificadas e consultadas. Uso: decisões acima
aplicadas nesta mudança. A entrada autonomous-verification-engineering foi
inspecionada como amostra de contrato da biblioteca, sem seleção/ativação do método.
Não carregar toda a biblioteca, instalar skills ou delegar por mera referência.

Alternativas: reescrever 29 skills acoplaria competências reutilizáveis ao Ox;
duplicar o SDD em AGENTS criaria autoridades concorrentes; manter evidência ativa
imutável faria freshness falhar. O plano v1.0 é ajustado nesses pontos, com
aprovações antigas preservadas na baseline e reexame explícito no estado corrente.

Compatibilidade: modelo SDD 1.3.0, paths das 29 pontes, comandos Python e perfil
permanecem. Muda intencionalmente o nome do ZIP; consumidores devem ler o recibo
novo. Não há processo, banco ou aplicação implantada a migrar. Não iniciar outra
feature de produto por inferência desta transição.

Baseline executada em docs/validation/runs/20261026T212731.499388Z: SDD e os 13
testes passaram; check-ox rejeitou o link existente para docs/decisions/ no plano
de entrada. D-05 corrige a falsa rejeição sem remover o documento do usuário.

Oráculos: mutações nas autoridades atuais, no escopo de pacote, nos estados das
skills e no histórico, com restauração; teste de cópia independente; qualificação
do ZIP com manifesto e auditoria de leitura. Hashes são identidade, não prova de
revisão. Revisão semântica do executor é separada das execuções e não é humana
independente. Reavaliar ao mudar fase, política, perfil ou pipeline de produto.
