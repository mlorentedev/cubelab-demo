from fastapi import FastAPI, UploadFile, File
from minio import Minio
from minio.error import S3Error
import os
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv(dotenv_path="/app/.env")

app = FastAPI()

# MinIO configuration
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
MINIO_ROOT_USER = os.getenv("MINIO_ROOT_USER")
MINIO_ROOT_PASSWORD = os.getenv("MINIO_ROOT_PASSWORD")
BUCKET_NAME = os.getenv("BUCKET_NAME")

logger.info(f"MinIO config - Endpoint: {MINIO_ENDPOINT}, Bucket: {BUCKET_NAME}")

# Initialize MinIO client
client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ROOT_USER,
    secret_key=MINIO_ROOT_PASSWORD,
    secure=False
)

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

@app.on_event("startup")
def startup():
    if not client.bucket_exists(BUCKET_NAME):
        client.make_bucket(BUCKET_NAME)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    temp_path = f"/tmp/{file.filename}"
    with open(temp_path, "wb") as buffer:
        buffer.write(await file.read())
    try:
        client.fput_object(BUCKET_NAME, file.filename, temp_path)
        os.remove(temp_path)
        return {"message": "Upload successful"}
    except S3Error as e:
        return {"error": str(e)}
