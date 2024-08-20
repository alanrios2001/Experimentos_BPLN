from asyncio import Semaphore

from provider.openai import Provider
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

    def generate_dataset(self):
        for chapter in self.book:
            for section in self.book[chapter]:
                user_message = self.book[chapter][section]
                print(user_message)
                print(len(user_message))
                input()


if __name__ == "__main__":
    semaphore = Semaphore(3)
    provider = Provider(semaphore)
    generator = GenerateDataset(provider)
    generator.generate_dataset()