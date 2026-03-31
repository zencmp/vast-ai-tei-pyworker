import os
import requests
import uvicorn
from fastapi import FastAPI, HTTPException

TEI_PORT = int(os.getenv("TEI_PORT", "8080"))
TEI_HOST = os.getenv("TEI_HOST", "http://localhost")
WORKER_HOST = os.getenv("WORKER_HOST", "0.0.0.0")
WORKER_PORT = int(os.getenv("WORKER_PORT", "3000"))

app = FastAPI()


@app.post("/embed")
def tei_handler(payload: dict):
    try:
        inputs = payload["inputs"]
    except KeyError as exc:
        raise HTTPException(status_code=400, detail="Missing 'inputs' in request body") from exc

    try:
        resp = requests.post(f"{TEI_HOST}:{TEI_PORT}/embed", json=inputs, timeout=60)
        resp.raise_for_status()
    except requests.RequestException as exc:
        raise HTTPException(status_code=502, detail=f"TEI backend error: {exc}") from exc

    return resp.json()


if __name__ == "__main__":
    uvicorn.run(app, host=WORKER_HOST, port=WORKER_PORT)
