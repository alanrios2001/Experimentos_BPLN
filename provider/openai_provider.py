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

MAX_CONCURRENT_TASKS = 1


class Provider:

    def __init__(
        self,
        semaphore: Semaphore,
        model_name: str = (
            "llama-3.3-70b-versatile"
            if USE_GROQ
            else ("gpt-4o" if USE_OPENAI else "Qwen/Qwen2.5-72B-Instruct")
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
        temperature: float = 0.4,
        top_p: float = 0.9,
        response_format: dict | None = None,
    ):
        retry_attempts = 10  # Número de tentativas de retentativa
        while retry_attempts > 0:
            try:
                async with self.semaphore:
                    messages = [
                        {
                            "role": "system",
                            "content": [
                                {
                                    "type": "text",
                                    "text": system_message
                                }
                            ]
                        },
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": user_message
                                }
                            ]
                        }
                    ]
                    response = await self.client.chat.completions.create(
                        model=self.model_name,
                        messages=messages,
                        max_tokens=2048,
                        temperature=temperature,
                        top_p=top_p,
                        response_format=response_format,
                    )
                    return response.choices[0].message.content
            except Exception as e:
                if "429" in str(e) and retry_attempts > 0:
                    print(
                        f"Too many requests. Retrying in 60 seconds. Attempts left: {retry_attempts}"
                    )
                    await asyncio.sleep(60)
                    #retry_attempts -= 1
                else:
                    raise e


if __name__ == "__main__":
    semaphore = Semaphore(MAX_CONCURRENT_TASKS)
    provider = Provider(semaphore)
    system_message = "Olá! Como posso te ajudar hoje?"

    response = asyncio.run(
        provider.generate_response(
            "Você é um chatbot que extrai perguntas e repostas a partir do trecho de um livro",
            "**Trove** é um agregador e serviço de banco de dados de biblioteca online australiano que inclui documentos de texto completo, , dados bibliográficos e de acervos de itens que não estão disponíveis digitalmente e um mecanismo de pesquisa facetado gratuito como ferramenta de descoberta. A base de dados inclui arquivos, imagens, jornais, documentos oficiais, sites arquivados, manuscritos e outros tipos de dados.",
            response_format={
                "type": "json",
                "value": {
                    "properties": {
                        "perguntas": {
                            "description": "Perguntas e respostas sobre o livro.",
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "pergunta": {"description": "Pergunta sobre o livro.", "type": "string"},
                                    "resposta": {"description": "Resposta da pergunta.", "type": "string"}
                                },
                                "required": ["pergunta", "resposta"]
                            }
                        }
                    }
                },
            }
        )
    )
    print(response)
