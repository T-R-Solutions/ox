# Decisões abertas

As decisões listadas continuam abertas durante a implementação da fundação do
Ox. Antes de adotar uma tecnologia ou ação cujo risco dependa dessas escolhas,
registrar a ADR correspondente, suas alternativas, limitações e critérios.
A abertura da fase de implementação não aprova automaticamente itens PENDENTE,
PROPOSTA ou HIPÓTESE.

| ID | Estado | Decisão / impacto | Retomada |
|---|---|---|---|
| OPEN-01 | PARCIALMENTE DECIDIDO | Linux x86_64 inicialmente, confirmado pelo mantenedor; [ADR bootstrap](product-bootstrap.md) | X11 exercitado; Wayland nativo, outros SO/FS/GPU e isolamento aguardam validação |
| OPEN-02 | DECIDIDO PARA BOOTSTRAP | stable, edição 2024, piso 1.99; Iced 0.14.0 com tiny-skia e thread-pool; [ADR](product-bootstrap.md) | Rever runtime quando houver I/O externo; lockfile em application |
| OPEN-03 | PROPOSTA | Processo externo/IPC versionado, JSON-RPC, ACP | Escolher protocolo/transportes e agentes após verificar versões/capabilities reais; sem ABI ou sandbox presumidos |
| OPEN-04 | PENDENTE | Primeiros agentes, rede, segredos e graus de autonomia | Definir adaptadores e grants; distinguir mediação do host de ferramentas diretas |
| OPEN-05 | PROPOSTA | SQLite, FTS5, formato de grafo, backup e retenção | Comparar alternativas com workload, recuperação e política de dados |
| OPEN-06 | PENDENTE | Sandbox por plataforma e plugins confiáveis | Modelo de ameaças e testes de efeitos negados em SO alvo |
| OPEN-07 | PARCIALMENTE DECIDIDO | GPL-3.0-only para material próprio conforme [ADR](licensing.md); titular próprio Rodrigo Batista; termos de terceiros, distribuição, assinatura, atualização e SDK ainda pendentes | Confirmar direitos por origem antes de publicar; software-delivery cobre o método |
| OPEN-08 | PENDENTE | Metas de CPU/RAM/latência, corpus e acessibilidade | Spike/benchmark autorizado com hardware fixado; nenhum número adotado agora |
| OPEN-09 | PENDENTE | Parsers, linguagens prioritárias, C/FFI transitivo | Auditar dependências; first-party Rust é definido, ausência absoluta de C não foi imposta |
| OPEN-10 | HIPÓTESE | Embeddings, nuvem opt-in, marketplace e economia de tokens | Avaliação comparativa futura; fora do escopo inicial de `product-foundation`, salvo decisão SDD posterior explícita |
| OPEN-11 | PENDENTE | UX de aprovação, idiomas, multijanela, layout final | Validar com usuários/targets e manter arquivos SDD como autoridade |

Uma proposta ainda não aprovada não concede permissões. A implementação local
do produto exige feature e escopo autorizados; dependências, agentes externos,
transmissão de código, gastos, operações destrutivas e publicação continuam
sujeitos às permissões efetivas e às decisões aplicáveis.
