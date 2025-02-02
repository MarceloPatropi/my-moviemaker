from openai import OpenAI
from dotenv import load_dotenv
import os

class OpenAIChatGPT:
    def __init__(self, api_key=None):
        load_dotenv()
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        OpenAI.api_key = self.api_key
        self.client = OpenAI(
            api_key=self.api_key
        )
        self.model = "gpt-4o"
        self.store = True

    def generate_response(self, prompt, model="text-davinci-003", max_tokens=150, temperature=0.7):
        response = self.client.chat.completions.create(
            model = self.model,
            store = self.store,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content

# Exemplo de uso
if __name__ == "__main__":
    chatgpt = OpenAIChatGPT()
    prompt = "Explique a teoria da relatividade de forma simples."
    response = chatgpt.generate_response(prompt)
    print(response)
