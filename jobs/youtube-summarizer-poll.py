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

MAX_PREVIEW_CHARS = 15

def preview_response(response, max_chars=MAX_PREVIEW_CHARS):
    """
    Return a short, safe preview of the response body.
    Works for JSON and plain text.
    """
    try:
        body = response.text or ""
    except Exception:
        return "<unable to read response body>"

    body = body.replace("\n", " ").strip()
    return body[:max_chars] + ("..." if len(body) > max_chars else "")

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

    # Always log a preview, regardless of success/failure
    preview = preview_response(response)
    if preview:
        print(f"Response preview: {preview}")

    try:
        response.raise_for_status()
        print("Request succeeded")
    except requests.exceptions.HTTPError as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    main()