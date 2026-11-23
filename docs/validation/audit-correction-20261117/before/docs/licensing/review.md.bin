# OPEN-07 — Análise para decisão do mantenedor

Estado inicial: PENDENTE; análise abaixo preserva as alternativas apresentadas antes da decisão.
Decisão posterior do mantenedor: GPL-3.0-only para material próprio, conforme
[ADR](../decisions/licensing.md), LICENSE e NOTICE da raiz. Rodrigo Batista foi informado pelo mantenedor como
titular do material próprio; os direitos das cópias continuam pendentes. As ADRs de adoção,
externalização, implementação e layout não resolvem OPEN-07. A baseline desta análise ainda não continha
aplicativo Rust nem Cargo.lock. Atualmente existem `application/Cargo.lock` e
os 16 crates em `application/crates/`; o inventário de dependências do bootstrap
é separado desta análise histórica e não concede autorização de distribuição. O aviso nominal agora registra o titular declarado, sem atribuir a ele direitos
sobre materiais de terceiros.

Inspeção local em 27/10/2026: não encontrados LICENSE, COPYING ou NOTICE na árvore
nem nos membros dos archives examinados recursivamente. Foram examinados 153
archives, contando ocorrências aninhadas/repetidas; os marcadores observados estão
em docs/validation/maintenance-001/license-inventory.json. Nomes e marcadores
SPDX/copyright/licensed-under foram pesquisados; isso não é parecer sobre todos os
textos nem prova de ausência de direitos. Cabeçalhos Python locais não apresentam
concessão de licença. A proveniência de cópia em docs/structure/files.json prova
identidade de bytes e origem histórica, não autorização de redistribuição.

| Material | Origem observada | Situação e ação necessária |
| --- | --- | --- |
| Ferramentas próprias de governança, docs e nove especializações autoradas no Ox | Histórico de autoria e revisões locais | Rodrigo Batista, conforme declaração do mantenedor; GPL-3.0-only aplicada ao material próprio |
| Vinte skills copiadas e seus recursos | copy-001 em docs/structure/files.json e baseline de adoção | Obter licença/permissão da origem por versão e manter avisos; licença da raiz não as relicencia |
| SDD 1.3.0, templates, validador e pontes copiadas/adaptadas | Mesmo manifesto e baselines | Confirmar termos da biblioteca de origem e das adaptações |
| skill-quick-validate.py | Cabeçalho de validador mínimo; histórico indica ferramenta upstream | Confirmar origem exata e licença da versão copiada; não presumir termos atuais por semelhança |
| Referências bibliográficas, trechos e exemplos nas skills | portable-sources.md, sources.md e recursos imported | Autores/editoras mencionados não concedem reprodução; revisar extensão dos trechos e permissões quando necessário |
| Logs, respostas de agentes, fixtures e archives | Evidências e baselines locais | Revisar dados/termos aplicáveis antes de publicação; archives carregam as mesmas pendências de seus membros |
| Produto Rust/Iced e futuro SDK | Bootstrap em application/crates/; SDK ainda não implementado | Material próprio sob a decisão vigente; dependências de application/Cargo.lock exigem avaliação própria antes da distribuição |

Proposta: decidir primeiro o objetivo comercial para o material próprio. Se o objetivo
for adoção permissiva e integração com plugins comerciais, considerar Apache-2.0,
com concessão expressa de patentes e obrigações de avisos; MIT é alternativa mais
curta, com preservação do aviso de copyright/licença. Se o objetivo for exigir
reciprocidade na distribuição de obras cobertas, avaliar GPL-3.0 e seu efeito no
modelo de plugins/SDK antes da adoção. Manter uso privado por enquanto também é
uma opção; não rotular a árvore como open source sem concessão aplicável.
Essas são alternativas para decisão, não termos já aplicados.

Fontes públicas consultadas em 27/10/2026 (GNU HTML indisponível no navegador;
texto integral obtido com curl e registrado em license-source.json):
[MIT — OSI](https://opensource.org/license/mit),
[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0),
[GNU GPLv3](https://www.gnu.org/licenses/gpl-3.0.html).
Esses textos descrevem alternativas; não estabelecem direitos sobre os arquivos do Ox.

Decisão de licença própria recebida: GPL-3.0-only. Ainda necessário:
fornecer a base de permissão/licença das cópias; titular próprio registrado como Rodrigo Batista.
ADR, LICENSE, NOTICE e inclusão dos avisos na allowlist já implementados. Após sanar as lacunas,
acrescentar avisos de terceiros/NOTICE quando exigidos pelos termos confirmados,
atualizar documentação/OPEN-07 e acrescentar à allowlist eventuais avisos adicionais exigidos.
Não inventar titular, ano, licença de origem ou permissões ausentes. A escolha da
licença própria sozinha não fecha as pendências de terceiros. Até lá, não há
prontidão declarada para distribuição pública.
