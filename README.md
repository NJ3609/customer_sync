# Customer Sync & Automation Service

A Phase 1 capstone demonstrating a production-style SaaS integration using:

- FastAPI
- PostgreSQL
- SQLAlchemy
- httpx
- Webhooks
- HMAC signatures
- Pagination
- Retries and exponential backoff
- Rate-limit handling
- Idempotency/deduplication
- pytest
- Docker Compose

## Architecture

```text
Mock AcmeCRM
     |
     | HTTP + Bearer API key
     v
FastAPI Integration Service
     |
     +---- REST API
     |
     +---- Webhook receiver
     |
     +---- CRM client
     |
     v
PostgreSQL
```

## Run with Docker

```bash
docker compose up --build
```

Then open:

- API: http://localhost:8000
- Swagger: http://localhost:8000/docs
- Mock CRM: http://localhost:9000/docs

## Main endpoints

```text
GET    /health
POST   /customers
GET    /customers
GET    /customers/{id}
PATCH  /customers/{id}

POST   /sync

POST   /webhooks/crm
```

## Example

Create a local customer:

```bash
curl -X POST http://localhost:8000/customers \
  -H "Content-Type: application/json" \
  -d '{"external_id":"local-001","name":"John Doe","email":"john@example.com"}'
```

List customers:

```bash
curl "http://localhost:8000/customers?page=1&page_size=20&search=john&sort=name"
```

Run CRM synchronization:

```bash
curl -X POST http://localhost:8000/sync
```

The mock CRM intentionally returns two customers per page so the integration must actually paginate.

## Webhook

Payload:

```json
{
  "event_id": "evt-001",
  "event_type": "order.created",
  "data": {
    "customer_id": "crm-001",
    "amount": 250
  }
}
```

The signature is:

```text
HMAC-SHA256(raw_request_body, WEBHOOK_SECRET)
```

Send it using:

```text
X-Webhook-Signature
```

The service rejects invalid signatures and ignores duplicate event IDs.

## Testing

Install dependencies and run:

```bash
pytest -q
```

## Production improvements

This capstone intentionally stays small. A production deployment would additionally consider:

- Alembic migrations
- structured JSON logging
- Redis for distributed idempotency/rate limiting
- background job queue
- secrets manager
- observability/tracing
- PostgreSQL JSONB instead of generic JSON where appropriate
- connection pool tuning
- authentication/authorization for internal API
- CI/CD
- deployment configuration

## Phase 1 pass condition

Given unfamiliar SaaS documentation, independently identify:

1. Authentication
2. HTTP client design
3. Request/response schemas
4. Pagination
5. Rate limits
6. Retries
7. Webhooks
8. Signature verification
9. Database mapping
10. Idempotency
11. Tests
12. Docker configuration
