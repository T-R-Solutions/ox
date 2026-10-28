# Fronteiras de confiança a verificar

Este registro aplica a [constituição](../constitution.md) sem criar política concorrente. AGENTS, pontes e skills são orientação; não implementam contenção.

| Fronteira | Evidência necessária no consumidor | Estado verificado na baseline / atualização |
|---|---|---|
| Plugin → host | Negociação, autorização, efeitos recusados e crash | NÃO VERIFICADO: sem host |
| Processo → SO | Negação de filesystem/rede/segredos fora do grant, inclusive bypass de IPC | NÃO VERIFICADO: plataforma/sandbox pendentes |
| Agente → workspace | Base hash, conflitos, escape de path e recuperação | NÃO VERIFICADO: sem runtime |
| Logs/arquivos/contexto → agente | Conteúdo preservado como dado, sem ampliar autoridade | Revisão documental; proteção operacional futura |
| Agente → provedor remoto | Escopo de transmissão, consentimento e capacidades do adaptador | NÃO VERIFICADO: agentes pendentes |
| Implementação → veredicto | Oráculo e inputs atuais, independente da declaração do agente | Modelo local disponível; produto ausente |

Os estados acima referem-se à baseline de governança. Cada controle de produto
somente poderá mudar de NÃO VERIFICADO mediante evidência de integração
ou teste adversarial do componente e plataforma correspondente, vinculada
à feature `product-*` e ao snapshot real. Autorizar desenvolvimento
não equivale a demonstrar sandbox, isolamento ou segurança do runtime.

Retomada: escolher consumidor e SO, delimitar dados descartáveis/autorização, instanciar os casos das respectivas skills e registrar efeitos reais com snapshots. Não usar mocks como prova de sandbox. Retenção/redação do bruto devem preservar evidência autorizada sem expor segredos nas visões compactas.
