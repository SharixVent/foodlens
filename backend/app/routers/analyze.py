from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from .. import models, schemas
from ..ocr import extract_text, guess_ingredients
from ..evaluate import evaluate_product

router = APIRouter(prefix="/analyze", tags=["analyze"])

@router.post("/ocr", response_model=schemas.OCRResult)
async def ocr_endpoint(file: UploadFile = File(...)):
    content = await file.read()
    text = extract_text(content)
    ingredients = guess_ingredients(text)
    return schemas.OCRResult(text=text, ingredients=ingredients)

@router.post("/score/{product_id}", response_model=schemas.EvaluationOut)
async def score_product(product_id: int, rules: schemas.RulesIn, db: Session = Depends(get_db)):
    p = db.get(models.Product, product_id)
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")
    score, issues = evaluate_product(p.nutrition or {}, (p.ingredients_text or "").split(","), rules.model_dump())
    ev = models.Evaluation(product_id=product_id, score=score, issues=issues, rules_snapshot=rules.model_dump())
    db.add(ev)
    db.commit()
    db.refresh(ev)
    return ev

@router.post("/rules", response_model=schemas.RulesIn)
async def set_rules(rules: schemas.RulesIn, db: Session = Depends(get_db)):
    # MVP: single global rules row (id=1)
    row = db.get(models.Rules, 1)
    if not row:
        row = models.Rules(id=1)
        db.add(row)
        db.flush()
    row.name = rules.name
    row.exclude_ingredients = rules.exclude_ingredients
    row.max_sugars_g_per_100g = rules.max_sugars_g_per_100g
    row.max_salt_g_per_100g = rules.max_salt_g_per_100g
    db.commit()
    return rules

@router.get("/rules", response_model=schemas.RulesIn)
async def get_rules(db: Session = Depends(get_db)):
    row = db.get(models.Rules, 1)
    if not row:
        return schemas.RulesIn()
    return schemas.RulesIn(
        name=row.name,
        exclude_ingredients=row.exclude_ingredients or [],
        max_sugars_g_per_100g=row.max_sugars_g_per_100g,
        max_salt_g_per_100g=row.max_salt_g_per_100g,
    )
