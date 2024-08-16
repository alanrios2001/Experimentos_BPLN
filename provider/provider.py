from openai import AsyncOpenAI
from config import settings
from asyncio import Semaphore
import asyncio

HF_API_KEY = settings.provider.HF_API_KEY
GROQ_API_KEY = settings.provider.GROQ_API_KEY
OPENAI_API_KEY = settings.provider.OPENAI_API_KEY

GROQ_ENDPOINT = settings.provider.GROQ_ENDPOINT
OPENAI_ENDPOINT = settings.provider.OPENAI_ENDPOINT
HF_ENDPOINT = settings.provider.HF_ENDPOINT

USE_GROQ = settings.provider.USE_GROQ
USE_OPENAI = settings.provider.USE_OPENAI
USE_HF = settings.provider.USE_HF

MAX_CONCURRENT_TASKS = 10


class Provider:

    def __init__(
        self,
        semaphore: Semaphore,
        model_name: str = (
            "llama3-8b-8192"
            if USE_GROQ
            else ("gpt-4o" if USE_OPENAI else "meta-llama/Meta-Llama-3.1-8B-Instruct")
        ),
    ):
        self.model_name = model_name
        self.api_key = HF_API_KEY
        self.client = AsyncOpenAI(
            api_key=(
                GROQ_API_KEY
                if USE_GROQ
                else (OPENAI_API_KEY if USE_OPENAI else HF_API_KEY)
            ),
            base_url=(
                GROQ_ENDPOINT
                if USE_GROQ
                else (OPENAI_ENDPOINT if USE_OPENAI else HF_ENDPOINT)
            ),
        )

        self.semaphore = semaphore

    async def generate_response(
        self,
        system_message: str,
        user_message: str,
        temperature: float = 0.2,
        top_p: float = 0.9,
    ):
        retry_attempts = 10  # Número de tentativas de retentativa
        while retry_attempts > 0:
            try:
                async with self.semaphore:
                    messages = [
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": user_message},
                    ]
                    response = await self.client.chat.completions.create(
                        model=self.model_name,
                        messages=messages,
                        max_tokens=2048,
                        temperature=temperature,
                        top_p=top_p,
                    )
                    return response.choices[0].message.content
            except Exception as e:
                if "429" in str(e) and retry_attempts > 0:
                    print(
                        f"Too many requests. Retrying in 60 seconds. Attempts left: {retry_attempts}"
                    )
                    await asyncio.sleep(60)
                    retry_attempts -= 1
                else:
                    raise e


if __name__ == "__main__":
    semaphore = Semaphore(MAX_CONCURRENT_TASKS)
    provider = Provider(semaphore)
    system_message = "Olá! Como posso te ajudar hoje?"

    response = asyncio.run(
        provider.generate_response(
            "Você é um chatbot que entende muito de todas as áreas e responde a perguntas de forma precisa.",
            "Qual é o melhor modelo de linguagem?",
        )
    )
    print(response)
