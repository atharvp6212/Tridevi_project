# Reliability architecture

Checkout locks product rows and atomically writes the order, inventory changes,
domain event and outbox event. A client-supplied idempotency key makes safe retry
possible after a timeout. The outbox is committed with the business transaction;
a future worker can publish unprocessed rows and mark them processed only after
acknowledgement.

`grocery/routing.py` supplies an explainable delivery-assignment baseline that
minimizes distance plus a configurable workload penalty. Experiments should
compare it with nearest-only and round-robin strategies using assignment
latency, total travel distance and load variance.
