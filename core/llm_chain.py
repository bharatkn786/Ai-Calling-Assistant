import os
from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_google_genai import ChatGoogleGenerativeAI

# ✅ Load .env file
load_dotenv()

# ✅ Get API Key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise RuntimeError("❌ GOOGLE_API_KEY not found in environment variables.")

# ✅ Initialize LLM with API Key
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=GOOGLE_API_KEY
)

# ✅ Setup memory + conversation chain
memory = ConversationBufferMemory(return_messages=True)
conversation_chain = ConversationChain(llm=llm, memory=memory)

# ✅ Sync function (since Gemini is not async-compatible yet)
def get_llm_response(prompt: str) -> str:
    """Get response from Gemini LLM with memory"""
    try:
        result = conversation_chain.invoke(prompt)

        # Handle both possible output types
        if isinstance(result, dict):
            return result.get("response", "").strip()
        return str(result).strip()

    except Exception as e:
        print(f"❌ Gemini Error: {e}")
        return "Sorry, something went wrong with the AI."
