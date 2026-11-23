# Métricas de auditoria (M01–M20)

Escala por métrica, aplicada à task em análise (`.ai/task_planning.md`):

| Nota | Significado |
|---|---|
| 4 | Exemplar: sem achados; nada razoável a melhorar |
| 3 | Bom: só achados baixos/info |
| 2 | Aceitável com ressalvas: ao menos um achado médio |
| 1 | Insuficiente: achado alto, ou vários médios no mesmo tema |
| 0 | Inaceitável: achado crítico, ou alegação material falsa |
| N/A | Não se aplica — escreva o porquê em uma linha |

Toda nota < 4 cita ao menos uma correção (`C<n>`). Nota sem evidência é proibida.
A **nota global** da task é a média das métricas aplicáveis, mas o veredito é limitado
pelo pior achado (um crítico reprova mesmo com média alta).

Severidade dos achados:

| Severidade | Critério |
|---|---|
| crítica | perda/corrupção de dados, falha de segurança explorável, gate de aceite falso, comportamento oposto ao contrato |
| alta | defeito funcional real em caminho usado; teste que não protege o que afirma; alegação de verificação falsa |
| média | defeito em caminho raro; lacuna de teste de caminho infeliz relevante; fragmentação/legado que já gera divergência |
| baixa | legibilidade, nome, duplicação pequena, documentação imprecisa sem impacto operacional |
| info | observação, elogio fundamentado, sugestão opcional |

---

## Obrigatórias (pedido do mantenedor)

### M01 · Correção da lógica
A implementação faz o que a spec/pedido exige em todos os estados?
- Leia o fluxo de controle alterado; trace entradas válidas, vazias, limites, inválidas.
- Off-by-one, comparação de tempo/fuso (ex.: janelas de 12h/24h), arredondamento,
  Unicode, ordenação, precedência de operadores, `set -e`/`||` em shell, retorno
  ignorado, estado mutável compartilhado, early return que pula limpeza.
- Rust: `unwrap/expect` em entrada do usuário, overflow, `match` com `_` engolindo
  variante nova, clones que mascaram aliasing, estado de UI dessincronizado da fonte.
- Confirme com experimento sempre que possível (`✔ exp`).

### M02 · Alternativa mais correta
Existia solução mais simples, robusta, idiomática ou já presente no código?
- Procure utilitário existente que foi reimplementado.
- Compare com a prática da linguagem (Iced: `Task`, `Subscription`, widgets nativos;
  shell: função única com `main`; Python: stdlib antes de parsing manual).
- Só registre se a alternativa for **concretamente** melhor; descreva o trade-off.

### M03 · Trabalho testado
Cada mudança de comportamento tem teste ou verificação que a exercita?
- Monte a matriz: função/arquivo alterado → teste que o executa (grep do nome, leitura).
- Mudança sem teste: diga se a verificação manual/nativa registrada é suficiente.
- Rode a suíte; compare contagem/exits com o que o Codex alegou.

### M04 · Qualidade e amplitude dos testes
- Caminho feliz **e** infeliz (erro de I/O, entrada inválida, cancelamento, timeout,
  permissão, arquivo ausente, concorrência), bordas e combinações relevantes.
- O oráculo é independente da implementação? (Fixture feita à mão que não
  corresponde à saída real é falso positivo.)
- Sensibilidade: o teste falharia se a correção fosse revertida? Se possível, reverta
  em cópia e rode (`✔ exp`). Asserts fracos (`assertIn` de string, `exit != 0`
  genérico, `assert!(result.is_ok())` sem conteúdo) baixam a nota.
- Testes `#[ignore]`/skip: há justificativa e execução registrada?
- Flakiness: dependência de tempo real, ordem, rede, display.

### M05 · Fragmentação
- Mesma regra implementada em 2+ lugares (shell e JSON, Rust e doc, teste e código).
- Arquivo/função monolítica que cresceu (ex.: `views.rs` com centenas de linhas
  novas) ou, ao contrário, fragmentação em módulos minúsculos sem coesão.
- Estado global/escopo dinâmico usado como canal entre funções.
- Diretórios de evidência por task que duplicam o mesmo conteúdo.

### M06 · Legado, morto, depreciado
- Código antigo mantido ao lado do novo; flags/ramos de compatibilidade sem prazo
  ou ADR; funções sem chamador; `#[allow(dead_code)]`; comentários “legacy/old/v1”.
- Tratadores inalcançáveis (`x=$y || fail`), constantes não usadas, campos sempre
  constantes, scripts sem chamador em produção.
- API/dependência depreciada (avisos do compilador, `DeprecationWarning`, crate yanked).

---

## Complementares (nível enterprise)

### M07 · Aderência ao escopo autorizado
Compare o diff com a seção correspondente de `sdd/project.md`/spec. Mudança fora do
escopo, escopo entregue parcialmente, ou critério enfraquecido para caber.

### M08 · Veracidade das alegações
Cada afirmação do relatório do Codex (“N testes passaram”, “revisão independente”,
“hash X”, “sem impacto documental”) confere com a realidade? Reexecute, recalcule
hashes por amostragem, confira se logs citados existem. Alegação falsa material = 0.

### M09 · Governança SDD e fechamento
Rota correta (local vs. completa) pela matriz de risco; cinco estados usados
corretamente; evidência schema 2 com inputs reais; disposição documental registrada;
entrada em `task_finalizada.md` presente, completa e append-only; revisão/validação em
contexto independente quando exigido. Ver [governança Ox](ox-governance.md).

### M10 · Tratamento de erros e resiliência
Falhas propagam com causa útil? Recuperação preserva dados (POL-05)? Limpeza em
falha (trap, Drop, finally)? Mensagens de erro alcançáveis e corretas?

### M11 · Segurança
Injeção de comando (quoting em shell, `subprocess` com shell=True), path traversal,
symlinks, permissões de arquivo, segredos em logs/evidências, supressões amplas de
scanner (`nosec`, baselines, ignores), `unsafe` (proibido por POL-01), entradas não
confiáveis tratadas como instruções.

### M12 · Compatibilidade e contratos
Mudou formato de arquivo, CLI, saída, schema, API pública ou atalho de teclado? Os
consumidores foram atualizados? Há quebra silenciosa para dados existentes?

### M13 · Desempenho e eficiência
Complexidade algorítmica, processos por arquivo, I/O repetido, alocação em loop de
render (Iced `view` chamado a cada frame), clones grandes, recomputação evitável.
Só afirme regressão com medição ou cálculo explícito (`estimativa`).

### M14 · Manutenibilidade e legibilidade
Tamanho de função, aninhamento, nomes, números mágicos, comentários que explicam o
porquê, consistência com convenções do crate/script. Duplicação de literais de UI.

### M15 · Documentação
README/DESIGN/surfaces/ADRs refletem o comportamento real? Comandos documentados
funcionam? Links locais resolvem? Excesso de prosa que obscurece o contrato.

### M16 · Observabilidade e diagnóstico
Logs/saídas permitem diagnosticar falha? Exit codes distintos? Saída compacta
preserva sinal de falha e caminho do bruto (POL-08)?

### M17 · Integridade e concorrência
Escritas atômicas, detecção de alteração concorrente antes de sobrescrever (POL-05),
corrida entre processos, estado de UI vs. tarefa em background, cancelamento.

### M18 · UX e acessibilidade (tasks visuais)
Aderência a `DESIGN.md`/surfaces e à baseline Visual Studio 2026 Enterprise;
navegação por teclado, foco visível, tooltips reais, contraste (`check_contrast.py`),
redimensionamento, estados vazio/erro/carregando, textos em pt-BR consistentes.

### M19 · Dependências e licenças
Crates/pacotes novos ou atualizados: necessidade, licença, `Cargo.lock` coerente,
features mínimas, fontes/ativos com proveniência (`NOTICE`, `font-provenance.json`).

### M20 · Proporcionalidade e higiene do diff
Volume de artefatos proporcional ao risco (milhares de linhas de evidência para uma
mudança pequena é custo de revisão); arquivos gerados/caches/binários no diff
(`__pycache__`, `.pyc`, `.log` fora do `.gitignore`); mudanças não relacionadas
misturadas; arquivos alterados que `task_completed.md` não cita (órfãos).
