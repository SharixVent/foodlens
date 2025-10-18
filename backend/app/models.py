from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float, ForeignKey, Text, JSON
from .db import Base

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    barcode: Mapped[str | None] = mapped_column(String(64), index=True)
    name: Mapped[str] = mapped_column(String(255))
    brand: Mapped[str | None] = mapped_column(String(255))
    ingredients_text: Mapped[str | None] = mapped_column(Text)
    nutriscore: Mapped[str | None] = mapped_column(String(5))
    nova_group: Mapped[int | None] = mapped_column(Integer)
    nutrition: Mapped[dict | None] = mapped_column(JSON)

    evaluations: Mapped[list["Evaluation"]] = relationship("Evaluation", back_populates="product")

class Evaluation(Base):
    __tablename__ = "evaluations"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    score: Mapped[float] = mapped_column(Float)
    issues: Mapped[dict | None] = mapped_column(JSON)
    rules_snapshot: Mapped[dict | None] = mapped_column(JSON)

    product: Mapped[Product] = relationship("Product", back_populates="evaluations")

class Rules(Base):
    __tablename__ = "rules"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), default="default")
    exclude_ingredients: Mapped[list[str]] = mapped_column(JSON, default=[])
    max_sugars_g_per_100g: Mapped[float | None] = mapped_column(Float)
    max_salt_g_per_100g: Mapped[float | None] = mapped_column(Float)
