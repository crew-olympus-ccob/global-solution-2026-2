"""Navegação entre assuntos relacionados."""


def buscar_relacionados(base, registro):
    """Devolve os outros registros do mesmo tema do registro informado."""
    return [r for r in base if r["tema"] == registro["tema"] and r["id"] != registro["id"]]


def escolher_relacionado(base, registro):
    """Mostra os assuntos relacionados e devolve o registro escolhido.

    Devolve None se não houver relacionados ou se a pessoa voltar ao menu.
    Entradas inválidas (vazio, letras, número fora da lista) pedem nova escolha.
    """
    relacionados = buscar_relacionados(base, registro)
    if not relacionados:
        print("Não há outros assuntos relacionados.")
        return None

    print(f"\nOutros assuntos de {registro['tema']}:")
    for numero, r in enumerate(relacionados, start=1):
        print(f"  {numero}. {r['pergunta_chave']}")
    print("  0. Voltar ao menu")

    while True:
        escolha = input("Escolha uma opção: ").strip()
        if escolha == "0":
            return None
        if escolha.isdigit() and 1 <= int(escolha) <= len(relacionados):
            return relacionados[int(escolha) - 1]
        print("Opção inválida. Digite um dos números da lista.")
