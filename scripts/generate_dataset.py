from asyncio import Semaphore

from provider.openai_provider import Provider
import json
from pathlib import Path


class GenerateDataset:
    def __init__(self, provider: Provider):
        self.provider = provider

        self.data_path = Path(__file__).parents[1] / "assets"

        with open(self.data_path / 'prompt.json', encoding='utf-8') as f:
            prompts = json.load(f)
        self.system_message = prompts['system_message']
        self.user_message = prompts['user_message']

        with open(self.data_path / 'crawler' / 'book.json', encoding='utf-8') as f:
            self.book = json.load(f)

    async def generate_dataset(self):
        for chapter in self.book:
            for section in self.book[chapter]:
                text = self.book[chapter][section]

                user_prompt = self.user_message.replace('<TEXTO AQUI>', text)
                answer = await self.provider.generate_response(system_message=self.system_message,
                                                               user_message=user_prompt)
                print(answer)
                input('')


if __name__ == "__main__":
    import asyncio

    async def teste():
        semaphore = Semaphore(1)
        provider = Provider(semaphore)
        generator = GenerateDataset(provider)
        await generator.generate_dataset()

    asyncio.run(teste())
