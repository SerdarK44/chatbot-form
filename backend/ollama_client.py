import requests

class OllamaClient:
    def __init__(self, base_url="http://localhost:11434", model_name="erdiari/llama3-turkish:latest"):
        self.api_url = f"{base_url}/api/generate"
        self.model_name = model_name

    def ask(self, message):
        payload = {
            "model": self.model_name,
            "prompt": message,
            "stream": False
        }
        response = requests.post(self.api_url, json=payload)
        response.raise_for_status()
        return response.json()["response"]
