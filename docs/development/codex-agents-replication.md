# Adaptação dos agentes Ec para o Ox

Esta instalação usa a configuração e os treze TOMLs do projeto Ec inspecionados
em 14/11/2026, além dos guias `docs/development/codex-agents.md` e
`docs/development/codex-agents-replication.md` daquele checkout. O Ec foi somente
lido. Esta referência registra proveniência; operar no Ox não requer acesso ao Ec.
A [matriz e o procedimento comum](codex-agents.md) são a fonte de uso dos perfis.

## Mapa adotado

| Fonte Ec | Destino/contrato Ox |
| --- | --- |
| `.codex/config.toml` | Mesmo caminho; controlador Sol médio e execução proporcional pelo procedimento comum |
| `.codex/agents/*.toml` | Mesmos 13 nomes `ec_*`; validadores adaptados ao aceite Ox |
| `docs/development/codex-agents.md` | Mesmo caminho; autoridades e verificação locais |
| `task-verification.md` e `scripts/accept-task.sh` | `sdd/evidence.md`, checker `sdd/tools/validate.py` e parecer manual na rota local |
| `local-state.md` | `docs/development/local-artifacts.md` |
| Autoridades e comandos Ec | AGENTS, projeto, constituição, arquitetura, ADRs e scripts reais do Ox |

Nenhum runner, gate, recibo, skill, permissão histórica ou arquivo de produto Ec
foi importado. Os perfis não configuram o runtime Rust nem alteram a política de
sandbox. O perfil versionado de skills é separado da configuração de agentes.
A allowlist de exportação de governança permanece inalterada; a adoção é deste
checkout. Uma réplica precisa copiar explicitamente a configuração e os perfis,
além do guia e das autoridades locais necessárias.

## Nova sessão e diagnóstico

Na raiz do Ox, inicie `codex --strict-config`. Confirme que o cliente carrega a
configuração do projeto confiável e os perfis. Políticas administradas e opções
explícitas podem prevalecer. Alterações em disco não trocam o modelo da conversa
já aberta. A CLI observada nesta instalação é `codex-cli 0.169.0`.

A raiz é o controlador e faz triagem sem assumir o papel restrito do especialista
`ec_triador` delegado, que permanece somente leitura e sem filhos. A
[política de execução](codex-agents.md#entrada-triagem-e-continuidade) admite
leitura/diagnóstico e reparo local claro, recuperável e sem risco material nas
condições do workflow. Risco material exige `ec_orquestrador_alta`, revisão e
validação independentes; capacidade ausente bloqueia sua etapa dependente.
Instruções expressas do usuário e limites do host prevalecem. Três threads de subagentes mais a raiz
permitem quatro nós, normalmente raiz + orquestrador + dois especialistas.
O [preflight](codex-agents.md#preflight-de-capacidades-e-vagas) trata limites,
contextos independentes, liberação de vagas e retomada.

| Problema | Conferência |
| --- | --- |
| Perfil não reconhecido | Caminho, TOML, campo `name`, descoberta e confiança do projeto em nova sessão |
| Modelo/esforço rejeitado | Capacidade da conta/cliente; não substituir silenciosamente nem afirmar equivalência |
| Escrita em `.codex` protegida | Preparar alteração revisável e usar autorização específica do ambiente |
| Vaga não liberada | Conferir estado real; interrupção não comprova liberação |
| Comando de verificação ausente | Conferir autoridades Ox; não usar comando Ec nem simular resultado |

## Conferência estrutural reproduzível

Da raiz, Python 3.11+ verifica os arquivos sem chamar modelos:

```bash
python3 - <<'PY'
from pathlib import Path
import tomllib
root = Path.cwd()
config = tomllib.loads((root / '.codex/config.toml').read_text())
files = sorted((root / '.codex/agents').glob('*.toml'))
assert len(files) == 13
names = set()
for path in files:
    agent = tomllib.loads(path.read_text())
    assert agent['name'] == path.stem and agent['name'] not in names
    names.add(agent['name'])
    for key in ('description', 'model', 'model_reasoning_effort', 'developer_instructions'):
        assert isinstance(agent[key], str) and agent[key].strip()
    assert 'docs/development/codex-agents.md' in agent['developer_instructions']
assert config['agents']['enabled'] is True
assert config['agents']['max_concurrent_threads_per_session'] == 3
assert (root / 'docs/development/codex-agents.md').is_file()
print('13 perfis conferidos; estrutura não comprova execução dos modelos.')
PY
```

Confira também a matriz, links e instruções dos validadores. Carregamento pelo
cliente, criação por perfil, modelo/esforço efetivo e ensaio completo da equipe
são verificações distintas. A instalação não demonstra eficácia, custo ou latência.
O [registro da instalação original](../validation/codex-agents-20261114/report.md)
preserva seus resultados e limites sobre aqueles inputs. O sucessor aprovado em
14/11/2026 é a [reconciliação de instruções](../decisions/governance-instruction-reconciliation.md);
as observações novas ficam no [relatório da correção](../validation/governance-corrections-20261114/instruction-implementation.md).
Revisão textual, parsing e testes de plano não demonstram obediência ou eficácia
dos modelos nem reconfiguram a sessão em andamento.
