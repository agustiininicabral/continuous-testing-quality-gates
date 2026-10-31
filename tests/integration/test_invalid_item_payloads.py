import json

import pytest


@pytest.mark.integration
@pytest.mark.parametrize(
    "payload",
    [
        {"id": 0, "name": "Keyboard", "price": 20},
        {"id": 3, "name": "   ", "price": 20},
        {"id": True, "name": "Keyboard", "price": 20},
        {"id": "3", "name": "Keyboard", "price": 20},
        {"id": 3, "name": "x" * 101, "price": 20},
        {"id": 3, "name": "Keyboard", "price": float("nan")},
        {"id": 3, "name": "Keyboard", "price": float("inf")},
        {"id": 3, "name": "Keyboard", "price": True},
        {"id": 3, "name": "Keyboard", "price": "20"},
        {"id": 3, "name": "Keyboard", "price": 20, "unexpected": "field"},
    ],
)
def test_create_item_rejects_invalid_payloads_without_mutating_state(client, payload):
    before = client.get("/api/items").json()

    # json= uses a strict encoder that rejects NaN/Infinity before the request
    # reaches the API. Serialize explicitly to exercise server-side validation.
    response = client.post(
        "/api/items",
        content=json.dumps(payload),
        headers={"content-type": "application/json"},
    )

    assert response.status_code == 422
    assert response.json()["detail"]
    assert client.get("/api/items").json() == before
