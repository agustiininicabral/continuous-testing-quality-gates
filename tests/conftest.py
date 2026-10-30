from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import ITEMS, ITEMS_LOCK, app

BASELINE_ITEMS = deepcopy(ITEMS)


@pytest.fixture()
def client():
    with ITEMS_LOCK:
        ITEMS.clear()
        ITEMS.extend(deepcopy(BASELINE_ITEMS))
    with TestClient(app) as test_client:
        yield test_client
    with ITEMS_LOCK:
        ITEMS.clear()
        ITEMS.extend(deepcopy(BASELINE_ITEMS))
