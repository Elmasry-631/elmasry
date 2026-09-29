# Design

The intentional design is operationally boring: persistent queue, Settings, scheduled delivery, and visible failures. Receiver-side idempotency makes at-least-once delivery safe.