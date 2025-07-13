# Voice AI Call System 🎤🤖

A sophisticated voice-based AI assistant that integrates with Twilio for phone calls, Google's Gemini AI for intelligent responses, Deepgram for speech-to-text, and Edge TTS for text-to-speech conversion.

## ✨ Features

- 🎤 **Voice-to-text conversion** using Deepgram API
- 🤖 **AI-powered conversations** using Google's Gemini AI
- 🗣️ **Natural text-to-speech** using Microsoft Edge TTS
- ☁️ **Cloud storage** for audio files using Cloudinary
- 📞 **Phone call integration** via Twilio
- 🔄 **Conversation memory** and context retention
- 🌐 **Automatic tunnel setup** with Cloudflare
- 🧩 **Modular architecture** for easy maintenance

## 📁 Project Structure

```
project_root/
│
├── main.py                  # 🚀 FastAPI app with Twilio endpoints
├── call_user.py             # 📞 Triggers Twilio call
├── servo_url.py             # 🌐 Cloudflare tunnel management & URL injection
├── core/                    # 🧩 Core business logic modules
│   ├── __init__.py          # 📦 Package initialization
│   ├── llm_chain.py         # 🤖 Gemini LLM + LangChain logic
│   ├── cloudinary.py        # ☁️ Cloudinary upload function
│   ├── tts.py               # 🗣️ Edge TTS synthesis and upload
│   ├── stt.py               # 🎧 Deepgram transcription
│   └── utils.py             # 🔧 Helper functions (Twilio audio fetching)
├── templates/
│   └── index.html           # 🌐 Web UI page
├── static/                  # 📁 Audio files storage
├── .env                     # 🔐 Your API keys and secrets
├── .env.example             # 📋 Example environment file
├── requirements.txt         # 📦 Python dependencies
└── test_imports.py          # 🧪 Import validation script
```

## 🛠️ Prerequisites

- **Python 3.8+**
- **Cloudflare Tunnel** (cloudflared installed)
- **Twilio account** with phone number
- **Google Cloud account** with Gemini AI API access
- **Deepgram API account**
- **Cloudinary account**

## ⚡ Quick Setup

### 1. Clone and Install Dependencies

```powershell
# Navigate to your project
cd "C:\Users\nagpa\OneDrive\Desktop\gemini - Copy"

# Install all dependencies
"C:/Users/nagpa/OneDrive/Desktop/gemini - Copy/venv/Scripts/pip.exe" install -r requirements.txt
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and fill in your API credentials:

```env
# API Keys
GOOGLE_API_KEY=your_google_api_key_here
DEEPGRAM_API_KEY=your_deepgram_api_key_here

# Twilio Configuration
TWILIO_SID=your_twilio_sid_here
TWILIO_TOKEN=your_twilio_token_here
TWILIO_PHONE_NUMBER=+1234567890
TARGET_PHONE_NUMBER=+0987654321

# Cloudinary Configuration
CLOUDINARY_CLOUD_NAME=your_cloud_name_here
CLOUDINARY_API_KEY=your_api_key_here
CLOUDINARY_API_SECRET=your_api_secret_here
```

### 3. Test Your Setup

```powershell
# Test if all imports work correctly
"C:/Users/nagpa/OneDrive/Desktop/gemini - Copy/venv/Scripts/python.exe" test_imports.py
```

## 🚀 Running the Application

### Method 1: Automatic Setup (Recommended)

```powershell
# 1. Start Cloudflare tunnel (this auto-updates URLs in files)
"C:/Users/nagpa/OneDrive/Desktop/gemini - Copy/venv/Scripts/python.exe" servo_url.py

# 2. In another terminal, start FastAPI
"C:/Users/nagpa/OneDrive/Desktop/gemini - Copy/venv/Scripts/python.exe" uvicorn main:app --reload

# 3. Make a test call
"C:/Users/nagpa/OneDrive/Desktop/gemini - Copy/venv/Scripts/python.exe" call_user.py
```

## 🔧 How It Works

### 🔄 **Call Flow:**
1. **Call Initiation** → Twilio hits `/voice` endpoint
2. **Name Capture** → User's name processed via speech-to-text
3. **Question Processing** → Questions converted to text → sent to Gemini AI
4. **Response Generation** → AI response converted back to speech
5. **Follow-up Handling** → Supports multiple questions with memory

### 🧩 **Modular Architecture:**

# Each core module handles specific functionality:
# - core.llm_chain: AI conversation logic
# - core.cloudinary: File upload handling  
# - core.tts: Text-to-speech conversion
# - core.stt: Speech-to-text processing
# - core.utils: Helper functions
```


## ⚙️ Configuration

### 🎵 **Audio Settings:**
- **Recording length:** 15 seconds for questions, 4 seconds for name
- **Audio format:** WAV for processing, MP3 for TTS output
- **Speech timeout:** 3 seconds

### 🤖 **AI Settings:**
- **Model:** Gemini-1.5-flash
- **Response limit:** 80 words maximum
- **Memory:** Conversation context maintained throughout session

## 🔍 Troubleshooting

### Common Issues:

1. **Import Errors:**
   ```powershell
   # Test imports
   "C:/Users/nagpa/OneDrive/Desktop/gemini - Copy/venv/Scripts/python.exe" test_imports.py
   ```

2. **Tunnel Not Working:**
   - Ensure cloudflared is installed at `C:\Program Files\cloudflared\cloudflared.exe`
   - Check if port 8000 is available

3. **uvicorn or any other library not imported**
  use this command: **venv\Scripts\activate**
 and thn run the command in venv 

 if not thn download all the libraries and all dependies required for the project by :
 pip install -r requirements.txt


4. **API Errors:**
   - Validate all API keys in `.env` file
   - Ensure APIs have proper permissions

### 📊 **Debugging Logs:**
The application provides detailed logging:
- 🎧 Audio processing
- 🧠 Speech-to-text conversion  
- 🤖 AI response generation
- 🔊 Text-to-speech conversion
- 📤 Cloud uploads

## 🛡️ Security Notes

- Keep your `.env` file secure and never commit it to version control
- All API keys should have minimal required permissions
- Consider rate limiting for production use


## 📄 License

This project is licensed under the MIT License.

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs for error messages  
3. Ensure all API credentials are correctly configured
4. Test individual modules using the test script

---

**Built with ❤️ using FastAPI, Gemini AI, and modern cloud services**

2. Set up your tunnel (update SERVEO_URL in `serveo_url.py`)

3. Trigger a call:
   ```bash
   python call_user.py
   ```

## Features

- Voice conversation with Gemini AI
- Speech-to-text using Deepgram
- Text-to-speech using Edge TTS
- Audio file handling via Cloudinary
- Session memory for conversations
- Follow-up question handling