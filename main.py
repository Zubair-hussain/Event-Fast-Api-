# main.py
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from fetch_serp import fetch_serp_data
import requests

app = FastAPI(title="HasData SERP API", version="1.0")


class SerpQuery(BaseModel):
    query: str
    location: str | None = None  # optional; auto-detect if not given
    gl: str = "pk"
    device_type: str = "desktop"
    tbs: str = "qdr:w"
    tbm: str = "lcl"
    num: int = 50


def get_user_location(ip: str) -> str:
    """
    Detect user's location using ipapi.co (primary) and ipinfo.io (fallback).
    Returns a formatted string like: 'City,Region,Country'
    Defaults to 'Karachi,Sindh,Pakistan' if all fail.
    """
    default_location = "Karachi,Sindh,Pakistan"

    # --- Primary: ipapi.co ---
    try:
        res = requests.get(f"https://ipapi.co/{ip}/json/", timeout=5)
        data = res.json()
        if all(k in data for k in ["city", "region", "country_name"]):
            city = data.get("city", "")
            region = data.get("region", "")
            country = data.get("country_name", "")
            if city and country:
                return f"{city},{region},{country}"
    except Exception:
        pass  # move to fallback

    # --- Fallback: ipinfo.io ---
    try:
        res = requests.get(f"https://ipinfo.io/{ip}/json", timeout=5)
        data = res.json()
        if all(k in data for k in ["city", "region", "country"]):
            city = data.get("city", "")
            region = data.get("region", "")
            country = data.get("country", "")
            if city and country:
                return f"{city},{region},{country}"
    except Exception:
        pass

    # --- Final fallback ---
    return default_location


@app.post("/serp")
async def get_serp_data(request: Request, params: SerpQuery):
    """
    POST /serp
    Automatically detects user location from IP if not provided.
    Example body:
    {
        "query": "Exhibition"
    }
    """
    try:
        # Extract client IP
        client_ip = request.client.host

        # Determine user location (auto or provided)
        location = params.location or get_user_location(client_ip)

        # Fetch data from HasData
        data = fetch_serp_data(
            query=params.query,
            location=location,
            gl=params.gl,
            device_type=params.device_type,
            tbs=params.tbs,
            tbm=params.tbm,
            num=params.num
        )

        if isinstance(data, dict) and "error" in data:
            raise HTTPException(status_code=400, detail=data)

        return {
            "detected_location": location,
            "results": data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
