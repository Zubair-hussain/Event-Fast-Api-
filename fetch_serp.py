# fetch_serp.py
import os
import http.client
import json
import socket

API_KEY = os.getenv("f9f4949f-9179-4f4f-ba14-bfb64098245c")
API_HOST = "api.hasdata.com"


def fetch_serp_data(query, location, gl="pk", device_type="desktop", tbs="qdr:w", tbm="lcl", num=50):
    """
    Fetches Google SERP data from HasData API and returns the decoded string.
    """
    if not API_KEY:
        raise ValueError("Missing HASDATA_API_KEY environment variable.")

    conn = None
    try:
        encoded_location = location.replace(",", "%2C")
        encoded_tbs = tbs.replace(":", "%3A")

        path = (
            f"/scrape/google/serp?q={query}&location={encoded_location}&gl={gl}"
            f"&tbs={encoded_tbs}&tbm={tbm}&deviceType={device_type}&num={num}"
        )

        headers = {
            "x-api-key": API_KEY,
            "Content-Type": "application/json"
        }

        conn = http.client.HTTPSConnection(API_HOST, timeout=10)
        conn.request("GET", path, headers=headers)
        res = conn.getresponse()

        if 200 <= res.status < 300:
            data = res.read().decode("utf-8")
            try:
                return json.loads(data)  # return as parsed JSON
            except json.JSONDecodeError:
                return {"raw": data}
        else:
            error_text = res.read().decode("utf-8")
            return {"error": f"API returned status {res.status}", "details": error_text}

    except (http.client.HTTPException, socket.gaierror, socket.timeout) as e:
        return {"error": f"Request failed: {e}"}
    finally:
        if conn:
            conn.close()
