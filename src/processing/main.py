from datetime import datetime
import os
import time
import cv2
from minio import Minio
from fastapi import FastAPI
import threading
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
RESULTS_DIR = os.getenv("RESULTS_DIR")
SCAN_INTERVAL = int(os.getenv("SCAN_INTERVAL"))

logger.info(f"MinIO config - Endpoint: {MINIO_ENDPOINT}, Bucket: {BUCKET_NAME}")

# Initialize MinIO client
client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ROOT_USER,
    secret_key=MINIO_ROOT_PASSWORD,
    secure=False
)

app = FastAPI()

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

def process_images():
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)
        logger.info(f"Created results directory: {RESULTS_DIR}")
    try:
        objects = client.list_objects(BUCKET_NAME)
        for obj in objects:
            filename = obj.object_name
            thumb_path = os.path.join(RESULTS_DIR, f"thumb_{filename}")
            if os.path.exists(thumb_path):
                logger.info(f"Thumbnail already exists for {filename}, skipping...")
                continue             
            logger.info(f"Processing image: {filename}")
            local_path = f"/tmp/{filename}"
            thumb_path = f"{RESULTS_DIR}/thumb_{filename}"
            try:
                client.fget_object(BUCKET_NAME, filename, local_path)
            except Exception as e:
                logger.error(f"Failed to download {filename} from MinIO: {e}")
                continue
            image = cv2.imread(local_path)
            if image is None:
                logger.error(f"Failed to read image {filename}. Skipping...")
                continue

            max_size = 128
            h, w = image.shape[:2]
            scale = max_size / max(h, w)
            new_w = int(w * scale)
            new_h = int(h * scale)
            if h <= max_size and w <= max_size:
                thumbnail = image.copy()
            else:
                thumbnail = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
            
            success = cv2.imwrite(thumb_path, thumbnail)
            logger.info(f"Thumbnail created: {thumb_path}, Success: {success}")
            if not success:
                logger.error(f"Failed to save thumbnail for {filename}")
                continue
            os.remove(local_path)

    except Exception as e:
        logger.error(f"Error processing images: {e}")

def polling_worker():
    logger.info(f"Starting image bucket polling every {SCAN_INTERVAL} seconds")
    while True:
        try:
            logger.info("Polling for new images...")
            process_images()
        except Exception as e:
            logger.error(f"Error in polling worker: {e}")
        finally:
            time.sleep(SCAN_INTERVAL)

@app.on_event("startup")
def start_background_task():
    thread = threading.Thread(target=polling_worker, daemon=True)
    thread.start()
    logger.info("Polling worker started")
