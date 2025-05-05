# queue-simulator

Este projeto implementa um simulador de filas (G/G/C/K) em Python, suportando diferentes topologias de filas.

## Requisitos

Python 3.8+

Dependências listadas em `requirements.txt`

## Para rodar:

1. Clone o projeto
2. Crie e ative um ambiente virtual (recomendável)

```bash
python -m venv .venv
source .venv/bin/activate # macOS / Linux
.venv\Scripts\activate # Windows
```

3. Instale as dependências

```bash
pip install -r requirements.txt
```

4. Prepare o arquivo de configuração em `config/model.yaml`
5. Execute a simulação

```bash
# Na raiz do projeto, execute:
python -m src.main config/model.yaml
```
