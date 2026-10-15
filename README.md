# Scalable Multi-Service Ordering and Marketplace Platform

A Django marketplace that connects customers with restaurant and grocery-store
owners. It includes role-specific dashboards, catalogues, reviews, ordering and
order-management workflows.

## Reliability upgrade

Grocery checkout now runs inside a database transaction. Requested product rows
are locked with `select_for_update`, stock is validated before any writes occur,
and order creation, line-item insertion and inventory reservation commit as one
unit. Invalid cross-store products and insufficient stock are rejected without
leaving partial orders behind.

Retries can now carry an idempotency key, and each successful checkout records
both an immutable order event and a transactional outbox event. An explainable
distance-and-workload delivery-assignment baseline is included for experiments.

This design demonstrates an important systems property: concurrent requests
must preserve inventory invariants, not merely succeed individually.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py test
python manage.py runserver
```

## Evaluation roadmap

- Concurrent checkout tests on PostgreSQL
- Indexed search and cache hit-rate measurements
- Delivery assignment strategies and workload balance
- Load testing with latency percentiles and database-query counts

See `ARCHITECTURE.md` for the failure model and `LIMITATIONS.md` before drawing
production conclusions.
