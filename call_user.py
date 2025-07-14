
# import os
# from twilio.rest import Client
# from dotenv import load_dotenv
# load_dotenv()

# account_sid = os.getenv("account_sid")
# auth_token=os.getenv("auth_token")
# # twilio_number = "+15075643820"
# twilio_number = "+19899990030"

# target_number =os.getenv("phone_number")
# print(target_number)
# client = Client(account_sid, auth_token)

# # Your actual public Serveo URL with /voice endpoint
# # SERVEO_URL="ai-call-assistance-ebh2h7bwgwbmcdh8.centralindia-01.azurewebsites.net"
# public_url = os.getenv("SERVEO_URL") + "/voice"
# # public_url = f"{SERVEO_URL}/voice"

# print("📞 Voice URL being used in call_user:", public_url)
# call = client.calls.create(
#     to=target_number,
#     from_=twilio_number,
#     url=public_url
# )

# print(f"✅ Call initiated! SID: {call.sid}")
# call_user.py

import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

def start_twilio_call():
    account_sid = os.getenv("twilio_sid")
    auth_token = os.getenv("twilio_token")
    twilio_number = "+19899990030"
    target_number = os.getenv("phone_number")
    serveo_url = os.getenv("SERVEO_URL")

    if not all([account_sid, auth_token, target_number, serveo_url]):
        print("❌ Missing required environment variables")
        return False

    voice_url = serveo_url + "/voice"
    print("📞 Calling:", target_number)
    print("🌐 Voice URL:", voice_url)

    client = Client(account_sid, auth_token)

    try:
        call = client.calls.create(
            to=target_number,
            from_=twilio_number,
            url=voice_url
        )
        print(f"✅ Call initiated! SID: {call.sid}")
        return True
    except Exception as e:
        print("❌ Twilio call failed:", e)
        return False
