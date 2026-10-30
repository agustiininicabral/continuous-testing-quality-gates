import pytest
from fastapi.testclient import TestClient
from src.app import app, ITEMS


@pytest.fixture()
def client():
    original = ITEMS.copy()
    ITEMS.clear()
    ITEMS.extend(original)
    with TestClient(app) as test_client:
        yield test_client
    ITEMS.clear()
    ITEMS.extend(original)
