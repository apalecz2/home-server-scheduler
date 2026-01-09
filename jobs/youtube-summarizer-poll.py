import os
import requests
from datetime import datetime, timezone

# Configuration from environment
URL = os.getenv("YT_SUMM_URL")
API_KEY = os.getenv("YT_SUMM_API_KEY")

HEADERS = {
    "x-api-key": API_KEY,
    "User-Agent": "scheduler/1.0",
}

def main():
    if not URL:
        raise RuntimeError("YT_SUMM_URL env var not set")
    if not API_KEY:
        raise RuntimeError("YT_SUMM_API_KEY env var not set")

    # Perform the request
    # Note: data=FORM_DATA removed as api_poll() doesn't seem to expect a body
    response = requests.post(
        URL,
        headers=HEADERS,
        timeout=120, # Increased because video summarization is slow
    )

    # Get current UTC time (timezone-aware)
    now_utc = datetime.now(timezone.utc)

    print(
        f"[{now_utc.isoformat()}] POST {URL} -> "
        f"Status: {response.status_code}"
    )

    try:
        response.raise_for_status()
        print("Success:", response.json())
    except requests.exceptions.HTTPError as e:
        print(f"Request failed: {e}")
        if response.text:
            print("Server Response:", response.text)

if __name__ == "__main__":
    main()