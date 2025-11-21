import json
import os
from pypdf import PdfReader

# Seus dados JSON estruturados
biblioteca_json = {
    "./1. Linguística Computacional Teoria & Prática (Othero e Menuzzi).pdf":{
        "TECNOLOGIA E LINGUAGEM": [14,20],
        "TRABALHOS EM LINGUÍSTICA COMPUTACIONAL":[21,35],
        "DESENVOLVENDO UM PARSER SINTÁTICO — PARTE I: ALGUMAS NOÇÕES TEÓRICAS IMPORTANTES": [36,63],
        "DESENVOLVENDO UM PARSER SINTÁTICO — PARTE II: “COLOCANDO A MÃO NA MASSA”": [64,75],
        "NOSSA GRAMÁTICA": [76,87]
    },
    "./2. Linguística Computacional (Claudia Freitas).pdf":{
         "PALAVRAS INICIAIS": [3,8],
         "UMA VISÃO PANORÂMICA DA LINGUÍSTICA COMPUTACIONAL": [9,29],
         "LINGUÍSTICA COMPUTACIONAL E LINGUÍSTICA: UM POUCO DE HISTÓRIA": [30,36],
         "RECURSOS LEXICAIS EM FOCO: LÉXICOS COMPUTACIONAIS, ONTOLOGIAS": [37,49],
         "PREPARATIVOS PARA UM PROCESSAMENTO COMPUTACIONAL DA LÍNGUA (OU: PRÉ-PROCESSAMENTO TAMBÉM É PROCESSAMENTO)": [50,54],
         "ANOTAÇÃO: PRINCIPAIS TIPOS": [55,92],
         "ANOTAÇÃO: BASTIDORES": [93,102],
         "ANÁLISE DE ERROS": [103,107],
         "MAIS ALGUMAS PALAVRAS SOBRE LINGUÍSTICA E LINGUÍSTICA COMPUTACIONAL": [108,110]
    },
    "./3. Speech and Language Processing (jurafsky).pdf":{
        "Large Language Models":{
            "Words and Tokens": [12,44],
            "N-gram Language Models":[45,68],
            "Logistic Regression": [69,102],
            "Embeddings":[103,126],
            "Neural Networks": [127,152],
            "Large Language Models":[153,178],
            "Transformers":[179,204],
            "Masked Language Models":[205,223],
            "Post-training: Instruction Tuning, Alignment, and Test-Time Compute":[224,240],
            "Retrieval-based Models": [241,260],
            "Machine Translation":[261,286],
            "RNNs and LSTMs": [287,312],
            "Phonetics and Speech Feature Extraction": [313,341],
            "Automatic Speech Recognition":[342,368],
            "Text-to-Speech": [369,382]
        },
        "Annotating Linguistic Structure":{
            "Sequence Labeling for Parts of Speech and Named Entities": [386,410],
            "Context-Free Grammars and Constituency Parsing":[411,434],
            "Dependency Parsing": [435,458],
            "Information Extraction: Relations, Events, and Time": [459,484],
            "Semantic Role Labeling": [485,504],
            "Lexicons for Sentiment, Affect, and Connotation": [505,524],
            "Coreference Resolution and Entity Linking": [525,554],
            "Discourse Coherence": [555,576],
            "Conversation and its Structure": [577,584]
        }
    },
    "./4 Foundations of statistical natural language pro_251119_100732.pdf":{
        "Preliminaries":{
            "introduction": [43,78],
            "Mathematical Foundations": [79,120],
            "Linguistic Essentials": [121,156],
            "Corpus-Based Work": [157,188]
        },
        "Words":{
            "Collocations": [191,230],
            "Statistical Inference: n-gram Models over Sparse Data": [231,268],
            "Word Sense Disambiguation": [269,304],
            "Lexical Acquisition": [305,354]
        },
        "Grammar":{
            "Markov Models": [357,380],
            "Part-of-Speech Tagging": [381,420],
            "Probabilistic Context Free Grammars": [421,446],
            "Probabilistic Parsing": [447,500]
        },
        "Applications and Techniques":{
            "Statistical Alignment and Machine Translation": [503,534],
            "Clustering": [535,568],
            "Topics in Information Retrieval": [569,614],
            "Text Categorization": [615,648]
        }
    },
    "./5. Natural Language Understanding (Gardner, Davidson e winograd).pdf":{
        "Natural Language Processing Overview": [12,16],
        "Mechanical Translatlon": [17,21],
        "Grammars": [22,35],
        "Parsing": [36,49],
        "Text Generation": [50,55],
        "Natural Language Processing Systems": [56,90]
    },
    "./6. Natural Language Processing (Indurkhya e Fred J. Damerau).pdf":{ 
        "Classical Approaches":{
            "Classical Approaches to Natural Language Processing": [29,34],
            "Text Preprocessing ": [35,56],
            "Lexical Analysis": [57,84],
            "Syntactic Parsing": [85,118],
            "Semantic Analysis": [119,146],
            "Natural Language Generation": [147,166]
        },
        "Empirical and Statistical Approaches":{
            "Corpus Creation": [173,192],
            "Treebank Annotation": [193,214],
            "Fundamental Statistical Techniques": [215,230],
            "Part-of-Speech Tagging": [231,262],
            "Statistical Parsing": [263,292],
            "Multiword Expressions": [293,318],
            "Normalized Web Distance and Word Similarity": [319,340],
            "Word Sense Disambiguation": [341,364],
            "An Overview of Modern Speech Recognition": [365,392],
            "Alignment": [393,434],
            "Statistical Machine Translation": [435,446]
        },
        "Applications":{
            "Chinese Machine Translation": [451,480],
            "Information Retrieval": [481,510],
            "Question Answering": [511,536],
            "Information Extraction": [537,558],
            "Report Generation": [559,582],
            "Emerging Applications of Natural Language Generation in Information Visualization, Education, and Health Care": [583,602],
            "Ontology Construction": [603,630],
            "BioNLP: Biomedical Text Mining": [631,652],
            "Sentiment Analysis and Subjectivity": [653,687]
        },
    },
    "./7. Computational Linguistics and Natural Language Processing (Clark e Fox).pdf":{
        "Formal Foundations":{
            "Formal Language Theory":[37,68],
            "Computational Complexity in Natural Language": [69,99],
            "Statistical Language Modeling": [100,130],
            "Theory of Parsing":[131,155]
        },
        "Current Methods":{
            "Maximum Entropy Models": [159,179],
            "Memory-Based Learning":[180,205],
            "Decision Trees":[206,222],
            "Unsupervised Learning and Grammar Induction": [223,246],
            "Artificial Neural Networks": [247,263],
            "Linguistic Annotation": [264,296],
            "Evaluation of NLP Systems": [297,318]
        },
        "Domains of Application":{
            "Speech Recognition": [325,358],
            "Statistical Parsing": [359,389],
            "Segmentation and Morphology": [390,419],
            "Computational Semantics": [420,454],
            "Computational Models of Dialogue": [455,507],
            "Computational Psycholinguistics ": [508,539]
        },
        "Applications":{
            "Information Extraction": [543,556],
            "Machine Translation": [557,599],
            "Natural Language Generation": [600,624],
            "Discourse Processing": [625,655],
            "Question Answering": [656,680]
        }
    },
    "./8. Natural Language Processing in Action Understanding, analyzing, and generating text with Python (Hannes, Cole e Hobson).pdf":{
        "Wordy Machines":{
            "Packets of thought": [35,61],
            "Build your vocabulary": [62,101],
            "Math with words": [102,128],
            "Finding meaning in word counts": [129,184]
        },
        "Deeper Learning":{
            "Baby steps with neural networks": [187,212],
            "Reasoning with word vectors": [213,249],
            "Getting words in order with convolutional neural networks": [250,278],
            "Loopy (recurrent) neural networks": [279,305],
            "Improving retention with long short-term memory networks": [306,342],
            "Sequence-to-sequence models and attention": [343,368]
        },
        "Getting Real":{
            "Information extraction": [371,396],
            "Getting chatty": [397,434],
            "Scaling up": [435,456]
        }
    },
    "./9. Natural Language processing with python (Klein e Loper).pdf":{
        "Language Processing and Python": [23,60],
        "Accessing Text Corpora and Lexical Resources": [61,100],
        "Processing Raw Text": [101,150],
        "Writing Structured Programs": [151,200],
        "Categorizing and Tagging Words": [201,242],
        "Learning to Classify Text": [243,282],
        "Extracting Information from Text": [283,312],
        "Analyzing Sentence Structure": [313,348],
        "Building Feature-Based Grammars": [349,382],
        "Analyzing the Meaning of Sentences": [383,428],
        "Managing Linguistic Data": [429,461]
    },
    "./10. Natural Language Processing (Jacob Eisenstein).pdf":{
        "Learning":{
            "Linear text classification": [31,62],
            "Nonlinear classification": [63,82],
            "Linguistic applications of classification": [83,108],
            "Learning without supervision": [109,135]
        },
        "Sequences and Trees":{
            "Language models": [139,156],
            "Sequence labeling": [157,186],
            "Applications of sequence labeling": [187,200],
            "Formal language theory": [201,234],
            "Context-free parsing": [235,262],
            "Dependency parsing": [263,285]
        },
        "Meaning":{
            "Logical semantics": [289,310],
            "Predicate-argument semantics": [311,334],
            "Distributional and distributed semantics": [335,360],
            "Reference Resolution": [361,386],
            "Discourse": [387,406]
        },
        "Applications":{
            "Information extraction": [409,436],
            "Machine translation": [437,460],
            "Text generation": [461,476]
        }
    },
    "./11. Deep Learning and Machine Learning - Natural Language (Chen et al. ).pdf":{
        "Natural language processing": [21,24],
        "Text Preprocessing": [25,57],
        "Data Cleaning for Training Large Language Models": [58,62],
        "Hugging Face for NLP":{
            "Hugging Face Dataset Library": [63,66],
            "Tokenization in Natural Language Processing": [67,75],
            "How to Fine-Tune a Pretrained Model?": [76,96],
            "Tokenizer Library": [97,149],
            "Don’t Stop Pre-training": [150,163],
            "Token Classification": [164,168],
            "Masked Language Model": [169,182],
            "Translation":[183,197],
            "Summarization": [198,206],
            "Further Reading and Resources": [207,210],
            "Casual Language Model": [211,221],
            "Question & Answering": [222,231],
            "Gradio - The Fastest Way to Demo Your Machine Learning Model": [232,245]
        }
    }
}

def extrair_paginas(pdf_reader, inicio, fim):
    """
    Extrai texto de um intervalo de páginas.
    O JSON usa contagem começando em 1 (humano),
    o Python/PyPDF usa contagem começando em 0.
    """
    texto_extraido = ""
    total_paginas = len(pdf_reader.pages)
    
    # Ajuste de índice: inicio-1 para pegar a página correta
    # O loop vai até 'fim' porque o range em python é exclusivo no último número
    for i in range(inicio - 1, fim):
        if 0 <= i < total_paginas:
            try:
                pagina = pdf_reader.pages[i]
                texto_extraido += pagina.extract_text() + "\n\n"
            except Exception as e:
                print(f"  [Erro] Falha ao ler página {i+1}: {e}")
        else:
            print(f"  [Aviso] Página {i+1} fora do limite do arquivo.")
            
    return texto_extraido

def gerar_json_recursivo(estrutura, pdf_reader):
    """
    Função recursiva que navega na estrutura (Livros -> Seções -> Capítulos),
    extrai o texto e retorna um dicionário com a mesma estrutura,
    mas substituindo [pág_inicio, pág_fim] pelo texto extraído.
    """
    resultado = {}
    
    for titulo, valor in estrutura.items():
        if isinstance(valor, list):
            # Caso base: É um capítulo com intervalo de páginas [inicio, fim]
            inicio, fim = valor
            print(f"  -> Extraindo '{titulo}' (Páginas {inicio}-{fim})...")
            texto = extrair_paginas(pdf_reader, inicio, fim)
            resultado[titulo] = texto
                
        elif isinstance(valor, dict):
            # Caso recursivo: É uma seção (ex: "Large Language Models")
            print(f" Entrando na seção: {titulo}")
            # Chama a função novamente para processar o conteúdo da seção
            resultado[titulo] = gerar_json_recursivo(valor, pdf_reader)
            
    return resultado

def main():
    arquivo_saida = "biblioteca_extraida.json"
    biblioteca_final = {}

    print("Iniciando extração para JSON único...")

    for caminho_pdf, conteudo in biblioteca_json.items():
        # Limpa o caminho do arquivo (remove ./ se necessário para consistência)
        caminho_limpo = caminho_pdf.replace("./", "")
        
        if not os.path.exists(caminho_limpo):
            print(f"\n[ERRO] Arquivo não encontrado: {caminho_limpo}")
            continue

        print(f"\nProcessando livro: {caminho_limpo}")

        try:
            reader = PdfReader(caminho_limpo)
            # Processa o livro e guarda o resultado no dicionário principal
            conteudo_extraido = gerar_json_recursivo(conteudo, reader)
            biblioteca_final[caminho_pdf] = conteudo_extraido
            
        except Exception as e:
            print(f"Erro crítico ao abrir o PDF {caminho_limpo}: {e}")

    # Salva tudo no arquivo JSON final
    print(f"\nSalvando dados em {arquivo_saida}...")
    with open(arquivo_saida, "w", encoding="utf-8") as f:
        json.dump(biblioteca_final, f, ensure_ascii=False, indent=4)

    print("\n--- Processo Finalizado com Sucesso! ---")

if __name__ == "__main__":
    main()