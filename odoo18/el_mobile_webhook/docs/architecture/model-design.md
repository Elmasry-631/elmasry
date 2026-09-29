# Model Design

`mobile.webhook.event` stores an immutable JSON payload, delivery state, retry metadata, and company. Source business models only override `write` to enqueue transitions.