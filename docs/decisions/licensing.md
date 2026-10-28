# ADR — Licença do material próprio

Estado: decisão do mantenedor registrada em 27/10/2026; implementação parcial,
com permissões de terceiros pendentes. Titular informado pelo mantenedor: Rodrigo Batista. Resposta recebida: “GLP-3.0”,
interpretada no contexto das opções apresentadas como GPL-3.0 e comunicada ao mantenedor.

Adotar GNU GPL versão 3 somente (GPL-3.0-only) para as contribuições próprias do Ox.
Não acrescentar a permissão “ou posterior” nem exceção de ligação de plugins sem
nova decisão. LICENSE contém o texto integral obtido de
https://www.gnu.org/licenses/gpl-3.0.txt; hash e método em license-source.json
no registro maintenance-001. NOTICE delimita escopo e materiais excluídos.

Motivo: preferência expressa do mantenedor dentre as alternativas permissivas,
copyleft e adiamento documentadas na análise. MIT e Apache-2.0 não foram escolhidas.
A decisão sucede somente a pendência de escolha da licença própria em OPEN-07 e
na ADR maintenance-001; não resolve direitos de terceiros, distribuição, assinatura,
atualização ou SDK. As demais políticas e permissões continuam válidas.

Em confirmação posterior, o mantenedor informou “Titular - Rodrigo Batista” e
reiterou a licença. Registrar Copyright (C) 2026 Rodrigo Batista no NOTICE para
o material próprio, conforme autoria local de 2026. A declaração não atribui
direitos sobre cópias: obter termos por origem/versão dos materiais copiados. Uma GPL na raiz não os relicencia. A futura arquitetura de SDK/plugins
precisa considerar os termos e dependências reais antes de distribuir; nenhum
modelo de compatibilidade foi aprovado aqui.

Revisão da allowlist: incluir LICENSE e NOTICE nos dois meios de compartilhamento,
por pasta ou futuro pacote; manter exclusão de dist e fontes futuras do aplicativo.
Testes devem exigir esses avisos no conteúdo exportável. Nenhum pacote da solução
é produzido nesta tarefa. Revisar esta ADR se mudar escopo, versão, modelo de plugins,
identificação de titular ou permissões dos componentes copiados.
