from fastapi import Header, HTTPException

# MVP: brak realnego auth. Zostawiamy hook pod przyszłe rozszerzenie.
async def get_current_profile(x_api_key: str | None = Header(default=None)):
    if x_api_key and x_api_key == "dev":
        return {"profile": "dev"}
    return {"profile": "anonymous"}
