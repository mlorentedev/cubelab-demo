
import requests

def test_upload_image():
    url = "http://localhost:8080/upload"
    files = {'file': ('test.jpg', open('tests/test.jpg', 'rb'), 'image/jpeg')}
    response = requests.post(url, files=files)
    assert response.status_code == 200
    assert "Upload successful" in response.text or "status" in response.json()
