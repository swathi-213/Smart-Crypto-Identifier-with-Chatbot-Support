# local_llm.py
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.1"

def query_llm(messages):
    """
    messages = list of dicts:
    [
      {"role": "system", "content": "..."},
      {"role": "user", "content": "..."},
      {"role": "assistant", "content": "..."}
    ]
    """

    # Convert chat messages into a single prompt
    prompt = ""
    for msg in messages:
        role = msg["role"].capitalize()
        prompt += f"{role}: {msg['content']}\n"

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt + "Assistant:",
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload, timeout=120)
    response.raise_for_status()

    return response.json()["response"].strip()