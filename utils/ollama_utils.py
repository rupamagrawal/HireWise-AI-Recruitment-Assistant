import requests
import os

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "phi")

def query_ollama(prompt):
    try:
        print(f"\n🧠 Sending prompt to Ollama ({OLLAMA_MODEL})...")
        res = requests.post(
            f"{OLLAMA_BASE_URL}/api/chat",
            json={
                "model": OLLAMA_MODEL,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "stream": False
            },
            timeout=90  # Increase timeout for slow models
        )
        res.raise_for_status()
        result = res.json()
        return result.get("message", {}).get("content", "").strip()

    except requests.exceptions.ReadTimeout:
        print("⚠️ Ollama timed out while waiting for response.")
        return None
    except Exception as e:
        print(f"❌ Ollama request failed: {e}")
        return None
