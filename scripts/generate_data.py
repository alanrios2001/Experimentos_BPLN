from openai import OpenAI
from config import settings
import asyncio

class Provider:
    def __init__(self, semaphore):
        self.model_name = 'meta-llama/Meta-Llama-3-70B-Instruct'
        self.api_key = HF_API_KEY
        self.client = AsyncInferenceClient(self.model_name, token=self.api_key)
        self.semaphore = semaphore

    async def generate_response(self, system_prompt, user_message, temperature=0.5, top_p=0.9):
        retry_attempts = 10  # Número de tentativas de retentativa
        while retry_attempts > 0:
            try:
                async with self.semaphore:
                    messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_message}]
                    response = await self.client.chat_completion(messages, max_tokens=2048, temperature=temperature, top_p=top_p)
                    return response.choices[0]["message"]["content"]
            except Exception as e:
                if "429" in str(e) and retry_attempts > 0:
                    print(f"Too many requests. Retrying in 60 seconds. Attempts left: {retry_attempts}")
                    await asyncio.sleep(60)
                    retry_attempts -= 1
                else:
                    raise e