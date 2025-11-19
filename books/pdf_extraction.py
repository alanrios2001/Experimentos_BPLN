import pdfplumber
import re
import json
import os
from pathlib import Path

dir = Path("./")
saida = Path("../assets")
saida.mkdir(exist_ok=True)

# Observar os sumarios de cada livro e extrair os intervalos entre os capitulos 

book_1 = {
     
}
class book_extractor_pdf:
        def __init__(self,first_pg,last_pg,dados):
            self.first_pg = first_pg
            self.last_pg = last_pg
            self.texto = ""
            self.dados = dados

        def extract_interval(self):
            with pdfplumber.open("livro.pdf") as pdf:
                for p in range(self.first_pg, self.last_pg + 1):
                    pagina = pdf.pages[p - 1]
                    texto_total += (pagina.extract_text() or "") + "\n"
            dados[nome]["texto"] = texto_total.strip()
            
if __name__ == "__main__":
     
    for index, pdf_file in enumerate(dir.glob("*.pdf")):
        nome = pdf_file.stem
        dados = {nome: {"texto": ""}}
        book = book_extractor_pdf()
        book.extract_interval