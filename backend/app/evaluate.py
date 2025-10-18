from typing import Tuple, Dict, Any


def evaluate_product(nutrition: dict | None, ingredients: list[str], rules: dict) -> Tuple[float, Dict[str, Any]]:
    """Zwraca (score, issues).
    Score: 0-100 (100 = najlepszy)
    Prosty model na start: kary za przekroczenia i wykluczenia.
    """
    score = 100.0
    issues: dict[str, list[str] | float | dict] = {"exclude_hits": [], "limits": {}}

    excludes: list[str] = [e.lower() for e in rules.get("exclude_ingredients", [])]
    for ing in ingredients:
        for ex in excludes:
            if ex and ex in ing:
                issues["exclude_hits"].append(ing)
                score -= 20
                break

    limits = {
        "max_sugars_g_per_100g": ("sugars_100g", 1.5),  # kara * nadmiar * waga
        "max_salt_g_per_100g": ("salt_100g", 5.0),
    }
    if nutrition:
        for rule_key, (nutri_key, weight) in limits.items():
            limit = rules.get(rule_key)
            if limit is not None and nutrition.get(nutri_key) is not None:
                value = float(nutrition[nutri_key])
                excess = max(0.0, value - float(limit))
                if excess > 0:
                    score -= excess * weight
                    issues["limits"][nutri_key] = {"value": value, "limit": float(limit), "excess": excess}

    score = max(0.0, min(100.0, score))
    return score, issues
