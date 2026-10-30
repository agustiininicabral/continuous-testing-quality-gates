import pytest
from pydantic import ValidationError

from src.app import Item


@pytest.mark.unit
@pytest.mark.parametrize(
    ("payload", "expected"),
    [
        ({"id": 10, "name": "Monitor", "price": 100.0}, 10),
        ({"id": 11, "name": "Desk", "price": 75.5}, 11),
    ],
)
def test_valid_item_payload(payload, expected):
    assert Item(**payload).id == expected


@pytest.mark.unit
@pytest.mark.parametrize(
    "payload",
    [
        {"id": 1, "name": "A", "price": 10},
        {"id": 1, "name": "Valid", "price": 0},
        {"id": 1, "name": "Valid", "price": -1},
        {"id": 1, "name": "Valid", "price": float("nan")},
        {"id": 1, "name": "Valid", "price": float("inf")},
        {"id": True, "name": "Valid", "price": 10},
        {"id": "1", "name": "Valid", "price": 10},
        {"id": 1, "name": "x" * 101, "price": 10},
    ],
)
def test_invalid_item_payload_is_rejected(payload):
    with pytest.raises(ValidationError):
        Item(**payload)
