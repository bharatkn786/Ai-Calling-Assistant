import edge_tts
import io
from .cloudinary import upload_to_cloudinary

async def synthesize_and_upload_edge_tts(text: str) -> str:
    """
    This function takes text (a reply from ChatGPT/Gemini) and:
        Synthesizes it into speech using Microsoft Edge TTS
        Uploads the generated audio (MP3) to Cloudinary
        Returns the Cloudinary URL for the audio so Twilio can play it in the call
    """
    try:
        communicate = edge_tts.Communicate(text, "en-US-JennyNeural")
        mp3_buffer = io.BytesIO()

        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                mp3_buffer.write(chunk["data"])

        mp3_buffer.seek(0)  # Reset buffer pointer

        # Upload to Cloudinary
        cloud_url = upload_to_cloudinary(mp3_buffer.read(), "reply.mp3")
        return cloud_url
    except Exception as e:
        print(f"❌ TTS synthesis error: {e}")
        return None
