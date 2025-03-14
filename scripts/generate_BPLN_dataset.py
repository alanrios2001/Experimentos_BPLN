from asyncio import Semaphore
from provider.openai_provider import Provider
import json
from pathlib import Path

from tqdm import tqdm


class BPLNDataset:
    def __init__(self, provider: Provider):
        self.provider = provider

        self.data_path = Path(__file__).parents[1] / "assets"

        self.dataset_path = self.data_path / "dataset" / "generated_dataset"
        self.dataset_path.mkdir(parents=True, exist_ok=True)

        with open(self.data_path / "prompt.json", encoding="utf-8") as f:
            prompts = json.load(f)
        self.system_message = prompts["system_message"]
        self.user_message = prompts["user_message"]

        with open(self.data_path / "crawler" / "book.json", encoding="utf-8") as f:
            self.book = json.load(f)

        # carregamento do estado da geracao do dataset
        self.init_len = len(self.book)

        self.dataset = {}
        self.load_dataset()
        self.update_book_state()

        self.updt_len = len(self.book)

    async def generate_qa_dataset(self):
        for chapter in tqdm(
            self.book,
            desc="Gerando perguntas e respostas do capitulo",
            initial=self.init_len - self.updt_len,
            total=self.init_len,
        ):
            self.dataset[chapter] = []
            for i, section in tqdm(
                enumerate(self.book[chapter]),
                total=len(self.book[chapter]),
                desc="Etapas das seções do capitulo",
            ):
                text = self.book[chapter][section]
                user_message = self.user_message.replace("<TEXTO AQUI>", text)

                try:
                    await self.get_and_process_answer(user_message, chapter)
                except Exception as e:
                    if "Failed to generate JSON" in str(e):
                        await self.get_and_process_answer(user_message, chapter)

    async def get_and_process_answer(self, user_message: str, chapter: str):
        answer = await self.provider.generate_response(
            system_message=self.system_message,
            user_message=user_message,
            temperature=0.2,
            response_format={"type": "json_object"},
        )
        json_response = json.loads(answer)

        self.dataset[chapter].extend(json_response["perguntas"])

        with open(self.dataset_path / "book_dataset.json", "w", encoding="utf-8") as f:
            json.dump(self.dataset, f, ensure_ascii=False, indent=4)

    def load_dataset(self):
        try:
            with open(
                self.dataset_path / "book_dataset.json", "r", encoding="utf-8"
            ) as f:
                self.dataset = json.load(f)
        except FileNotFoundError:
            print("Checkpoint do dataset não encontrado")
            return

    def update_book_state(self):
        if not self.dataset:
            return

        chapters = list(self.dataset.keys())

        for chapter in chapters[:-1]:
            del self.book[chapter]

        del self.book[chapters[-1]]


if __name__ == "__main__":
    import asyncio

    async def teste():
        semaphore = Semaphore(1)
        provider = Provider(semaphore)
        generator = BPLNDataset(provider)
        await generator.generate_qa_dataset()

    asyncio.run(teste())
