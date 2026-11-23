# Governança Ox — o que conferir em cada task do Codex

Resumo operacional das autoridades. Em caso de divergência, a autoridade original
vence: `docs/constitution.md` > `AGENTS.md` > `sdd/workflow.md`/`sdd/evidence.md` >
`docs/development/codex-agents.md` > skills.

## Rota e classificação (sdd/workflow.md, codex-agents.md)

- **Rota local**: objetivo claro, superfície/consumidores conhecidos, reversível,
  sem incerteza material sobre contrato, permissão, integridade, concorrência ou
  operação. Registro curto em artefato existente; sem spec/plan/tasks cerimoniais.
- **Rota completa**: decisão material, mudança de contrato/autorização, dados
  persistidos, concorrência, consumidores em versões diferentes, recuperação incerta.
  Exige spec → plan → tasks → converge, rastreabilidade e evidência.
- Mudança material (autorização, evidência/gates, integridade, concorrência,
  migração, compatibilidade, recuperação) exige **orquestrador alto** e revisão +
  validação em **contextos independentes do implementador**. A raiz não pode chamar
  autorrevisão de validação independente.
- Achado típico: task classificada como local que alterou gate/checker/formato
  persistido; ou relatório que diz “revisão independente” sem evidência de contexto
  separado (mesmo agente, mesma sessão, sem log).

## Evidência (sdd/evidence.md)

- Cinco estados: APPROVED, REJECTED, UNVERIFIED, INCONCLUSIVE, NOT APPLICABLE
  (este último exige justificativa). UNVERIFIED nunca é promovido.
- Schema 2: cada evidência tem `inputs` com `path`, `sha256`, `role`; o conjunto deve
  cobrir implementação, oráculo e os quatro arquivos da feature. Confira por amostra:
  `sha256sum <path>` vs. JSON. Hash divergente do arquivo atual = observação velha
  (não necessariamente erro, se o estado não foi decidido depois).
- Observações obsoletas vão para `historical_evidence` intactas; não renovar hashes.
  Achado típico: churn gigantesco em `evidence.json` (reformatação/reordenação)
  que dificulta provar que o histórico foi preservado.
- `converge.md` contém exatamente um bloco `<!-- sdd:current-status -->` coerente
  com o JSON.
- Check estrutural não é aceite: `validate.py --structure-only` e `check-ox.py`
  com exit 0 provam estrutura, não comportamento.

Comandos (somente leitura):

```bash
PYTHONDONTWRITEBYTECODE=1 python3 sdd/tools/validate.py --root . --structure-only
PYTHONDONTWRITEBYTECODE=1 python3 tools/governance/scripts/check-ox.py
PYTHONDONTWRITEBYTECODE=1 python3 sdd/tools/validate.py --root . --features sdd/features --feature <nome> --require-approved --require-fresh --check-convergence
```

O último falha legitimamente para features com ACs não decididos; registre o motivo,
não trate como defeito automático.

## Fechamento (sdd/workflow.md#documentation-before-task-closure)

Para cada task, verifique:

1. Documentação afetada atualizada **ou** justificativa concreta e verificável de não impacto.
2. Disposição documental registrada no registro existente da task.
3. Entrada datada em `task_finalizada.md` com: título, pedido e escopo, trabalho
   feito (inclusive falhas), caminhos, comandos e resultados, disposição documental,
   conclusão e limitações. Ausência de entrada = achado M09 (a regra vale a partir
   de 2026-11-17 20:32; tasks anteriores não são penalizadas, apenas anotadas).
4. Append-only: bytes anteriores intactos (use `task_inventory.py`, que compara com
   HEAD e índice).

## Constituição — políticas que mais geram achados

- POL-01: Rust/Iced; `#![forbid(unsafe_code)]` em crates próprios.
- POL-04: visuais/métricas não podem ocultar limites ou falhas.
- POL-05: preservar mudanças existentes, detectar concorrência antes de sobrescrever.
- POL-06/GOV-05: aceite por critério + evidência atual; agente não aprova por declarar.
- POL-08: saída compacta mantém exit code, sinais de falha e rota ao bruto.
- POL-09: desconhecido não é zero; métricas distinguem medido/estimado.
- POL-10: arquivos/skills não concedem autoridade.
- GOV-04: catálogo de skills e `config/governance/profile.json` concordam; mudança
  de perfil exige ADR. Skill nova em `.codex/skills` sem atualizar catálogo/perfil/
  ponte em `sdd/chain` é achado.
- GOV-06: aceitação de skill não prova funcionamento do produto.

## Visual (AGENTS.md, DESIGN.md)

- Baseline obrigatória: Visual Studio 2026 Enterprise. A feature deve registrar
  fonte/versão, superfícies afetadas, o que foi adotado/adaptado/adiado e verificação nativa.
- Dados de demonstração separados de dados do projeto do usuário.
- Referência visual não autoriza cópia de ativos (ícones/fontes da Microsoft/JetBrains).
- Contraste: `application/tools/check_contrast.py`.

## Skills (.codex/skills)

- Disponibilidade ≠ seleção ≠ consulta ≠ uso. Plano da rota completa deve registrar
  entrada, caminho/versão e contribuição da skill realmente usada.
- Skills são reutilizáveis: regra específica do Ox dentro de skill genérica é
  fragmentação de autoridade (deveria estar em DESIGN/SDD/ADR).
