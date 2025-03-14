import json
from asyncio import Semaphore
from pathlib import Path

from langchain_text_splitters import TokenTextSplitter
from tokenizers import Tokenizer
from tqdm import tqdm
from transformers import AutoTokenizer

from provider.openai_provider import Provider


class ComputerDataset:
    def __init__(self, provider: Provider):
        self.provider = provider
        self.data_path = Path(__file__).parents[1] / "assets"

        self.dataset_path = self.data_path / "dataset" / "generated_dataset"
        self.dataset_path.mkdir(parents=True, exist_ok=True)
        with open(self.data_path / "prompt.json", encoding="utf-8") as f:
            prompts = json.load(f)

        self.system_message = prompts["system_message2"]
        self.user_message = prompts["user_message"]

        with open("content_wikipedia_computing.json", "r", encoding="utf-8") as f:
            self.computing_pages = json.load(f)

        max_text_len = 1024
        tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-72B-Instruct")
        self.splitter = TokenTextSplitter.from_huggingface_tokenizer(tokenizer, chunk_size=max_text_len, chunk_overlap=50)

        self.dataset = {}


    async def generate_computer_dataset(self):
        for page in tqdm(self.computing_pages, desc="Gerando perguntas e respostas de computação"):
            title = page["title"]
            text = page["text"]
            self.dataset[title] = []
            text_pieces = self.splitter.split_text(text)
            for text_piece in text_pieces:
                user_message = self.user_message.replace("<TEXTO AQUI>", text_piece)
                try:
                    await self.get_and_process_answer(user_message, title)
                except Exception as e:
                    if "Failed to generate JSON" in str(e):
                        await self.get_and_process_answer(user_message, title)


    async def get_and_process_answer(self, user_message: str, title: str):
        answer = await self.provider.generate_response(
            system_message=self.system_message,
            user_message=user_message,
            temperature=0.2,
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
        json_response = json.loads(answer)
        self.dataset[title].extend(json_response["perguntas"])
        with open(self.dataset_path / f"computer_dataset.json", "w", encoding="utf-8") as f:
            json.dump(self.dataset, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    import asyncio

    semaphore = Semaphore(1)
    provider = Provider(semaphore)
    dataset = ComputerDataset(provider)
    asyncio.run(dataset.generate_computer_dataset())
