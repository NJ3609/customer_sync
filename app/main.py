from fastapi import FastAPI
from app.api.customers import router as customers_router
from app.api.webhooks import router as webhooks_router
from app.api.sync import router as sync_router
from app.api.health import router as health_router
from app.db.database import Base, engine

# For this capstone we create tables automatically at startup.
# Production systems would normally use Alembic migrations.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Customer Sync & Automation Service", version="1.0.0")

app.include_router(health_router)
app.include_router(customers_router, prefix="/customers", tags=["customers"])
app.include_router(webhooks_router, prefix="/webhooks", tags=["webhooks"])
app.include_router(sync_router, prefix="/sync", tags=["sync"])


@app.get("/")
def root():
    return {"service": "customer-sync-service", "status": "running"}
