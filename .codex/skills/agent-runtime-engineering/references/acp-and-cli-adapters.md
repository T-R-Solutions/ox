# ACP and CLI adapters

The consulted [ACP initialization v1](https://agentclientprotocol.com/protocol/v1/initialization) negotiates version and capabilities; use the schema matching the observed peer. The documentation also exposes a v2 draft: do not mix its messages with a v1 adapter. No agent executable/version is selected by this skill.

For [ACP cancellation](https://agentclientprotocol.com/protocol/v1/cancellation), distinguish sending a cancellation notification from observing the turn stop. Preserve events already in flight. Cancellation is not a rollback of filesystem effects.

For a plain CLI, prefer documented machine output. If only terminal text exists, expose a narrower adapter with explicit uncertainty: process started/exited can be observed, semantic completion may not be. Persist raw streams and invocation configuration without secrets. Compare declared support, negotiated support and tested support in separate columns. A CLI able to run tools directly may bypass host mediation; document that boundary before enabling execution.
