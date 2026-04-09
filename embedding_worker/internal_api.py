import os
import requests
def update_status_in_db(video_id: str, new_status: str):
    backend_url = os.environ.get("BACKEND_URL")
    if not backend_url:
        raise ValueError("BACKEND_URL environment variable is missing")

    endpoint = f"{backend_url}/api/v1/content/{video_id}/status"
    payload = {"status": new_status}
    headers = {"X-Internal-API-Key": os.environ.get("INTERNAL_API_KEY")}
    response = requests.patch(endpoint, json=payload,headers=headers, timeout=10)

    response.raise_for_status()
    print(f"[*] Status updated to '{new_status}' for video {video_id}")