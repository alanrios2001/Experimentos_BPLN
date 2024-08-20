import requests
import json
from bs4 import BeautifulSoup
from pathlib import Path

TOPICS_TO_IGNORE = [
    "Vale a pena relembrar",
    "Considerações finais",
    "Agradecimentos",
    "Ao infinito e além",
    "Em resumo…",
    "Exercícios",
    "Para Concluir",
    "Tendências",
    "Conclusões provisórias",
    "Aplicações de PLN na Saúde",
    "Conclusão",
    "Qual é melhor: constituência ou dependência?",
    "Recursos e ferramentas para o português",
    "Visualização, anotação e edição de treebanks",
    "Por onde começar?",
    "Uso Responsável e Boas Práticas"
]

CAPS_TO_IGNORE = [
    "apendice",
    "cap-caracteres-palavras",
]


class BookExtractor:
    def __init__(self):
        self.base_url = "https://brasileiraspln.com/livro-pln/2a-edicao/"
        self.cap_links = []
        self.book = {}

        self.output_path = Path(__file__).parents[1] / "assets" / "crawler"
        self.output_path.mkdir(parents=True, exist_ok=True)

    def run(self):
        self.get_cap_links()
        self.extract_cap_content()
        self.save_json()

    def get_cap_links(self):
        response = requests.get(self.base_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser", from_encoding="utf-8")
        sidebar = soup.find("nav", {"id": "quarto-sidebar"})
        for item in sidebar.find_all("a", {"class": "sidebar-link"}):
            if "data-bs-toggle" not in item.attrs and "/cap-" in item["href"]:
                self.cap_links.append(self.base_url + item["href"])

    def extract_cap_content(self):
        for link in self.cap_links:
            capitle_name = link.split("/")[-1].replace(".html", "")

            if not any([cap.lower() in capitle_name.lower() for cap in CAPS_TO_IGNORE]):
                response = requests.get(link)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, "html.parser", from_encoding="utf-8")
                content = soup.find("main", {"class": "content"})
                chapter_titles = content.find_all("h2")
                chapter_content = {}
                for title in chapter_titles:
                    cleaned_title = title.text.strip()

                    if not any([topic.lower() in cleaned_title.lower() for topic in TOPICS_TO_IGNORE]):
                        if title.find("span", class_="header-section-number"):
                            title.find("span", class_="header-section-number").decompose()

                        section_content = []
                        current = title.find_next_sibling()

                        while current and current.name != "h2":
                            if current.name == "p":
                                section_content.append(current.text.strip())
                            current = current.find_next_sibling()

                        section_content_str = " ".join(section_content)

                        if len(section_content_str) > 800:
                            chapter_content[' '.join(cleaned_title.split(' ')[1:])] = " ".join(section_content)

                        if chapter_content:
                            self.book[capitle_name] = chapter_content

    def save_json(self):
        file_path = self.output_path / "book.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(self.book, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    instance = BookExtractor()
    instance.run()
