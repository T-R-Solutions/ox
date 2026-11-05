---
name: plugin-protocol-engineering
description: Design and verify versioned host-plugin protocols, capability negotiation and lifecycle failure boundaries. Use for plugin hosts or compatibility changes; skip clients of an unchanged SDK.
---

# plugin-protocol-engineering

## Responsabilidade e seleção

Projetar e verificar protocolos versionados de plugins isolados do host, incluindo negociação de capacidades, permissões, ciclo de vida, falhas, ABI e compatibilidade.

Selecionar: Novo protocolo/plugin host, manifest de capacidades, IPC, compatibilidade vN/vN+1, instalação/desinstalação segura.

Não selecionar: Não selecionar para um plugin de lint que apenas utiliza SDK já estabilizado; nesse caso, aplicar Rust e API Testing. Não converter a skill em recomendação automática de Wasm, gRPC ou Dylib.

## Entradas e lacunas

políticas de extensibilidade, modelo de ameaças, operações/capacidades, matriz de versões, SO, recursos disponíveis.

Inspecione os contratos e recursos reais antes de executar. Ausência de versão exige consulta à documentação correspondente; ausência de permissão impede o efeito dependente. Registre a lacuna, seu impacto e como resolvê-la, continuando partes independentes. Os exemplos deste pacote são contratos de avaliação, não APIs ou políticas impostas a todos os consumidores.

## Procedimento operacional

1. Inventory each operation as a tuple: caller identity, requested capability, granted scope, input limit, effect, idempotency rule and revocation point. Separate host-mediated effects from direct process access; an allowlist in a manifest cannot constrain the latter.

2. Write a negotiation transcript before implementation. Define transport framing, maximum frame size, protocol version ranges, unknown fields, request correlation and error ownership. Compute effective capabilities as the supported/requested/granted intersection; never grant a capability merely because both binaries implement it.

3. Compare out-of-process RPC, in-process ABI and a restricted runtime against the actual trust model. Record which failure each option contains, platform mechanisms required and what remains trusted. Do not default to Wasm, gRPC or dynamic libraries.

4. Define lifecycle transitions from discovery through negotiation, ready, draining and stopped/failed. Admission closes before shutdown; in-flight requests either finish or expire under a documented policy. Reconnect creates a new instance generation, so old replies cannot satisfy new requests.

5. Build a compatibility matrix by host version, plugin version and capability subset. Exercise successful negotiation, denied capability, malformed frame, oversized payload, crash mid-effect and timeout. Inspect persistent state and protected-file effects, not just the error response.

6. Deliver a protocol contract, denied-effect matrix, lifecycle transcript and platform-specific residual risks. Treat a successful mock as protocol evidence only; isolate and test a real untrusted plugin before claiming sandbox enforcement.

## Entregáveis e aceitação

contrato de mensagens, estados do host, modelo de permissões, limites de recursos, matriz compatível, testes de falhas e migração.

Vincule cada conclusão a input observado, método, resultado e limite. Execute casos esperados, de borda e de falha de [avaliações](references/evaluation-cases.md) no ambiente autorizado; diferencie resultado de revisão, simulação e integração. Casos apenas escritos continuam não executados. O texto da skill não prova eficácia nem concede autoridade.

## Fronteiras e encaminhamento

`application-security` — O isolamento escolhido realmente impede os efeitos não autorizados de um plugin comprometido?

Encaminhe somente a pergunta técnica distinta ainda não resolvida, com escopo, IDs de critérios, fatos, lacunas e evidência requerida. Confirme disponibilidade antes da consulta. Uma menção não instala, delega, executa nem carrega recursivamente outras skills. A autoridade de comportamento pertence ao contrato do consumidor; a skill oferece o método.

## Referências especializadas

- [protocol-negotiation](references/protocol-negotiation.md): consultar para Negotiation and message identity.
- [permissions-and-isolation](references/permissions-and-isolation.md): consultar para Mediated permissions and containment.
- [versioning-and-faults](references/versioning-and-faults.md): consultar para Compatibility and failure windows.

Fontes oficiais acessadas em 2026-10-26 são citadas junto às afirmações. Versão consultada não é versão adotada pelo consumidor. Sínteses operacionais e esquemas de exemplo são decisões de método desta skill, sem promessa de implementação ou compatibilidade futura.

## Responsabilidades adjacentes

A competência própria acima não substitui os métodos gerais abaixo. Consultar apenas quando a questão correspondente permanecer aberta; nenhum encaminhamento é obrigatório.

| Competência | Autoridade técnica adjacente |
|---|---|
| `api-testing` | verificação de protocolos, efeitos, permissões e compatibilidade entre consumidores |
| `application-security` | fronteiras de confiança, segredos, autorizações e ameaças |
| `reliability-engineering` | falhas, cancelamento, limites, degradação, recuperação |
| `software-architecture` | fronteiras, integração, atributos de qualidade, adrs |
| `software-evolution` | compatibilidade, migrações, coexistência e versões antigas |
| `distributed-systems` | garantias entre domínios de falha e versões, mensageria/consistência |
| `rust` | ownership, crates, concorrência, compatibilidade, validação rust |
| `software-delivery` | supply chain, builds, assinaturas, release e rollback |
| `software-design` | interfaces, coesão, acoplamento, refatoração localizada |
