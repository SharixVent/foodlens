from PIL import Image
import pytesseract
from io import BytesIO
import re

INGR_PAT = re.compile(r"skład(?:niki)?[:\-]?\s*(.*)", re.IGNORECASE)


def extract_text(file_bytes: bytes) -> str:
    image = Image.open(BytesIO(file_bytes)).convert("RGB")
    text = pytesseract.image_to_string(image, lang="eng+pol")
    return text


def guess_ingredients(text: str) -> list[str]:
    # Najpierw spróbuj wyłuskać linie po słowie kluczowym "Skład"
    m = INGR_PAT.search(text)
    if m:
        chunk = m.group(1)
    else:
        chunk = text
    # Tokenizacja prosta: po przecinku/średniku/kropce
    parts = re.split(r"[,;\n]", chunk)
    cleaned = [p.strip().lower() for p in parts if p.strip()]
    # Odfiltruj typowe śmieci (procenty, spójniki)
    cleaned = [re.sub(r"\d+%", "", p).strip(" -") for p in cleaned]
    # Dedup przy zachowaniu kolejności
    seen = set()
    out = []
    for c in cleaned:
        if c and c not in seen and len(c) <= 80:
            seen.add(c)
            out.append(c)
    return out[:50]
