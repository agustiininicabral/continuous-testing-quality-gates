import pytest


@pytest.mark.contract
def test_items_have_strict_json_types(client):
    items = client.get("/api/items").json()
    for item in items:
        assert isinstance(item["id"], int)
        assert isinstance(item["name"], str)
        assert isinstance(item["price"], (int, float))
        assert item["name"].strip()
        assert item["price"] > 0
