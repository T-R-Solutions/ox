# Independent review — 2026-11-14

Delivered by `/root/governance_execution/independent_review`, profile ec_revisor,
in a new context, independent of both implementers and coordinator. The reviewer
had a read-only role and returned this verdict to the coordinator for recording.
The following preserves its findings, observations and limits; integration results
are separate and cannot reinterpret the reviewer's failed intermediate check.

Parecer independente: **nenhum defeito pendente confirmado nos contratos e fontes
examinados**. Houve um achado documental baixo, corrigido e reexaminado. A
integração/aceitação final permanece aberta.

**Achado resolvido — baixo, AC-03/AC-12.** deduplication.json,
`inventory[*].bridge_sections`: originalmente 30 mapas tratavam o corpo da ponte
como título, impedindo o mapeamento por obrigação anunciado. Após correção, conferi
as 31 pontes: mapas anteriores e atuais correspondem às respectivas seções,
normalizando somente whitespace externo. `inventory_correction` registra a falha
original. Nenhuma perda de método foi encontrada.

Escopo efetivamente examinado:

- Spec canônico AC-01–15, suplemento aprovado A01–A10, workflow/evidence,
  autoridades e procedimento comum.
- validate.py: projeções, normalização dos estados históricos, seleção completa
  de features, compatibilidade posicional, fronteiras project/portable/skill,
  caminhos ausentes/escapantes e symlinks.
- README, templates e adoção isolada; consumidores check-ox, sucessão
  instruction_revision/closure_revision, perfis e configuração.
- Commit skill: resolução da receita completa em AGENTS, catálogo real em plano,
  escolhas negativa/sem resposta e falha preservadas.
- Todas as 31 identidades de skills/pontes. Trinta skills mantêm bytes anteriores;
  commit-governance conserva métodos fora dos trechos deliberadamente alterados.
  Seleção, contribuições e handoffs das pontes comparados com pré-imagens.
- Entrada atual de project.md, histórico preservado, projeções e descarte
  delimitado de observações afetadas.

| Cenário A07/A08 | Contrato observado |
|---|---|
| Triador delegado | Somente leitura, sem testes/implementação/filhos; devolve encaminhamento |
| Raiz com orquestrador disponível | Controlador distinto do triador; encaminhamento proporcional ao risco |
| Raiz sem delegação, diagnóstico | Conclusão direta permitida com fontes e limites |
| Typo/link ou bug local conhecido | Direto somente com autorização, reversibilidade, consumidores/oráculo conhecidos e ausência de risco material |
| Feature existente | Conserva gates, bindings e documentação aplicáveis |
| Migração, permissão ou checker | Coordenação alta e revisão/validação independentes |
| Capacidade/vaga indispensável ausente | Análise autorizada continua; execução dependente bloqueada com retomada explícita |
| Escopo materialmente incerto | Classificação alta provisória |
| Orquestrador descobre risco maior | Interrompe novas atribuições, confere escritores/efeitos e devolve continuidade ao controlador |
| Restrição expressa do usuário/host | Prevalece; não autoriza fallback ou autorrevisão declarada independente |

| Método executado | Resultado observado |
|---|---|
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools/governance/tests -p 'test_instruction_*.py'` | 37 testes, OK, sem skips; adoção isolada e plano real da CLI |
| `PYTHONDONTWRITEBYTECODE=1 python3 sdd/tools/validate.py --root . --structure-only` | Exit 0 |
| inputs-before.json contra pré-imagens | 198 hashes corretos |
| Predecessores das convergências | 39/39 preservam integralmente bytes anteriores |
| Projeções contra specs/JSON | 39 envelopes, nenhuma divergência |
| Inventário corrigido | 31 mapas antes/depois corretos; 62 hashes atuais skill/bridge correspondentes |
| Objetos históricos fora da feature em integração | 42 retidos sem alterações; 20 retirados; nenhum retido teve digest renovado |
| `PYTHONDONTWRITEBYTECODE=1 python3 tools/governance/scripts/check-ox.py` | Exit 1: Instruction current changed: sdd/features/configuration-cohesion/plan.md |

O último resultado observa integração ainda ativa: o plano canônico mudou depois
do registro de sucessão examinado. **Não constitui gate final aprovado**. Atualizar
a sucessão de forma delimitada, estabilizar inputs e executar nova observação
compete ao coordenador/validador; não reinterpreto esse exit como sucesso.

Identidades observadas, SHA-256:

```text
sdd/tools/validate.py
3b1e99d6152dbf7e6ac27dba534798baa66b57a63ba6f943c40de151f243922c
sdd/README.md
f8911d01b52f15fa742d0581787306c36f6958c1418d0812bba8d2d7aea06cf4
sdd/evidence.md
bb40a4eb436f4dbbdc73bceebc2e7c3017ab5453fd5ba32504eba6cd7b85c731
sdd/project.md
82c57cdebb84cd3a620e02de99cc91485076c8d389b9644016dc09ebb13bcfa1
docs/development/codex-agents.md
505454d7e54e203b5c085e8cdcc1dacfd1cd84e65a9443a730936941ba489adf
.codex/config.toml
ed3f9ecb380bb4aeb80467ee8865d321964ce4f47213298b4dc01a6c0304bb2f
.codex/skills/commit-governance/SKILL.md
ba5f5cb409c17eda4d86a7e395cfad20ac3cb8f603862c69fccfe8476abb4bac
tools/governance/scripts/check-ox.py
18ff504a58f5855d42859d92fc0bcd060fbb9e0d87ccd205041eed3a3d9acd58
tools/governance/scripts/instruction_revision.py
f3860616cb134886f0239e0a1776365173c266480d8da0dae9e4179d92409521
tools/governance/scripts/closure_revision.py
ada790ecb821deaede6db9f95d3ec0c023572fea0dfd55064c65ef618a644878
docs/validation/governance-corrections-20261114/inputs-before.json
ca8186d1397b241988ec1a9e9f1636b1fa4b1c56b530af4367431d38eab110e7
docs/validation/governance-corrections-20261114/succession.json
3c1cb405c851f6f6764238277bc73d1fa1497b129d5c20693150a17e993724c6
docs/validation/governance-corrections-20261114/deduplication.json
06469c17eb4a0a3a894200093e07474200e360841695ac46fc030ae1498596cc
tools/governance/tests/test_instruction_governance.py
fc0b6061909dcdf3b1dae3c64e245815156833078d6b727c7e596c580a81e235
tools/governance/tests/test_instruction_routes.py
257e08e39ff66af1ba91342808e388fdf4f881517b1200997a1ad66d6e05d39a
tools/governance/tests/test_instruction_succession.py
45bd395a68cf953eb24ebc702d392fe4449e92e867a884c71faca39ca9e96de4
tools/governance/tests/test_instruction_validator.py
1fc1335d366c1e262e816640e398f3d8297ca098b5ba1e8bb47b1ae8366af4e7
```

Limitações: não executei Rust, scanners, verificação completa, downloads, commits
ou ensaio de modelos. Não examinei como concluída a última edição do plano
canônico nem a futura evidência final. Parsing, revisão textual, fixtures e plano
da CLI não demonstram carregamento efetivo, obediência, desempenho ou custo de
modelos. AC-15 exige a etapa final independente sobre inputs estabilizados.
Consultei software-design e software-testing para responsabilidades/callers e
adequação dos oráculos. Não editei arquivos, conforme limite do perfil revisor.

## Independent focal successor — consumer boundary

The same independent reviewer resumed without implementing changes. Verdict:
**nenhum achado pendente nas fontes finais examinadas**. AC-15 remains dependent
on final stabilized integration. This supplements, rather than rewrites, the
previous review and its intermediate failing observation.

Achado médio AC-10/AC-14, resolvido: agent_errors initially compared only listed
snapshot sources; an extra `unobserved.toml` produced errors=[] in a checkout-like
fixture. The reviewer reproduced that failure. The corrected implementation
compares the complete direct `*.toml` inventory; the same reproduction now gives
`Live agent profile inventory differs from observed snapshot`.

Examined: explicit copy receipt and conflicts; product_record-only exclusions with
predecessor authentication; 14 snapshots, local equality and exact profile inventory;
source/hash/destination/snapshot-exact historical audit link; copy/archive/export
receipt manifests; AC-10 common-contract trace plus live/snapshot oracles; unchanged
docs index successor and exact EOF cleanup.

| Independent method | Observed result |
|---|---|
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools/governance/tests -p 'test_instruction_*.py'` | 43 tests OK, no skips |
| Extra-profile reproduction before/after | Defect detected and correction confirmed |
| Insert excluded product destination into declared copy | Rejected |
| Substitute snapshot with symlink | Rejected |
| Real copy_distribution checkout → copy → recopy in /tmp | Correct receipt; instruction_revision.errors=[] for both |
| Real create_archive, inspection and isolated extraction | Receipt exactly once; digest matches manifest; inventory is manifest plus two receipts; errors=[] after extraction |
| Copy contents | No live .codex/config.toml, .codex/agents, application or .git |
| docs index predecessor | Removing exactly the agent-guide row yields 0f6e901bf9d6c1e351395c9ecf6564433ae1c63dac7c7241a9ef58d7862ed704 |
| Two bridges versus before-format | Exactly one terminal LF removed from each |

Final observed SHA-256:

```text
tools/governance/scripts/instruction_revision.py
c1bc1c8dc5e2963f6ae70d7c6f1459d0be6835d34d6b1d7bd0290b845bf06b44
tools/governance/scripts/governance_support.py
293cbc772469489925246ac5e331f8d6746c145fc56d0f98fa227b8ea0fa132d
tools/governance/scripts/package-ox.py
5c5ce4c9b28a909eb153ff0678b20c85d4f58ef0026548b78d7c65b200614c7d
tools/governance/scripts/export-clean.py
6e74355504d96c8cb9e1ef0c7866bb8fdd625da789988501e3e707a7967180ba
tools/governance/scripts/check-ox.py
b633320d85daa941cf3c399118070aa276613e2c5cd379a1bc5d45ec4d3b33d8
tools/governance/tests/test_instruction_copy.py
99b6384f7e00bfce0d87c7ba9fbdd22aae96638529d9e413fc3b94202bcb0115
tools/governance/tests/test_instruction_routes.py
05aa1cebb1bf014e9796fa693a0c95434c16e81b4340907dee6f55c8f0174c81
sdd/features/configuration-cohesion/traceability.json
75001146ccba92f75ea0d039c909b0597cae7b02ff0eaf5821c1e83ff2c31550
docs/validation/governance-corrections-20261114/agent-snapshot.json
64cf6e670fb2aba45558696fde1b1300ece61a2270e58491cf2eafacd903d21b
docs/validation/governance-corrections-20261114/succession.json
0f5733af045a50631d5a04d897bc526510a14b8c7742bebc02fd1ae5febf0fdd
docs/README.md
1017d9c84faaf46bd79ecd7402915b9d3e7b8e7c73f25c20d4a81cb8a352fa5a
sdd/chain/prompt.md
c541a1843c51e16ad9eba10f765df19bd364a42729fbeae3df4155e85a0c86af
sdd/chain/distributed-systems.md
133628bae27c077fde182dc86b27e74b04133ead524b730b82fd2d0430b4a319
```

Limits: real copy/archive functions and instruction checker were exercised, not
package-ox main or the whole integration suite. No Rust/scanners/downloads/commits/
models. The public receipt declares consumer format; it does not authenticate its
creator. Snapshots are observed evidence, not installed profiles. Reviewer made no
file edits; coordinator records the returned findings and identities here.
