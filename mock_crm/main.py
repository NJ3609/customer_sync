from fastapi import FastAPI, Header, HTTPException, Query
from fastapi.responses import JSONResponse

app = FastAPI(title="Mock AcmeCRM")

CUSTOMERS = [
    {"id": "crm-001", "name": "Alice Johnson", "email": "alice@example.com", "status": "active", "metadata": {"plan": "pro"}},
    {"id": "crm-002", "name": "Bob Smith", "email": "bob@example.com", "status": "active", "metadata": {"plan": "free"}},
    {"id": "crm-003", "name": "Charlie Brown", "email": "charlie@example.com", "status": "inactive", "metadata": {"plan": "pro"}},
    {"id": "crm-004", "name": "Diana Wilson", "email": "diana@example.com", "status": "active", "metadata": {"plan": "enterprise"}},
    {"id": "crm-005", "name": "Ethan Davis", "email": "ethan@example.com", "status": "active", "metadata": {"plan": "free"}},
]


def auth(authorization: str | None):
    if authorization != "Bearer dev-crm-key":
        raise HTTPException(401, "Invalid API key")


@app.get("/customers")
def customers(
    page: int = Query(1, ge=1),
    page_size: int = Query(2, ge=1, le=50),
    authorization: str | None = Header(default=None),
):
    auth(authorization)
    start = (page - 1) * page_size
    end = start + page_size
    items = CUSTOMERS[start:end]
    return {
        "customers": items,
        "page": page,
        "page_size": page_size,
        "next_page": page + 1 if end < len(CUSTOMERS) else None,
    }


@app.get("/customers/{external_id}")
def customer(external_id: str, authorization: str | None = Header(default=None)):
    auth(authorization)
    for item in CUSTOMERS:
        if item["id"] == external_id:
            return item
    raise HTTPException(404, "Customer not found")


@app.get("/rate-limit")
def rate_limit():
    return JSONResponse({"error": "rate limited"}, status_code=429, headers={"Retry-After": "1"})
