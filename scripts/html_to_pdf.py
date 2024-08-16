import requests
import json
from bs4 import BeautifulSoup
from pathlib import Path


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
            response = requests.get(link)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser", from_encoding="utf-8")
            content = soup.find("main", {"class": "content"})
            chapter_titles = content.find_all("h2")
            chapter_content = {}
            for title in chapter_titles:
                if title.find("span", class_="header-section-number"):
                    title.find("span", class_="header-section-number").decompose()
                cleaned_title = title.text.strip()
                section_content = []
                current = title.find_next_sibling()
                while current and current.name != "h2":
                    if current.name == "p":
                        section_content.append(current.text.strip())
                    current = current.find_next_sibling()
                chapter_content[cleaned_title] = " ".join(section_content)
            self.book[link.split("/")[-1].replace(".html", "")] = chapter_content

    def save_json(self):
        file_path = self.output_path / "book.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(self.book, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    instance = BookExtractor()
    instance.run()
