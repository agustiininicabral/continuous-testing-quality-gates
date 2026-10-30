import pytest
from pydantic import ValidationError

from src.app import Item


@pytest.mark.unit
@pytest.mark.parametrize(
    "payload",
    [
        {"id": 0, "name": "Keyboard", "price": 20},
        {"id": -1, "name": "Keyboard", "price": 20},
        {"id": 3, "name": "   ", "price": 20},
    ],
)
def test_rejects_non_positive_ids_and_blank_names(payload):
    with pytest.raises(ValidationError):
        Item(**payload)


@pytest.mark.unit
def test_item_name_is_trimmed_before_validation():
    item = Item(id=3, name="  Keyboard  ", price=20)

    assert item.name == "Keyboard"
