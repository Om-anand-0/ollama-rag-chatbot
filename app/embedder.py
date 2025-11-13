import requests

class Embedder:
    MODEL = "nomic-embed-text"
    URL = "http://localhost:11434/api/embeddings"

    @staticmethod
    def embed(text: str):
        payload = {
            "model": Embedder.MODEL,
            "prompt": text  # ✅ Correct for Ollama 0.12.10
        }

        response = requests.post(Embedder.URL, json=payload).json()
        return response.get("embedding", [])
