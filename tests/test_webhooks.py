import hashlib
import hmac
import json


def test_webhook(client):
    payload = {
        "event_id": "evt-test-001",
        "event_type": "order.created",
        "data": {"customer_id": "crm-001", "amount": 100},
    }

    raw = json.dumps(payload, separators=(",", ":")).encode()
    signature = hmac.new(b"super-secret", raw, hashlib.sha256).hexdigest()

    response = client.post(
        "/webhooks/crm",
        content=raw,
        headers={"X-Webhook-Signature": signature},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "accepted"


def test_bad_signature(client):
    response = client.post(
        "/webhooks/crm",
        content=b'{"event_id":"x","event_type":"customer.updated","data":{}}',
        headers={"X-Webhook-Signature": "bad"},
    )
    assert response.status_code == 401
