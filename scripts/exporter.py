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
    def export_Digger_dataset(self):
        system_message = "Considere dois grupos de consumidores: aqueles que fazem compras online e aqueles que compram presencialmente no varejo. Esses consumidores podem ter diferentes níveis de conhecimento sobre o Código de Defesa do Consumidor (CDC), variando desde nenhum conhecimento até um conhecimento básico ou intermediário, levando em consideração suas experiências de compra e possíveis dúvidas. As perguntas devem simular situações reais em que eles possam precisar de orientação jurídica ou mais detalhes sobre como garantir seus direitos. Foque em questões práticas e cotidianas relacionadas ao CDC e às situações que esses consumidores poderiam enfrentar. NUNCA mencione explicitamente o TRECHO nas perguntas ou respostas. As perguntas devem ser autocontidas, ou seja, não devem exigir acesso ao trecho para serem respondidas; Formule perguntas de forma técnica; As perguntas devem ser desafiadoras, exigindo um alto nível de compreensão do assunto; Embase as respostas com LEIS, ARTIGOS, RESOLUÇÕES, Acordão, integrando isso na RESPOSTA de forma explícita. Por exemplo: O Código Penal (art. X), prevê a pena...; SEMPRE que existir menção a Lei ou Artigo, integre na RESPOSTA; Não inclua opiniões pessoais ou especulações nas respostas; NÃO COLOQUE (Fonte:), (Referências:), (Baseado no trecho:), (Base legal:) ou similares. NÃO CITE AUTORES. NÃO CITE O TRECHO;"
        with open(
            self.dataset_path / "generated_dataset" / "Digger_llama_dataset.json",
            encoding="utf-8",
        ) as f:
            Digger_llama_dataset = json.load(f)

        with open(
            self.exporter_data_path / "Digger_llama_sharegpt_dataset", "w", encoding="utf-8"
        ) as f:
            for division in Digger_llama_dataset:
                for section in Digger_llama_dataset[division]:
                    for qa in section:
                        f.write(
                            json.dumps(
                                {
                                    "conversations": [
                                        {'from': 'system', 'value': system_message},
                                        {'from': 'human', 'value': qa["Pergunta"]},
                                        {'from': 'gpt', 'value': qa["Resposta"]},
                                    ]  
                                },
                                ensure_ascii=False,
                            ) + "\n"
                        )          

if __name__ == "__main__":
    exporter = Exporter()
    exporter.export_book_dataset()
