from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select, SQLModel
from database import engine, get_session
from models import Item, ItemCreate, ItemUpdate, StatusEnum
from typing import List

# Create the database tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI(title="Lost and Found API")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Lost & Found API!"}

# 1. POST /items
@app.post("/items", response_model=Item, status_code=201)
def create_item(item: ItemCreate, db: Session = Depends(get_session)):
    db_item = Item.model_validate(item)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# 2. GET /items
@app.get("/items", response_model=List[Item])
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_session)):
    items = db.exec(select(Item).offset(skip).limit(limit)).all()
    return items

# 3. GET /items/{item_id}
@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int, db: Session = Depends(get_session)):
    item = db.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# 4. PUT /items/{item_id}
@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: ItemUpdate, db: Session = Depends(get_session)):
    db_item = db.get(Item, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    item_data = item.model_dump(exclude_unset=True)
    for key, value in item_data.items():
        setattr(db_item, key, value)
    
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# 5. DELETE /items/{item_id}
@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_session)):
    item = db.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"message": "Item deleted successfully"}

# 6. GET /items/status/{status}
@app.get("/items/status/{status}", response_model=List[Item])
def read_items_by_status(status: StatusEnum, db: Session = Depends(get_session)):
    items = db.exec(select(Item).where(Item.status == status)).all()
    return items

# 7. GET /items/category/{category}
@app.get("/items/category/{category}", response_model=List[Item])
def read_items_by_category(category: str, db: Session = Depends(get_session)):
    items = db.exec(select(Item).where(Item.category == category)).all()
    return items
