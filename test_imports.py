# Test script to verify all imports work correctly
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test all core module imports"""
    try:
        print("🧪 Testing core module imports...")
        
        # Test LLM chain import
        from core.llm_chain import get_llm_response
        print("✅ core.llm_chain imported successfully")
        
        # Test Cloudinary import
        from core.cloudinary import upload_to_cloudinary
        print("✅ core.cloudinary imported successfully")
        
        # Test TTS import
        from core.tts import synthesize_and_upload_edge_tts
        print("✅ core.tts imported successfully")
        
        # Test STT import
        from core.stt import transcribe_deepgram_from_url
        print("✅ core.stt imported successfully")
        
        # Test utils import
        from core.utils import fetch_twilio_audio_with_retry
        print("✅ core.utils imported successfully")
        
        print("\n🎉 All imports successful! Your main.py should work correctly.")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    test_imports()
