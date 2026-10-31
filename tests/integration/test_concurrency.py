from concurrent.futures import ThreadPoolExecutor

import pytest
from fastapi import HTTPException

from src.app import Item, create_item


@pytest.mark.integration
def test_concurrent_duplicate_creates_are_atomic(client):
    payload = {"id": 99, "name": "Concurrent item", "price": 12.5}

    def create(_):
        try:
            create_item(Item(**payload))
            return 201
        except HTTPException as error:
            return error.status_code

    with ThreadPoolExecutor(max_workers=8) as executor:
        statuses = list(executor.map(create, range(16)))

    assert statuses.count(201) == 1
    assert statuses.count(409) == 15
    matching_items = [
        item for item in client.get("/api/items").json() if item["id"] == payload["id"]
    ]
    assert len(matching_items) == 1
