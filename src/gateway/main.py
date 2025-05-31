from fastapi import FastAPI, UploadFile, File
import requests
import shutil
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv(dotenv_path="/app/.env")

STORAGE_UPLOAD_URL = os.getenv("STORAGE_UPLOAD_URL")

logger.info(f"Storage upload URL: {STORAGE_UPLOAD_URL}")

app = FastAPI()

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    temp_path = f"/tmp/{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    with open(temp_path, "rb") as f:
        response = requests.post(STORAGE_UPLOAD_URL, files={"file": (file.filename, f)})

    os.remove(temp_path)
    return {"status": response.status_code, "detail": response.text}
