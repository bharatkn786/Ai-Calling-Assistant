import hashlib
import time
import requests
import os
from dotenv import load_dotenv

load_dotenv()

cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME")
api_key = os.getenv("CLOUDINARY_API_KEY")
api_secret = os.getenv("CLOUDINARY_API_SECRET")
upload_url = f"https://api.cloudinary.com/v1_1/{cloud_name}/video/upload"

def upload_to_cloudinary(file_content: bytes, filename: str) -> str:
    """Upload audio file to Cloudinary and return secure URL"""
    try:
        timestamp = int(time.time())
        params_to_sign = f"timestamp={timestamp}{api_secret}"
        signature = hashlib.sha1(params_to_sign.encode()).hexdigest()

        files = {
            "file": (filename, file_content)
        }
        data = {
            "api_key": api_key,
            "timestamp": timestamp,
            "signature": signature
        }
        
        response = requests.post(upload_url, files=files, data=data)
        upload_json = response.json()
        
        if "secure_url" in upload_json:
            return upload_json["secure_url"]
        else:
            print("❌ Cloudinary upload failed:", upload_json)
            return None
    except Exception as e:
        print(f"❌ Cloudinary upload error: {e}")
        return None
