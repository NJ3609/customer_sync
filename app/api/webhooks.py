import json
from fastapi import APIRouter, Header, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import Depends
from app.db.database import get_db
from app.models.event import WebhookEvent, OrderEvent
from app.schemas.webhook import WebhookPayload
from app.utils.security import verify_signature

router = APIRouter()


@router.post("/crm")
async def receive_webhook(
    request: Request,
    x_webhook_signature: str = Header(...),
    db: Session = Depends(get_db),
):
    raw = await request.body()

    if not verify_signature(raw, x_webhook_signature):
        raise HTTPException(401, "Invalid webhook signature")

    try:
        data = WebhookPayload.model_validate(json.loads(raw))
    except Exception:
        raise HTTPException(400, "Invalid webhook payload")

    existing = db.scalar(
        select(WebhookEvent).where(WebhookEvent.event_id == data.event_id)
    )

    if existing:
        return {"status": "duplicate", "event_id": data.event_id}

    event = WebhookEvent(
        event_id=data.event_id,
        event_type=data.event_type,
        payload=data.model_dump(),
    )
    db.add(event)

    if data.event_type.startswith("order."):
        order = OrderEvent(
            event_id=data.event_id,
            customer_external_id=str(data.data.get("customer_id", "")),
            event_type=data.event_type,
            amount=str(data.data.get("amount"))
            if data.data.get("amount") is not None else None,
            payload=data.model_dump(),
        )
        db.add(order)

    db.commit()

    return {"status": "accepted", "event_id": data.event_id}
