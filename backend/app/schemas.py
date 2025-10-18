from pydantic import BaseModel, Field
from typing import Any

class ProductCreate(BaseModel):
    barcode: str | None = None
    name: str
    brand: str | None = None
    ingredients_text: str | None = None
    nutriscore: str | None = None
    nova_group: int | None = None
    nutrition: dict | None = None

class ProductOut(ProductCreate):
    id: int

class EvaluationOut(BaseModel):
    id: int
    product_id: int
    score: float
    issues: dict | None = None
    rules_snapshot: dict | None = None

class RulesIn(BaseModel):
    name: str = Field(default="default")
    exclude_ingredients: list[str] = Field(default_factory=list)
    max_sugars_g_per_100g: float | None = None
    max_salt_g_per_100g: float | None = None

class OCRResult(BaseModel):
    text: str
    ingredients: list[str]
