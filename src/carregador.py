"""Leitura segura da base de conhecimento em JSON."""

import json
import os

CAMINHO_PADRAO = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "data", "base_conhecimento.json"
)


def carregar_base(caminho=CAMINHO_PADRAO):
    """Lê o JSON e devolve a lista de registros.

    Se o arquivo não existir ou estiver corrompido, avisa no terminal
    e devolve uma lista vazia, sem derrubar o programa.
    """
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            base = json.load(arquivo)
    except FileNotFoundError:
        print(f"Erro: arquivo da base de conhecimento não encontrado ({caminho}).")
        return []
    except json.JSONDecodeError as erro:
        print(f"Erro: o arquivo da base está corrompido (linha {erro.lineno}).")
        return []
    except OSError as erro:
        print(f"Erro ao abrir a base de conhecimento: {erro}")
        return []

    if not isinstance(base, list):
        print("Erro: a base de conhecimento deve ser uma lista de registros.")
        return []

    return base
