import time
import requests
import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

TWILIO_SID = os.getenv("account_sid")
TWILIO_TOKEN = os.getenv("auth_token")

def fetch_twilio_audio_with_retry(url: str, retries: int = 4, delay: float = 1.5):
    """
    Number of times sending request to twilio to fetch audio with retry logic
    """
    for attempt in range(retries):
        print(f"🔁 Attempt {attempt + 1} to fetch Twilio audio...")
        res = requests.get(url, auth=HTTPBasicAuth(TWILIO_SID, TWILIO_TOKEN))
        if res.status_code == 200:
            print("✅ Audio fetched from Twilio.")
            return res
        time.sleep(delay)
    print("❌ Failed to fetch audio after retries.")
    return None
