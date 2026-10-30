import pytest


@pytest.mark.integration
@pytest.mark.parametrize(
    "payload",
    [
        {"id": 0, "name": "Keyboard", "price": 20},
        {"id": 3, "name": "   ", "price": 20},
    ],
)
def test_create_item_rejects_invalid_identifier_and_blank_name(client, payload):
    before = client.get("/api/items").json()

    response = client.post("/api/items", json=payload)

    assert response.status_code == 422
    assert client.get("/api/items").json() == before
