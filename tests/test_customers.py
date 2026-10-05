def test_create_customer(client):
    response = client.post(
        "/customers",
        json={
            "external_id": "test-001",
            "name": "Test User",
            "email": "test@example.com",
        },
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Test User"


def test_get_customer(client):
    response = client.get("/customers")
    assert response.status_code == 200
