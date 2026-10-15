# Limitations

- Real concurrency evaluation requires PostgreSQL; SQLite ignores row locks.
- The outbox publisher and external message broker are not included.
- Idempotency clients must provide stable, unpredictable keys.
- Euclidean coordinates are a controlled baseline, not road-network distance.
- Payment and delivery integrations are simulated and not production services.
