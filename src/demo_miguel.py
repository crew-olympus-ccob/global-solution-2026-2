"""Demo da parte do Miguel: busca por tema + Modelo 1 + erros.

Roda sozinho antes da integração:  python src/demo_miguel.py
Usa data/base_conhecimento.json se existir; senão, data/servicos.json.
"""

import json
from pathlib import Path

from busca_tema import buscar_por_tema, listar_temas
from erros import AmbiguidadeError, ErroDeConsulta, escolher_opcao
from respostas import formatar_modelo_1

DATA = Path(__file__).resolve().parent.parent / "data"


def carregar():
    for nome in ("base_conhecimento.json", "servicos.json"):
        caminho = DATA / nome
        if caminho.exists():
            with open(caminho, encoding="utf-8") as f:
                return json.load(f)
    raise SystemExit("Nenhum JSON encontrado em data/.")


def main():
    base = carregar()
    while True:
        print("\n=== Busca por tema ===")
        for i, tema in enumerate(listar_temas(base), 1):
            print(f"  {i}) {tema}")
        escolha = input("Tema (número, nome ou palavra; 'sair' para encerrar): ")
        if escolha.strip().lower() == "sair":
            print("Até logo!")
            return
        try:
            tema, registros = buscar_por_tema(base, escolha)
        except AmbiguidadeError as erro:
            print(erro.mensagem)
            indice = escolher_opcao(erro.opcoes)
            if indice is None:
                continue
            tema, registros = buscar_por_tema(base, erro.opcoes[indice])
        except ErroDeConsulta as erro:
            print(erro.mensagem)
            continue

        print(f"\nTema: {tema}")
        for i, r in enumerate(registros, 1):
            print(f"  {i}) {r['pergunta_chave']}")
        pick = input("Qual pergunta? (número; Enter volta): ").strip()
        if pick.isdigit() and 1 <= int(pick) <= len(registros):
            print("\n" + formatar_modelo_1(registros[int(pick) - 1]))
        elif pick:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
