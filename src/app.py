from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Quality Gates Demo API", version="1.0.0")


class Item(BaseModel):
    id: int
    name: str = Field(min_length=2)
    price: float = Field(gt=0)


ITEMS = [
    Item(id=1, name="Keyboard", price=45.0),
    Item(id=2, name="Mouse", price=25.5),
]


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}


@app.get("/api/items")
def list_items() -> list[Item]:
    return ITEMS


@app.get("/api/items/{item_id}")
def get_item(item_id: int) -> Item:
    for item in ITEMS:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")


@app.post("/api/items", status_code=201)
def create_item(item: Item) -> Item:
    if any(existing.id == item.id for existing in ITEMS):
        raise HTTPException(status_code=409, detail="Item already exists")
    ITEMS.append(item)
    return item
