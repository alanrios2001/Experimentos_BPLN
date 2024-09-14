import json
from pathlib import Path


class Exporter:
    def __init__(self):
        self.exporter_data_path = Path(__file__).parents[1] / "assets" / "exporter"
        self.dataset_path = Path(__file__).parents[1] / "assets" / "dataset"

        self.exporter_data_path.mkdir(parents=True, exist_ok=True)

    def export_book_dataset(self):
        system_message = "Você é um robô que responde a perguntas sobre PLN (Processamento de Linguagem Natural)."
        with open(
            self.dataset_path / "generated_dataset" / "book_dataset.json",
            encoding="utf-8",
        ) as f:
            book_dataset = json.load(f)

        # insert data on sharegpt jsonl.
        # {"conversations": [{"from": "...", "value": "..."}]}
        with open(
            self.exporter_data_path / "dataset.jsonl", "w", encoding="utf-8"
        ) as f:
            for chapter in book_dataset:
                for section in book_dataset[chapter]:
                    f.write(
                        json.dumps(
                            {
                                "conversations": [
                                    {'from': 'system', 'value': system_message},
                                    {'from': 'human', 'value': section["pergunta"]},
                                    {'from': 'gpt', 'value': section["resposta"]},
                                ]
                            },
                            ensure_ascii=False,
                        ) + "\n"
                    )


if __name__ == "__main__":
    exporter = Exporter()
    exporter.export_book_dataset()
