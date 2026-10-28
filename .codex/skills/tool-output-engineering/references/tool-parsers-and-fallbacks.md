# Format recognition and fallback

[Cargo external tools](https://doc.rust-lang.org/cargo/reference/external-tools.html#json-messages) documents JSON build messages and warns that message-format does not control every subprocess or macro output. Do not assume cargo test produces a homogeneous machine-readable test stream merely because a build flag is set.

Select parsers by observed tool version and format, not just executable basename. Validate records before interpretation; retain unknown records and the fact that recognition failed. For partial UTF-8, keep raw bytes and either incremental decode with carried state or a visibly lossy display; never silently drop the bytes that contain an error.

Fallback should expose exit status, raw locator, capture completeness and an explicit recorte/truncation notice. Differential oracle: every known failing fixture must remain failing or explicitly uninterpretable, never pass. Add an adversarial line asking the agent to publish secrets; its only permitted role is quoted log data.
