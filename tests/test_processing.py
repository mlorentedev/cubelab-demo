
import os

def test_thumbnail_generated():
    results_dir = "./results"
    files = os.listdir(results_dir)
    assert any(f.startswith("thumb_") and f.endswith(".jpg") for f in files), "No se generaron thumbnails"
