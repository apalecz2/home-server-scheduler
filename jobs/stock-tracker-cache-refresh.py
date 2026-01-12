import os
import requests
from datetime import datetime, timezone

URL = os.getenv("STOCK_REFRESH_URL")
API_KEY = os.getenv("STOCK_API_KEY")

HEADERS = {
    "x-api-key": API_KEY,
    "User-Agent": "scheduler/1.0",
}

MAX_PREVIEW_CHARS = 20

def preview_response(response, max_chars=MAX_PREVIEW_CHARS):
    """Return a short, safe preview of the response body."""
    try:
        body = response.text or ""
    except Exception:
        return "<unable to read response body>"

    body = body.replace("\n", " ").strip()
    return body[:max_chars] + ("..." if len(body) > max_chars else "")

def main():
    if not URL:
        raise RuntimeError("STOCK_REFRESH_URL env var not set")
    if not API_KEY:
        raise RuntimeError("STOCK_API_KEY env var not set")

    print(f"[{datetime.now(timezone.utc).isoformat()}] Starting stock cache refresh...")

    try:
        response = requests.post(
            URL,
            headers=HEADERS,
            timeout=60, 
        )
        
        status_msg = f"POST {URL} -> Status: {response.status_code}"
        print(f"[{datetime.now(timezone.utc).isoformat()}] {status_msg}")

        preview = preview_response(response)
        if preview:
            print(f"Response preview: {preview}")

        response.raise_for_status()
        print("Stock cache refresh succeeded.")

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        exit(1)

if __name__ == "__main__":
    main()