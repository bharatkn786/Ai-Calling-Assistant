
import os
from twilio.rest import Client
from dotenv import load_dotenv
load_dotenv()

account_sid = os.getenv("account_sid")
auth_token=os.getenv("auth_token")
# twilio_number = "+15075643820"
twilio_number = "+19899990030"

target_number =os.getenv("phone_number")
print(target_number)
client = Client(account_sid, auth_token)

# Your actual public Serveo URL with /voice endpoint
# SERVEO_URL="https://subaru-consistently-appearance-famous.trycloudflare.com"
public_url = os.getenv("SERVEO_URL") + "/voice"
# public_url = f"{SERVEO_URL}/voice"

print("📞 Voice URL being used in call_user:", public_url)
call = client.calls.create(
    to=target_number,
    from_=twilio_number,
    url=public_url
)

print(f"✅ Call initiated! SID: {call.sid}")
