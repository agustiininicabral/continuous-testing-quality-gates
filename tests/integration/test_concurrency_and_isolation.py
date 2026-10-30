from concurrent.futures import ThreadPoolExecutor

import pytest

from src.app import ITEMS, ITEMS_LOCK, Item


@pytest.mark.integration
def test_concurrent_duplicate_creates_are_atomic(client):
    payload = {"id": 50, "name": "Concurrent item", "price": 10.0}

    with ThreadPoolExecutor(max_workers=8) as executor:
        responses = list(
            executor.map(
                lambda _: client.post("/api/items", json=payload),
                range(16),
            )
        )

    statuses = [response.status_code for response in responses]
    assert statuses.count(201) == 1
    assert statuses.count(409) == 15
    assert sum(item["id"] == 50 for item in client.get("/api/items").json()) == 1


@pytest.mark.integration
def test_concurrent_distinct_creates_do_not_lose_items(client):
    item_ids = range(100, 116)

    def create_item(item_id):
        return client.post(
            "/api/items",
            json={"id": item_id, "name": f"Item {item_id}", "price": 10.0},
        )

    with ThreadPoolExecutor(max_workers=8) as executor:
        responses = list(executor.map(create_item, item_ids))

    assert all(response.status_code == 201 for response in responses)
    stored_ids = {item["id"] for item in client.get("/api/items").json()}
    assert set(item_ids) <= stored_ids


@pytest.fixture
def polluted_shared_state():
    with ITEMS_LOCK:
        ITEMS.append(Item(id=999, name="Leaked item", price=1.0))


@pytest.fixture
def dirty_client(polluted_shared_state, client):
    return client


@pytest.mark.integration
def test_client_fixture_restores_a_clean_baseline(dirty_client):
    response = dirty_client.get("/api/items")

    assert response.status_code == 200
    assert {item["id"] for item in response.json()} == {1, 2}
