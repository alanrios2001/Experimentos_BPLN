from asyncio import Semaphore

from provider.openai_provider import Provider
import json
from pathlib import Path

from tqdm import tqdm


class GenerateDataset:
    def __init__(self, provider: Provider):
        self.provider = provider

        self.data_path = Path(__file__).parents[1] / "assets"

        self.dataset_path = self.data_path / 'generated_dataset'
        self.dataset_path.mkdir(parents=True, exist_ok=True)

        with open(self.data_path / 'prompt.json', encoding='utf-8') as f:
            prompts = json.load(f)
        self.system_message = prompts['system_message']
        self.user_message = prompts['user_message']

        with open(self.data_path / 'crawler' / 'book.json', encoding='utf-8') as f:
            self.book = json.load(f)

        try:
            with open(self.dataset_path / 'book_dataset.json', 'r', encoding='utf-8') as f:
                self.dataset = f
        except FileNotFoundError:
            self.dataset = {}

    async def generate_qa_dataset(self):
        for chapter in tqdm(self.book, desc='Gerando perguntas e respostas do capitulo'):
            self.dataset[chapter] = []
            for i, section in tqdm(enumerate(self.book[chapter]), total=len(self.book[chapter]), desc='Etapas das seções do capitulo'):
                text = self.book[chapter][section]

                user_prompt = self.user_message.replace('<TEXTO AQUI>', text)
                answer = await self.provider.generate_response(system_message=self.system_message,
                                                               user_message=user_prompt,
                                                               temperature=0.4,
                                                               response_format={"type": "json_object"}
                                                               )
                json_response = json.loads(answer)
                self.dataset[chapter].extend(json_response['perguntas'])

                with open(self.dataset_path / 'book_dataset.json', 'w', encoding='utf-8') as f:
                    json.dump(self.dataset, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    import asyncio

    async def teste():
        semaphore = Semaphore(1)
        provider = Provider(semaphore)
        generator = GenerateDataset(provider)
        await generator.generate_qa_dataset()

    asyncio.run(teste())
