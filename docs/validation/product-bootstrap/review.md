# Revisão do bootstrap

16 bibliotecas com módulos externos e raiz forbid(unsafe_code); binário ox delega à biblioteca startup. Apenas app -> ui e ui -> iced são dependências de produção entre composição/GUI. Demais contratos não se interligam artificialmente. Cargo verifica grafo acíclico; inspect.py compara a lista exata e limites.

ox-core: disponibilidade não autoriza execução. agent: estados/capacidades/erros, sem adaptador. plugin: versão requerida aceita major igual e minor suficiente (teste negativo), nenhum host/transporte. policy: default ApprovalRequired, Grant representa decisão e não executor. task: transições validadas, término não reinicia. workspace: path absoluto encapsulado, sem existência ou sandbox presumidos. storage: local/erros, nenhum banco. context: limite não zero, proveniência, erro IndexUnavailable. graph: evidência verificada/inferida explícita. output: bytes brutos, término e captura incompleta preservados no contrato, sem compactador. verification: default NotVerified. observability: desconhecido distinto de zero, método/origem/unidade/período. sdd: artefatos de projetos de usuários. skills: seleção não executa. Esses modelos não validam conteúdo arbitrário de manifestos externos e não constituem APIs wire estáveis.

Não existem entidades persistentes globais, serialização ou importação de UUID: testes de UUID v7 não se aplicam nesta fatia. WorkspaceRoot e NodeKey não são intercambiáveis por tipo. Nome de plugin permanece ID de domínio. Futuros IDs persistentes devem ter validação e testes próprios antes do uso.

Capturas collapsed.png e expanded.png examinadas: título Ox, indicador F0, botões mostrar/ocultar, detalhes de indisponibilidade e Sair legíveis. Log desktop comprova mensagens por entrada gráfica, diferenças de pixels, reversão e retornos zero. Não estabelece acessibilidade, latência universal nem Wayland nativo.

Produto não integra dist nem exportações de governança. O teste de allowlist exige ausência de application e registros dependentes do produto; o restante da governança é executado em cópia independente. Archives existentes não foram regenerados.
