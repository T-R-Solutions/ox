# Message, update, effects

The consulted [Iced 0.14.0 guide](https://docs.rs/iced/0.14.0/iced/) uses state, Message, update and view; update may return Task and subscriptions describe active streams. These names are version-scoped, not a mandate to upgrade a consumer.

Design a search transition: QueryChanged stores text and increments generation; StartSearch emits work tagged with that generation; SearchFinished applies only if generation still matches. Failure becomes an explicit state with retry semantics. A panel being closed should not make a late result mutate a different panel that reused its visual position.

Keep a pure transition table for ordinary tests and an integration test for scheduling. An async function that performs a long synchronous loop may still block its executor. Verify worker choice and cancellation behavior under real load. UI state can display an execution verdict but must not calculate a second acceptance authority from message text.
