from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.sync_service import sync_all_customers
from app.clients.crm_client import CRMError

router = APIRouter()


@router.post("")
async def sync(db: Session = Depends(get_db)):
    try:
        return await sync_all_customers(db)
    except CRMError as exc:
        raise HTTPException(502, str(exc))
