```bash
pip install poetry
```

criar venv com poetry no projeto, se estiver utilizando pycharm é mais simples, basta criar um interpreter python com poetry

após criar um interpreter, instalar dependencias.
```bash
 poetry install
```

Dependencias instaladas.


por enquanto é possível utilizar o groq gratuitamente.
crie uma conta no groq em: https://groq.com/
crie uma api key
coloque a api_key em .secrets.local.toml, caso esse arquivo não exista, copie .secrets.toml e renomeie a cópia para .secrets.local.toml, ele não deve subir no git
tente utilizar o provider.
para utilizar o gpt ou modelos no huggingface, mude a configuração em settings.toml, e coloque a api key respectiva no .secrets.local.toml
