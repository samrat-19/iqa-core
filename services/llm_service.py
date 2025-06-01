import requests

API_URL = "http://localhost:11434/api/generate"
HEADERS = {"Content-Type": "application/json"}
EMBED_API_URL = "http://localhost:11434/api/embeddings"
EMBED_HEADERS = {"Content-Type": "application/json"}

def call_llm(prompt, max_retries=3):
    """Generic function to call LLM API with retries."""
    body = {"model": "llama3.1", "prompt": prompt, "stream": False}

    for _ in range(max_retries):
        response = requests.post(API_URL, json=body, headers=HEADERS)
        if response.status_code == 200:
            return response.json().get("response", "")

    return ""  # Return empty string if all retries fail

def call_embedding(text, max_retries=3):
    """Call embedding API with retries, using nomic-embed-text."""
    body = {"model": "nomic-embed-text", "prompt": text}

    for _ in range(max_retries):
        response = requests.post(EMBED_API_URL, json=body, headers=EMBED_HEADERS)
        if response.status_code == 200:
            data = response.json()
            # The embedding vector is usually under 'embedding' key
            if "embedding" in data:
                return data["embedding"]
            # Some APIs may return embeddings under 'data' or other keys, adjust if needed
        # optionally add delay or logging here

    return None  # Return None if all retries fail
