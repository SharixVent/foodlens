# 🍏 FoodLens — OCR etykiet + OpenFoodFacts + ocena produktu

FoodLens to aplikacja, która:
- skanuje etykiety produktów spożywczych (OCR, Tesseract),
- pobiera dane po **EAN** z **OpenFoodFacts**,
- przelicza prosty **„score zdrowotny”** (0–100) na bazie Twoich reguł (wykluczenia, limity cukru/soli),
- pozwala podejrzeć ostatnio zapisane produkty.

**Stack:** FastAPI (Python) · PostgreSQL · Alembic · Tesseract OCR (pl) · Next.js (React/TS, App Router) · Tailwind

---

## ✨ Funkcje

- **📷 OCR etykiety** — wyciąga listę składników i surowy tekst.
- **🔎 EAN lookup** — dane produktu z OpenFoodFacts (nazwa, marka, skład, nutriments).
- **⚖️ Ocena produktu** — proste kary za przekroczenia limitów i wykluczenia składników → wynik 0–100.
- **🧰 Filtry** — globalne reguły (np. „max cukry 12 g/100 g”, „wyklucz: orzechy, gluten”).
- **🗂 Ostatnie produkty** — szybki podgląd i ponowna ocena.
- **🧪 Swagger** — interaktywna dokumentacja API.

---

## 🗺 Architektura
```
infra/
  docker-compose.yml # Postgres + backend + frontend
backend/
  Dockerfile
  requirements.txt
  app/
    routers/
    main.py # FastAPI + CORS + routery
    health.py # GET /health
    products.py # GET /products, GET /products/barcode/{ean}
    analyze.py # POST /analyze/ocr, POST /analyze/score/{id}, /analyze/rules
    ocr.py # Tesseract OCR (eng+pol), ekstrakcja składników
    evaluate.py # liczenie score'u
    openfoodfacts.py # klient OFF
  migrations/ # Alembic
frontend/
  Dockerfile
  app/ # Next.js App Router (Skanuj, Produkty, Filtry)
  components/
  lib/
```


---

## 🔌 API – skrót

- `GET /health` → `{ "status": "ok" }`
- `GET /products` → lista ostatnich produktów
- `GET /products/barcode/{ean}` → pobierz z OpenFoodFacts (i zapisz)
- `POST /analyze/ocr` → multipart `file` → `{ text, ingredients[] }`
- `POST /analyze/rules` → zapisz globalne reguły
- `GET /analyze/rules` → pobierz reguły
- `POST /analyze/score/{product_id}` → policz `score` + `issues`

Swagger: **http://localhost:8000/docs**

---

## 🚀 Szybki start (Docker)

> Wymagane: **Docker** (Docker Desktop na Windows/macOS; na Linux – docker + docker compose).  
> Na Windows zalecany WSL2 z włączoną integracją w Docker Desktop.

1. Uruchom:
   ```bash
   cd infra
   docker compose up --build
  ```
