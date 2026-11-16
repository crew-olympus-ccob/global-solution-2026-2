from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

import carregador
from busca import buscar_por_pergunta

RAIZ = Path(__file__).resolve().parent.parent
ARQUIVOS_DE_PERGUNTAS = [RAIZ / "tests" / "perguntas_teste.json", RAIZ / "tests" / "perguntas_extras.json"]
AGUARDANDO_BUSCA_TEMA = "aguardando a busca por tema (src/busca_tema.py)"


def buscar_por_tema_disponivel():
    try:
        from busca_tema import buscar_por_tema
    except ImportError:
        return None
    return buscar_por_tema


def resolver_menu(entrada: str, base: list[dict], buscar_por_tema) -> list[dict]:
    if ">" not in entrada:
        return []
    tema_txt, item_txt = entrada.split(">", 1)
    try:
        _, registros = buscar_por_tema(base, tema_txt)
    except Exception:
        return []
    item_txt = item_txt.strip()
    if not item_txt.isdecimal() or not 1 <= int(item_txt) <= len(registros):
        return []
    return [registros[int(item_txt) - 1]]


def _pendente(forma, entrada, esperado, motivo):
    return {"forma": forma, "entrada": entrada, "esperado": esperado, "obtido": [],
            "acerto": False, "pendente": True, "motivo": motivo}


def executar_caso(caso: dict, base: list[dict], buscar_por_tema=None) -> dict:
    forma = caso.get("forma", "palavra_chave")
    entrada = str(caso.get("pergunta", ""))
    esperado = caso.get("id_esperado")
    ids_base = {r["id"] for r in base}

    if forma == "menu":
        if buscar_por_tema is None:
            return _pendente(forma, entrada, esperado, AGUARDANDO_BUSCA_TEMA)
        obtidos = resolver_menu(entrada, base, buscar_por_tema)
    else:
        obtidos = buscar_por_pergunta(entrada, base)[:1]
    ids = [r["id"] for r in obtidos]

    if esperado is not None and int(esperado) not in ids_base:
        if not ids:
            return _pendente(forma, entrada, esperado, "registro ainda não existe na base")
        return {"forma": forma, "entrada": entrada, "esperado": esperado, "obtido": ids,
                "acerto": False, "pendente": False,
                "motivo": f"falso positivo: o registro {esperado} não existe e respondeu {ids}"}

    if esperado is None:
        acerto, motivo = (not ids), ("" if not ids else f"deveria não achar nada, achou {ids}")
    elif ids:
        acerto = ids[0] == int(esperado)
        motivo = "" if acerto else f"retornou {ids[0]}"
    else:
        acerto, motivo = False, "nada encontrado"

    return {"forma": forma, "entrada": entrada, "esperado": esperado, "obtido": ids,
            "acerto": acerto, "pendente": False, "motivo": motivo}


def taxa_de_acerto(resultados: list[dict]) -> float:
    avaliados = [r for r in resultados if not r.get("pendente")]
    if not avaliados:
        return 0.0
    return round(100 * sum(r["acerto"] for r in avaliados) / len(avaliados), 1)


def calcular(base: list[dict], casos: list[dict], buscar_por_tema=None) -> dict:
    resultados = [executar_caso(c, base, buscar_por_tema) for c in casos]
    avaliados = [r for r in resultados if not r["pendente"]]
    por_forma = {f: taxa_de_acerto([r for r in avaliados if r["forma"] == f])
                 for f in sorted({r["forma"] for r in avaliados})}
    return {
        "total": len(resultados),
        "avaliados": len(avaliados),
        "pendentes": len(resultados) - len(avaliados),
        "acertos": sum(r["acerto"] for r in avaliados),
        "taxa": taxa_de_acerto(resultados),
        "por_forma": por_forma,
        "resultados": resultados,
    }


def carregar_casos(caminho: str | Path | None = None) -> list[dict]:
    arquivos = [Path(caminho)] if caminho else [a for a in ARQUIVOS_DE_PERGUNTAS if a.is_file()]
    casos = []
    for arquivo in arquivos:
        with arquivo.open(encoding="utf-8") as f:
            dados = json.load(f)
        casos += dados["casos"] if isinstance(dados, dict) else dados
    if not casos:
        raise ValueError("Nenhuma pergunta de teste encontrada.")
    return casos


def relatorio(res: dict, markdown: bool = False) -> str:
    nomes = {"palavra_chave": "Palavra-chave", "menu": "Menu (tema > assunto)"}
    linhas = []
    if markdown:
        linhas += ["# Resultado do indicador: taxa de acerto", "",
                   f"Gerado em {datetime.now():%d/%m/%Y %H:%M} com `python src/indicador.py`.", ""]
    linhas.append(f"Taxa de acerto geral: {res['taxa']}% ({res['acertos']}/{res['avaliados']} casos avaliados)")
    for forma, taxa in res["por_forma"].items():
        n = sum(1 for r in res["resultados"] if r["forma"] == forma and not r["pendente"])
        linhas.append(f"  - {nomes.get(forma, forma)}: {taxa}% ({n} casos)")
    erros = [r for r in res["resultados"] if not r["acerto"] and not r["pendente"]]
    if erros:
        linhas += ["", "Casos que falharam:"]
        linhas += [f"  - [{r['forma']}] \"{r['entrada']}\" -> esperado {r['esperado']}, {r['motivo']}" for r in erros]
    if res["pendentes"]:
        linhas += ["", "Pendentes (fora da conta):"]
        motivos = {}
        for r in res["resultados"]:
            if r["pendente"]:
                motivos.setdefault(r["motivo"], []).append(r)
        for motivo, itens in motivos.items():
            if motivo == "registro ainda não existe na base":
                ids = sorted({r["esperado"] for r in itens})
                linhas.append(f"  - {len(itens)} pergunta(s) esperam registros que ainda não existem (ids {', '.join(map(str, ids))})")
            else:
                linhas.append(f"  - {len(itens)} pergunta(s) {motivo}")
    return "\n".join(linhas) + "\n"


def main(argv: list[str] | None = None) -> int:
    try:
        sys.stdout.reconfigure(errors="replace")
    except AttributeError:
        pass
    p = argparse.ArgumentParser(description="Calcula a taxa de acerto das buscas")
    p.add_argument("--base", help="JSON da base (padrão: data/base_conhecimento.json)")
    p.add_argument("--casos", help="JSON das perguntas (padrão: tests/perguntas_teste.json e perguntas_extras.json)")
    p.add_argument("--meta", type=float, help="taxa mínima aceitável em %%")
    p.add_argument("--salvar", help="grava o relatório em Markdown neste caminho")
    args = p.parse_args(argv)

    base = carregador.carregar_base(args.base) if args.base else carregador.carregar_base()
    if not base:
        print("Erro: a base não pôde ser carregada.", file=sys.stderr)
        return 2
    try:
        casos = carregar_casos(args.casos)
    except (OSError, ValueError, KeyError) as e:
        print(f"Erro: {e}", file=sys.stderr)
        return 2

    res = calcular(base, casos, buscar_por_tema_disponivel())
    print(relatorio(res))
    if args.salvar:
        Path(args.salvar).write_text(relatorio(res, markdown=True), encoding="utf-8")
        print(f"Relatório salvo em {args.salvar}")
    if args.meta is not None and res["taxa"] < args.meta:
        print(f"Abaixo da meta de {args.meta}%.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
