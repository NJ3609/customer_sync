from sqlalchemy import select, or_
from sqlalchemy.orm import Session
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate


def create_customer(db: Session, data: CustomerCreate):
    existing = db.scalar(
        select(Customer).where(Customer.external_id == data.external_id)
    )
    if existing:
        return existing, False

    customer = Customer(
        external_id=data.external_id,
        name=data.name,
        email=str(data.email),
        status=data.status,
        metadata_json=data.metadata,
    )
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer, True


def get_customer(db: Session, customer_id: int):
    return db.get(Customer, customer_id)


def list_customers(
    db: Session,
    page: int,
    page_size: int,
    search: str | None,
    status: str | None,
    sort: str,
):
    query = select(Customer)

    if search:
        pattern = f"%{search}%"
        query = query.where(
            or_(Customer.name.ilike(pattern), Customer.email.ilike(pattern))
        )

    if status:
        query = query.where(Customer.status == status)

    sort_map = {
        "name": Customer.name,
        "email": Customer.email,
        "created_at": Customer.created_at,
    }
    column = sort_map.get(sort.lstrip("-"), Customer.created_at)
    query = query.order_by(column.desc() if sort.startswith("-") else column.asc())

    return db.scalars(
        query.offset((page - 1) * page_size).limit(page_size)
    ).all()


def update_customer(db: Session, customer: Customer, data: CustomerUpdate):
    values = data.model_dump(exclude_unset=True)
    if "metadata" in values:
        values["metadata_json"] = values.pop("metadata")

    for key, value in values.items():
        setattr(customer, key, str(value) if key == "email" else value)

    db.commit()
    db.refresh(customer)
    return customer
