import math
from threading import Lock
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field

app = FastAPI(title="Quality Gates Demo API", version="1.1.0")


class Item(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    id: int = Field(gt=0, strict=True)
    name: str = Field(min_length=2, max_length=100)
    price: float = Field(gt=0, strict=True, allow_inf_nan=False)


def _json_safe(value: Any) -> Any:
    if isinstance(value, float) and not math.isfinite(value):
        return repr(value)
    if isinstance(value, dict):
        return {key: _json_safe(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_safe(item) for item in value]
    return value


@app.exception_handler(RequestValidationError)
async def handle_request_validation_error(
    _request: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={"detail": jsonable_encoder(_json_safe(exc.errors()))},
    )


ITEMS_LOCK = Lock()

ITEMS = [
    Item(id=1, name="Keyboard", price=45.0),
    Item(id=2, name="Mouse", price=25.5),
]


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}


@app.get("/api/items")
def list_items() -> list[Item]:
    with ITEMS_LOCK:
        return list(ITEMS)


@app.get("/api/items/{item_id}")
def get_item(item_id: int) -> Item:
    with ITEMS_LOCK:
        for item in ITEMS:
            if item.id == item_id:
                return item
    raise HTTPException(status_code=404, detail="Item not found")


@app.post("/api/items", status_code=201)
def create_item(item: Item) -> Item:
    with ITEMS_LOCK:
        if any(existing.id == item.id for existing in ITEMS):
            raise HTTPException(status_code=409, detail="Item already exists")
        ITEMS.append(item)
        return item
