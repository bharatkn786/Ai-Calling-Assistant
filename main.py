from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import asyncio
import time

import os
import subprocess
from fastapi.responses import RedirectResponse

# importing the functions form the cores folder
from core.llm_chain import get_llm_response
from core.cloudinary import upload_to_cloudinary
from core.tts import synthesize_and_upload_edge_tts
from core.stt import transcribe_deepgram_from_url
from core.utils import fetch_twilio_audio_with_retry

# For now, using the hardcoded URL - you can modify this to use serveo_url.py later
# SERVEO_URL = "https://neither-chester-lyric-talking.trycloudflare.com"
from dotenv import load_dotenv
load_dotenv()

# SERVEO_URL= os.getenv("SERVEO_URL")
SERVEO_URL=os.getenv("SERVEO_URL")
# SERVEO_URL="ai-call-assistance-ebh2h7bwgwbmcdh8.centralindia-01.azurewebsites.net"
print(SERVEO_URL)
app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

templates = Jinja2Templates(directory="templates")

# Global memory for session
user_name = ""

@app.get("/", response_class=HTMLResponse)
async def serve_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/start-call")
async def start_call(request: Request):
    form = await request.form()
    name = form.get("name")
    phone = form.get("phone")

    # Set values as environment variables
    os.environ["CALLER_NAME"] = name
    os.environ["phone_number"] = phone

    # Run tunnel
    # subprocess.run(["python", "servo_url.py"])

    # Run call_user.py (it will read env vars)
    subprocess.run(["python", "call_user.py"])

    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/voice")
async def voice():
    global user_name
    user_name = ""  # 🔄 Reset user_name for new session
    if not SERVEO_URL:
        return PlainTextResponse("""
            <Response><Say>SERVEO URL not configured.</Say></Response>
        """, media_type="text/xml")

    return PlainTextResponse(f"""
        <Response>
            <Say>Welcome to Online Call ChatGPT.</Say>
            <Pause length="1" />
            <Say>May I know your good name please?</Say>
            <Record maxLength="4" action="{SERVEO_URL}/get-name" method="POST" />
            <Say>No name received. Goodbye!</Say>
        </Response>
    """, media_type="text/xml")

@app.post("/get-name")
async def get_name(request: Request):
    global user_name
    form = await request.form()
    recording_url = form.get("RecordingUrl")

    if not recording_url:
        return PlainTextResponse("""
            <Response><Say>I couldn't hear your name. Goodbye!</Say></Response>
        """, media_type="text/xml")

    try:
        # Fetch audio from Twilio (with retry logic)
        response = fetch_twilio_audio_with_retry(recording_url)
        if not response:
            return PlainTextResponse("""
                <Response><Say>Could not get your voice after retries. Goodbye!</Say></Response>
            """, media_type="text/xml")

        # Upload to Cloudinary
        cloud_audio_url = upload_to_cloudinary(response.content, "name.wav")
        if not cloud_audio_url:
            return PlainTextResponse("""
                <Response><Say>Could not upload your voice. Goodbye!</Say></Response>
            """, media_type="text/xml")

        print("📤 Name Audio URL:", cloud_audio_url)

        # Transcribe name
        transcript = await transcribe_deepgram_from_url(cloud_audio_url)
        print("📝 Raw Transcript:", transcript)

        words = transcript.strip().split()
        if not words:
            return PlainTextResponse(f"""
                <Response>
                    <Say>I couldn't catch your name clearly. Please say it again after the beep.</Say>
                    <Record maxLength="4" action="{SERVEO_URL}/get-name" method="POST" />
                </Response>
            """, media_type="text/xml")

        user_name = words[0].capitalize()
        print("👤 User Name:", user_name)

        return PlainTextResponse(f"""
            <Response>
                <Say>Hello {user_name}, what do you want to ask?</Say>
                <Record maxLength="15" timeout="3" action="{SERVEO_URL}/handle-recording" method="POST" />
                <Say>No input received. Goodbye!</Say>
            </Response>
        """, media_type="text/xml")

    except Exception as e:
        print("❌ Error in /get-name:", e)
        return PlainTextResponse("""
            <Response><Say>Something went wrong while processing your name.</Say></Response>
        """, media_type="text/xml")

@app.post("/handle-recording")
async def handle_recording(request: Request):
    form = await request.form()
    recording_url = form.get("RecordingUrl")
    if not recording_url:
        return PlainTextResponse("""
            <Response><Say>Recording URL missing. Goodbye.</Say></Response>
        """, media_type="text/xml")

    audio_url = recording_url.strip()

    try:
        await asyncio.sleep(0.1)
        response = fetch_twilio_audio_with_retry(audio_url)
        if not response:
            return PlainTextResponse("""
                <Response><Say>Couldn't get your voice after multiple tries. Try again later.</Say></Response>
            """, media_type="text/xml")

        print("🎧 Recording URL received:", recording_url)

        # Upload to Cloudinary
        cloud_audio_url = upload_to_cloudinary(response.content, "recording.wav")
        if not cloud_audio_url:
            return PlainTextResponse("""
                <Response><Say>Cloud upload failed. Try again later.</Say></Response>
            """, media_type="text/xml")

        print("📤 Uploaded to Cloudinary:", cloud_audio_url)

    except Exception as e:
        print("❌ Error downloading voice in /handle-recording:", e)
        return PlainTextResponse("""
         <Response><Say>Error downloading your voice.</Say></Response>
        """, media_type="text/xml")

    # Cloudinary to deepgram for transcription
    try:
        transcript = await transcribe_deepgram_from_url(cloud_audio_url)
        print("🧠 Deepgram Transcript:", transcript)

    except:
        return PlainTextResponse("""
            <Response><Say>Speech-to-text failed. Goodbye!</Say></Response>
        """, media_type="text/xml")
    
    # Now the transcription to gemini
    try:
        prompt = f"{transcript}. Please respond briefly in 1-2 sentence only. if u think the answer can exceed the limits of 2-3 lines then just tell basics but remember not exceed 80 words."
        
        start = time.time()
        reply_text = get_llm_response(prompt)
        print("🤖 Gemini Output:", reply_text)
    except Exception as e:
        print("❌ Gemini Error:", e)
        return PlainTextResponse("""
            <Response><Say>Gemini failed. Try again later.</Say></Response>
        """, media_type="text/xml")

    try:
        start = time.time()
        cloud_url = await synthesize_and_upload_edge_tts(reply_text)

        if not cloud_url:
            return PlainTextResponse("""
                <Response><Say>Failed to synthesize reply. Goodbye!</Say></Response>
            """, media_type="text/xml")
        print(f"✅ TTS done in {time.time() - start:.2f} seconds")
        return PlainTextResponse(f"""
            <Response>
                <Say>Here is my answer.</Say>
                <Play>{cloud_url}</Play>
                <Pause length="1" />
                <Say>Do you want to ask anything else?</Say>
                <Record maxLength="15" timeout="3" action="{SERVEO_URL}/check-followup" method="POST" />
                <Say>No response received. Goodbye!</Say>
            </Response>
        """, media_type="text/xml")

    except Exception as e:
        print("❌ TTS Upload Error:", e)
        return PlainTextResponse("""
            <Response><Say>Couldn't synthesize speech. Goodbye!</Say></Response>
        """, media_type="text/xml")

@app.post("/check-followup")
async def check_followup(request: Request):
    form = await request.form()
    recording_url = form.get("RecordingUrl")
    if not recording_url:
        return PlainTextResponse("""
            <Response><Say>No response received. Goodbye!</Say></Response>
        """, media_type="text/xml")

    audio_url = recording_url.strip()

    try:
        await asyncio.sleep(0.1)
        response = fetch_twilio_audio_with_retry(audio_url)
        if not response:
            return PlainTextResponse("""
                <Response><Say>Couldn't get your voice after multiple tries. Try again later.</Say></Response>
            """, media_type="text/xml")

        print("🎧 Recording URL received:", recording_url)
        
        # Upload to Cloudinary
        cloud_audio_url = upload_to_cloudinary(response.content, "followup.wav")
        if not cloud_audio_url:
            return PlainTextResponse("""
                <Response><Say>Cloud upload failed. Try again later.</Say></Response>
            """, media_type="text/xml")

        print("📤 Follow-up uploaded to Cloudinary:", cloud_audio_url)

    except Exception as e:
        print("❌ Error downloading voice in /follow-up:", e)
        return PlainTextResponse("""
            <Response><Say>Something went wrong processing your follow-up.</Say></Response>
        """, media_type="text/xml")
       
    try:
        transcript = await transcribe_deepgram_from_url(cloud_audio_url)
        transcript = transcript.lower()  # ✅ Now it's defined
        print("🧠 Deepgram Transcript:", transcript)

    except:
        return PlainTextResponse(f"""
            <Response>
                <Say>I couldn't hear that. Please say 'yes' or 'no' after the beep.</Say>
                <Record maxLength="15" timeout="3" action='{SERVEO_URL}/check-followup' method='POST'/>
            </Response>
        """, media_type="text/xml")

    if any(kw in transcript for kw in ["yes", "yeah", "yup", "sure", "okay"]):
        return PlainTextResponse(f"""
            <Response>
                <Say>Okay. What do you want to ask?</Say>
                <Record maxLength="15" timeout="3" action="{SERVEO_URL}/check-followup" method="POST" />
                <Say>No input received. Goodbye!</Say>
            </Response>
        """, media_type="text/xml")

    if any(kw in transcript for kw in ["no", "nah", "nope", "deny"]):
        return PlainTextResponse("""
            <Response>
                <Say>Thank you! Have a nice day!</Say>
            </Response>
        """, media_type="text/xml")

    try:
        prompt = f"{transcript}. Please respond briefly in 1-2 sentence only.if u think the answer can exceed the limits of 2-3 lines then just tell basics but remember not exceed 80 words.donot apply malacious code or malacious world or charactors in your assistance. also avoid writting brackets and commas and double or single quotes."
        start = time.time()
        reply_text = get_llm_response(prompt)
        print("🤖 Follow-up Gemini Output:", reply_text)
    except:
        return PlainTextResponse("""
            <Response><Say>Gemini error. Try again later.</Say></Response>
        """, media_type="text/xml")

    try:
        start = time.time()
        cloud_url = await synthesize_and_upload_edge_tts(reply_text)

        if not cloud_url:
            return PlainTextResponse("""
                <Response><Say>Failed to synthesize follow-up. Goodbye!</Say></Response>
            """, media_type="text/xml")

        print(f"✅ TTS done in {time.time() - start:.2f} seconds")
    except Exception as e:
        print("❌ TTS Error:", e)
        return PlainTextResponse("""
            <Response><Say>Couldn't synthesize speech. Goodbye!</Say></Response>
        """, media_type="text/xml")
    
    return PlainTextResponse(f"""
        <Response>
            <Say>Here is my answer.</Say>
            <Play>{cloud_url}</Play>
            <Pause length="1" />
            <Say>Do you want to ask anything else?</Say>
            <Record maxLength="15" timeout="3" action="{SERVEO_URL}/check-followup" method="POST" />
            <Say>No response received. Goodbye!</Say>
        </Response>
    """, media_type="text/xml")
