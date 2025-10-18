from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from .routers import health, products, analyze

app = FastAPI(title="FoodLens API")

origins = [os.getenv("BACKEND_CORS_ORIGINS", "http://localhost:3000")] 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(products.router)
app.include_router(analyze.router)
