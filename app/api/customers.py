from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.customer import CustomerCreate, CustomerResponse, CustomerUpdate
from app.services.customer_service import (
    create_customer, get_customer, list_customers, update_customer
)

router = APIRouter()


@router.post("", response_model=CustomerResponse, status_code=201)
def create(data: CustomerCreate, db: Session = Depends(get_db)):
    customer, created = create_customer(db, data)
    if not created:
        raise HTTPException(409, "Customer already exists")
    return customer


@router.get("", response_model=list[CustomerResponse])
def list_all(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = None,
    status: str | None = None,
    sort: str = "created_at",
    db: Session = Depends(get_db),
):
    return list_customers(db, page, page_size, search, status, sort)


@router.get("/{customer_id}", response_model=CustomerResponse)
def get_one(customer_id: int, db: Session = Depends(get_db)):
    customer = get_customer(db, customer_id)
    if not customer:
        raise HTTPException(404, "Customer not found")
    return customer


@router.patch("/{customer_id}", response_model=CustomerResponse)
def update(
    customer_id: int,
    data: CustomerUpdate,
    db: Session = Depends(get_db),
):
    customer = get_customer(db, customer_id)
    if not customer:
        raise HTTPException(404, "Customer not found")
    return update_customer(db, customer, data)
