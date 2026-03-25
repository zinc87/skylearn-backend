import requests
from app.config import Config

CPP_LANGUAGE_ID = 54  # C++ (GCC 9.2.0)

def run_code(source_code: str, stdin: str = "") -> dict:
    """Submit C++ code to Judge0 and return results."""
    payload = {
        "source_code": source_code,
        "language_id": CPP_LANGUAGE_ID,
        "stdin": stdin,
        "cpu_time_limit": 5,
        "memory_limit": 128000,
    }

    headers = {"Content-Type": "application/json"}
    if Config.JUDGE0_API_KEY:
        headers["X-Auth-Token"] = Config.JUDGE0_API_KEY

    resp = requests.post(
        f"{Config.JUDGE0_API_URL}/submissions?base64_encoded=false&wait=true",
        json=payload,
        headers=headers,
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()

    return {
        "stdout": data.get("stdout") or "",
        "stderr": data.get("stderr") or data.get("compile_output") or "",
        "status": data.get("status", {}).get("description", "Unknown"),
        "time": data.get("time") or "0",
        "memory": data.get("memory") or 0,
    }
