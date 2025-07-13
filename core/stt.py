import httpx
import os
from dotenv import load_dotenv

load_dotenv()

async def transcribe_deepgram_from_url(audio_url: str) -> str:
    """
    This function takes a public URL to an audio file (usually from Cloudinary), and:
        Sends it to Deepgram API
        Gets back the transcribed text
        Returns that transcript (to send to Gemini)
    """
    try:
        deepgram_key = os.getenv("DEEPGRAM_API_KEY")
        headers = {
            "Authorization": f"Token {deepgram_key}"
        }
        params = {
            "model": "nova",  # use "base" if you want cheaper model
            "punctuate": "true",
            "language": "en"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.deepgram.com/v1/listen",
                headers=headers,
                params=params,
                json={"url": audio_url}
            )
            if response.status_code == 200:
                result = response.json()
                return result["results"]["channels"][0]["alternatives"][0]["transcript"]
            else:
                print("❌ Deepgram error:", response.text)
                return ""
    except Exception as e:
        print(f"❌ Deepgram transcription error: {e}")
        return ""
