import httpx

BASE_URL = "https://world.openfoodfacts.org/api/v2"

async def fetch_by_barcode(barcode: str):
    url = f"{BASE_URL}/product/{barcode}.json"
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(url)
        r.raise_for_status()
        data = r.json()
        if data.get("status") != 1:
            return None
        p = data["product"]
        return {
            "barcode": barcode,
            "name": p.get("product_name") or p.get("generic_name") or "Unknown",
            "brand": (p.get("brands") or "").split(",")[0] if p.get("brands") else None,
            "ingredients_text": p.get("ingredients_text") or p.get("ingredients_text_pl") or None,
            "nutriscore": p.get("nutriscore_grade"),
            "nova_group": p.get("nova_group"),
            "nutrition": {
                "sugars_100g": (p.get("nutriments") or {}).get("sugars_100g"),
                "salt_100g": (p.get("nutriments") or {}).get("salt_100g"),
                "fat_100g": (p.get("nutriments") or {}).get("fat_100g"),
            },
        }
