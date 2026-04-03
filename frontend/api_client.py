import requests

BASE_URL = "http://127.0.0.1:5000"

def get_prediction(data):
    return requests.post(f"{BASE_URL}/predict_full/full",json=data).json()

def upload_documents(files):
    return requests.post(f"{BASE_URL}/ocr/upload-documents", files=files, timeout=120).json()