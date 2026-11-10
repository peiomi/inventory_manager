from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database.connection import Base, engine, SessionLocal
from .models.product import Product

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Inventory API"}

@app.get("/products")
def get_products(
    db: Session = Depends(get_db)
):
    return db.query(Product).all()

@app.get("/products/{product_id}")
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    return (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

@app.post("/products")
def create_product(product: dict, db: Session = Depends(get_db)):
    new_product = Product(
        name=product["name"],
        quantity=product["quantity"]
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return {
        "id": new_product.id,
        "name": new_product.name,
        "quantity": new_product.quantity
    }

@app.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    db.delete(product)
    db.commit()

    return {
        "message": "Product deleted"
    }

@app.put("products/{product_id}")
def update_product(
    product_id: int,
    product_data: dict,
    db: Session = Depends(get_db)
):
    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    product.name = product_data["name"]
    product.quantity = product_data["quantity"]

    db.commit()

    db.refresh(product)

    return product