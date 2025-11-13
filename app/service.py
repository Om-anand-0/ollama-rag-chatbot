import requests
import os
from qdrant_client import QdrantClient
from app.embedder import Embedder

localHost = os.getenv("OLLAMA_HOST", "http://localhost:11434/api/chat")
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")

retriever = QdrantClient(url=QDRANT_URL)

def find_context(query):
    query_vec = Embedder.embed(query)
    result = retriever.search(
        collection_name="genzgpt_kb",
        query_vector=query_vec,
        limit=4
    )
    return "\n".join([hit.payload["text"][:400] for hit in result])


class ChatManager:
    def __init__(self):
        self.chat = [
            {"role": "system", "content": "You are a Gen Z AI assistant. Use light emojis and friendly tone."}
        ]

    def add_user_message(self, message):
        context = find_context(message)
        enhanced = f"Relevant knowledge:\n{context}\n\nUser: {message}"
        self.chat.append({"role": "user", "content": enhanced})

    def generate_response(self):
        # keep conversation tight
        if len(self.chat) > 12:
            self.chat = self.chat[:1] + self.chat[-10:]

        payload = {
            "model": "phi3:mini",
            "prompt": "\n".join([m["content"] for m in self.chat]),
            "temperature": 0.7,
            "num_predict": 200,
            "stream": False
        }

        r = requests.post(localHost, json=payload)
        raw = r.text.strip()

        # For non-stream mode, Ollama returns exactly one JSON object
        data = r.json()
        reply = data.get("response", "").strip()

        self.chat.append({"role": "assistant", "content": reply})
        return reply


    def reset(self):
        self.chat = [
            {"role": "system", "content": "You are a Gen Z AI assistant. Use light emojis and friendly tone."}
        ]
