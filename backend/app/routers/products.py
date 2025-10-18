from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from .. import models, schemas
from ..openfoodfacts import fetch_by_barcode

router = APIRouter(prefix="/products", tags=["products"])

@router.get("")
def list_products(db: Session = Depends(get_db)):
    items = db.query(models.Product).order_by(models.Product.id.desc()).limit(50).all()
    return items

@router.post("", response_model=schemas.ProductOut)
def create_product(payload: schemas.ProductCreate, db: Session = Depends(get_db)):
    p = models.Product(**payload.model_dump())
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

@router.get("/barcode/{barcode}")
async def get_by_barcode(barcode: str, db: Session = Depends(get_db)):
    # Spróbuj z bazy
    p = db.query(models.Product).filter(models.Product.barcode == barcode).first()
    if p:
        return p
    # Fallback do OpenFoodFacts
    data = await fetch_by_barcode(barcode)
    if not data:
        raise HTTPException(status_code=404, detail="Barcode not found")
    p = models.Product(**data)
    db.add(p)
    db.commit()
    db.refresh(p)
    return p
