import pytest


@pytest.mark.regression
def test_duplicate_item_is_rejected_without_mutating_data(client):
    before = client.get("/api/items").json()

    response = client.post(
        "/api/items",
        json={"id": 1, "name": "Duplicate", "price": 20.0},
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Item already exists"
    assert client.get("/api/items").json() == before


@pytest.mark.regression
def test_invalid_item_payload_does_not_create_item(client):
    before = client.get("/api/items").json()

    response = client.post(
        "/api/items",
        json={"id": 3, "name": "Invalid", "price": 0},
    )

    assert response.status_code == 422
    assert client.get("/api/items").json() == before
