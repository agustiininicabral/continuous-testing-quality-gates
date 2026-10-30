import pytest


@pytest.mark.integration
def test_health_contract(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


@pytest.mark.integration
def test_list_items_contract(client):
    response = client.get("/api/items")
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2
    assert {item["id"] for item in body} == {1, 2}
    assert all({"id", "name", "price"} <= item.keys() for item in body)


@pytest.mark.integration
def test_get_missing_item_returns_404(client):
    response = client.get("/api/items/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"


@pytest.mark.integration
def test_create_item_returns_201(client):
    response = client.post(
        "/api/items",
        json={"id": 3, "name": "Webcam", "price": 60.0},
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Webcam"
