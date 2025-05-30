from fastapi import FastAPI, UploadFile, File
from minio import Minio
from minio.error import S3Error
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="/app/.env")

app = FastAPI()

client = Minio(
    os.environ.get("MINIO_ENDPOINT"),
    access_key=os.environ.get("MINIO_ACCESS_KEY"),
    secret_key=os.environ.get("MINIO_SECRET_KEY"),
    secure=False
)

BUCKET_NAME = "images"

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
