from sqlalchemy import select
from sqlalchemy.orm import Session
from app.clients.crm_client import CRMClient
from app.models.customer import Customer


async def sync_all_customers(db: Session):
    client = CRMClient()
    page = 1
    created = 0
    updated = 0

    while True:
        result = await client.list_customers(page=page, page_size=50)
        customers = result.get("customers", [])

        if not customers:
            break

        for item in customers:
            customer = db.scalar(
                select(Customer).where(Customer.external_id == item["id"])
            )

            if customer:
                customer.name = item["name"]
                customer.email = item["email"]
                customer.status = item.get("status", "active")
                customer.metadata_json = item.get("metadata", {})
                updated += 1
            else:
                db.add(
                    Customer(
                        external_id=item["id"],
                        name=item["name"],
                        email=item["email"],
                        status=item.get("status", "active"),
                        metadata_json=item.get("metadata", {}),
                    )
                )
                created += 1

        db.commit()

        if not result.get("next_page"):
            break

        page += 1

    return {"created": created, "updated": updated}
