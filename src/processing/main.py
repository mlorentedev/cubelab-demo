import os
import time
import cv2
from minio import Minio
from fastapi import FastAPI
from dotenv import load_dotenv
import threading

load_dotenv()
print("Environment variables loaded:", os.environ)

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "minio:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minio")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minio123")
BUCKET_NAME = os.getenv("BUCKET_NAME", "images")
RESULTS_DIR = os.getenv("RESULTS_DIR", "/results")
SCAN_INTERVAL = int(os.getenv("SCAN_INTERVAL", "10"))

client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False,
)

app = FastAPI()

def process_images():
    print("Processing images...")
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)
        print(f"Created results directory: {RESULTS_DIR}")

    try:
        objects = client.list_objects(BUCKET_NAME)
        for obj in objects:
            filename = obj.object_name
            thumb_path = os.path.join(RESULTS_DIR, f"thumb_{filename}")
            if os.path.exists(thumb_path):
                continue             
            
            print(f"Processing file: {filename}")
            local_path = f"/tmp/{filename}"
            thumb_path = f"{RESULTS_DIR}thumb_{filename}"
            client.fget_object(BUCKET_NAME, filename, local_path)
            
            image = cv2.imread(local_path)
            if image is None:
                print(f"Failed to read image: {local_path}")
                continue

            thumbnail = cv2.resize(image, (128, 128))
            success = cv2.imwrite(thumb_path, thumbnail)
            print(f"Thumbnail created: {thumb_path}, Success: {success}")
            os.remove(local_path)

    except Exception as e:
        print(f"Error processing images: {e}")

@app.on_event("startup")
def start_polling():
    def poll():
        print("Starting image bucket polling every", SCAN_INTERVAL, "seconds")
        while True:
            try:
                print("Polling for new images...")
                process_images()
            except Exception as e:
                print(f"Error during polling: {e}")
            finally:
                time.sleep(SCAN_INTERVAL)
    thread = threading.Thread(target=poll, daemon=True)
    thread.start()
    print("Polling thread started")
