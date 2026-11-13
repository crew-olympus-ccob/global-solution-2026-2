from __future__ import annotations

import argparse
import sys

from base import AVISO_LIMITACAO, ErroBase, carregar_base
from busca import (
    buscar_por_id,
    buscar_por_palavra_chave,
    empate_no_topo,
    escolher_por_numero,
    listar_temas,
    registros_do_tema,
)
from navegacao import escolher_relacionado
from saida import MODELOS

TAMANHO_MAX_ENTRADA = 200


class Sair(Exception):
    pass


def ler(mensagem: str) -> str:
    try:
        texto = input(mensagem)
    except (EOFError, KeyboardInterrupt):
        print()
        raise Sair from None
    texto = texto.replace("\x00", "").strip()
    if len(texto) > TAMANHO_MAX_ENTRADA:
        print(f"(Entrada muito longa: considerei só os primeiros {TAMANHO_MAX_ENTRADA} caracteres.)")
        texto = texto[:TAMANHO_MAX_ENTRADA]
    return texto


def mostrar(registro: dict, base: list[dict], modelo: str) -> None:
    _, funcao = MODELOS[modelo]
    print()
    print(funcao(registro, base, AVISO_LIMITACAO))
    print()


def responder(registro: dict, base: list[dict], modelo: str) -> None:
    while registro is not None:
        mostrar(registro, base, modelo)
        op = ler("Ver outros assuntos do mesmo tema? (s/N): ").lower()
        if op not in ("s", "sim"):
            return
        try:
            registro = escolher_relacionado(base, registro)
        except KeyboardInterrupt:
            print()
            raise Sair from None


def fluxo_palavra_chave(base: list[dict], modelo: str) -> None:
    while True:
        consulta = ler("\nDescreva sua dúvida (ou 0 para voltar): ")
        if consulta == "0":
            return
        if not consulta:
            print("Você não digitou nada. Exemplo: 'perdi meu CPF' ou 'título de eleitor'.")
            continue

        empatados = empate_no_topo(consulta, base)
        if not empatados:
            print("Não encontrei nada sobre isso na base.")
            print("Tente outras palavras ou use a opção 2 (navegar por tema).")
            continue

        if len(empatados) == 1:
            escolhido = empatados[0]
        else:
            print("Encontrei mais de um assunto possível:")
            for n, r in enumerate(empatados, 1):
                print(f"  {n}. {r['pergunta_chave']}")
            escolhido = None
            while escolhido is None:
                op = ler("Qual deles? (número, ou 0 para voltar): ")
                if op == "0":
                    break
                escolhido = escolher_por_numero(op, empatados)
                if escolhido is None:
                    print(f"Opção inválida. Digite um número de 1 a {len(empatados)}.")
            if escolhido is None:
                continue

        outros = [r for r in buscar_por_palavra_chave(consulta, base) if r is not escolhido]
        responder(escolhido, base, modelo)
        if outros:
            print("Também pode interessar: " + "; ".join(f"[{r['id']}] {r['pergunta_chave']}" for r in outros))


def fluxo_menu(base: list[dict], modelo: str) -> None:
    temas = listar_temas(base)
    while True:
        print("\nTEMAS")
        for n, t in enumerate(temas, 1):
            print(f"  {n}. {t}")
        op = ler("Escolha o tema (número) ou 0 para voltar: ")
        if op == "0":
            return
        if not op:
            print("Você não digitou nada.")
            continue
        tema = escolher_por_numero(op, temas)
        if tema is None:
            print(f"Opção inválida. Digite um número de 1 a {len(temas)}.")
            continue

        itens = registros_do_tema(tema, base)
        while True:
            print(f"\n{tema.upper()}")
            for n, r in enumerate(itens, 1):
                print(f"  {n}. {r['pergunta_chave']}")
            op2 = ler("Escolha o assunto (número) ou 0 para voltar: ")
            if op2 == "0":
                break
            reg = escolher_por_numero(op2, itens)
            if reg is None:
                print(f"Opção inválida. Digite um número de 1 a {len(itens)}.")
                continue
            responder(reg, base, modelo)


def escolher_modelo(atual: str) -> str:
    print("\nFORMATO DA RESPOSTA")
    for chave, (nome, _) in MODELOS.items():
        marca = " (atual)" if chave == atual else ""
        print(f"  {chave}. {nome}{marca}")
    op = ler("Escolha: ")
    if op in MODELOS:
        print(f"Formato alterado para: {MODELOS[op][0]}.")
        return op
    print("Opção inválida. Formato mantido.")
    return atual


def loop_interativo(base: list[dict], modelo: str) -> None:
    print("\nAssistente CitizenTech: orientações sobre serviços públicos")
    print(f"({len(base)} assuntos na base. A qualquer momento: Ctrl+C para sair.)")
    while True:
        print("\nMENU PRINCIPAL")
        print("  1. Buscar por palavra-chave")
        print("  2. Navegar por tema")
        print(f"  3. Formato da resposta (atual: {MODELOS[modelo][0]})")
        print("  0. Sair")
        op = ler("Opção: ")
        if op == "1":
            fluxo_palavra_chave(base, modelo)
        elif op == "2":
            fluxo_menu(base, modelo)
        elif op == "3":
            modelo = escolher_modelo(modelo)
        elif op == "0":
            raise Sair
        elif not op:
            print("Você não digitou nada. Escolha 1, 2, 3 ou 0.")
        else:
            print("Opção inválida. Escolha 1, 2, 3 ou 0.")


def main(argv: list[str] | None = None) -> int:
    try:
        sys.stdout.reconfigure(errors="replace")
    except AttributeError:
        pass

    p = argparse.ArgumentParser(description="Assistente CitizenTech")
    p.add_argument("--base", help="caminho do JSON (padrão: data/base_conhecimento.json)")
    p.add_argument("--modelo", choices=list(MODELOS), default="2", help="1 = direto, 2 = educativo (padrão)")
    p.add_argument("--buscar", metavar="TEXTO", help="busca por palavra-chave e sai")
    p.add_argument("--id", metavar="NUMERO", help="mostra um registro pelo id e sai")
    args = p.parse_args(argv)

    try:
        base = carregar_base(args.base)
    except ErroBase as e:
        print(f"Erro ao carregar a base: {e}", file=sys.stderr)
        return 2

    if args.id is not None:
        reg = buscar_por_id(args.id, base)
        if not reg:
            print(f"Id não encontrado: {args.id!r}")
            return 1
        mostrar(reg, base, args.modelo)
        return 0

    if args.buscar is not None:
        achados = empate_no_topo(args.buscar[:TAMANHO_MAX_ENTRADA], base)
        if not achados:
            print("Não encontrei nada sobre isso na base.")
            return 1
        if len(achados) > 1:
            print("Mais de um assunto possível: " + ", ".join(str(r["id"]) for r in achados))
        mostrar(achados[0], base, args.modelo)
        return 0

    try:
        loop_interativo(base, args.modelo)
    except Sair:
        print("Até logo!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
