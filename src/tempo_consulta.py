"""Medição independente do tempo de execução de uma consulta."""

import json
from pathlib import Path
from time import perf_counter

from busca import buscar_por_pergunta
from carregador import carregar_base


def medir_consulta(funcao, *args, **kwargs):
    """Retorna (resultado, segundos), excluindo entrada e exibição no terminal."""
    inicio = perf_counter()
    resultado = funcao(*args, **kwargs)
    return resultado, perf_counter() - inicio


def main():
    """Executa as perguntas disponíveis e mostra o tempo e o primeiro resultado."""
    base = carregar_base()
    if not base:
        print("Não foi possível carregar a base de conhecimento.")
        return 1
    caminho = Path(__file__).resolve().parent.parent / "tests" / "perguntas_teste.json"
    try:
        with caminho.open(encoding="utf-8") as arquivo:
            perguntas = json.load(arquivo)
    except (OSError, json.JSONDecodeError) as erro:
        print(f"Não foi possível carregar as perguntas de teste: {erro}")
        return 1
    for caso in perguntas:
        resultados, segundos = medir_consulta(buscar_por_pergunta, caso["pergunta"], base)
        obtido = resultados[0]["id"] if resultados else None
        print(f"Pergunta: {caso['pergunta']}")
        print(f"  Esperado: {caso['id_esperado']} | Obtido: {obtido} | Tempo: {segundos * 1000:.3f} ms")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
