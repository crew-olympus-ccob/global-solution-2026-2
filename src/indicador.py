from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

from base import RAIZ, ErroBase, carregar_base
from busca import empate_no_topo, escolher_por_numero, listar_temas, registros_do_tema

PERGUNTAS_PADRAO = RAIZ / "tests" / "perguntas_teste.json"


def resolver_menu(entrada: str, base: list[dict]) -> list[dict]:
    if ">" not in entrada:
        return []
    tema_txt, item_txt = entrada.split(">", 1)
    tema = escolher_por_numero(tema_txt, listar_temas(base))
    if tema is None:
        return []
    item = escolher_por_numero(item_txt, registros_do_tema(tema, base))
    return [item] if item else []


def executar_caso(caso: dict, base: list[dict]) -> dict:
    forma = caso.get("forma", "palavra_chave")
    entrada = str(caso.get("pergunta", ""))
    esperado = caso.get("id_esperado")
    ids_base = {r["id"] for r in base}

    obtidos = resolver_menu(entrada, base) if forma == "menu" else empate_no_topo(entrada, base)
    ids = [r["id"] for r in obtidos]

    if esperado is not None and int(esperado) not in ids_base:
        if not ids:
            return {"forma": forma, "entrada": entrada, "esperado": esperado, "obtido": [],
                    "acerto": False, "pendente": True, "motivo": "registro ainda não existe na base"}
        return {"forma": forma, "entrada": entrada, "esperado": esperado, "obtido": ids,
                "acerto": False, "pendente": False,
                "motivo": f"falso positivo: o registro {esperado} não existe e respondeu {ids}"}

    if esperado is None:
        acerto, motivo = (not ids), ("" if not ids else f"deveria não achar nada, achou {ids}")
    elif len(ids) == 1:
        acerto = ids[0] == int(esperado)
        motivo = "" if acerto else f"retornou {ids[0]}"
    elif len(ids) > 1:
        acerto, motivo = False, f"ambíguo: {', '.join(map(str, ids))}"
    else:
        acerto, motivo = False, "nada encontrado"

    return {"forma": forma, "entrada": entrada, "esperado": esperado, "obtido": ids,
            "acerto": acerto, "pendente": False, "motivo": motivo}


def taxa_de_acerto(resultados: list[dict]) -> float:
    avaliados = [r for r in resultados if not r.get("pendente")]
    if not avaliados:
        return 0.0
    return round(100 * sum(r["acerto"] for r in avaliados) / len(avaliados), 1)


def calcular(base: list[dict], casos: list[dict]) -> dict:
    resultados = [executar_caso(c, base) for c in casos]
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
    caminho = Path(caminho) if caminho else PERGUNTAS_PADRAO
    with caminho.open(encoding="utf-8") as f:
        dados = json.load(f)
    casos = dados["casos"] if isinstance(dados, dict) else dados
    if not isinstance(casos, list) or not casos:
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
        faltam = sorted({r["esperado"] for r in res["resultados"] if r["pendente"]})
        linhas += ["", f"Pendentes (fora da conta): {res['pendentes']} pergunta(s) esperam registros "
                       f"que ainda não existem (ids {', '.join(map(str, faltam))})."]
    return "\n".join(linhas) + "\n"


def main(argv: list[str] | None = None) -> int:
    try:
        sys.stdout.reconfigure(errors="replace")
    except AttributeError:
        pass
    p = argparse.ArgumentParser(description="Calcula a taxa de acerto das buscas")
    p.add_argument("--base", help="JSON da base (padrão: data/base_conhecimento.json)")
    p.add_argument("--casos", help="JSON das perguntas (padrão: tests/perguntas_teste.json)")
    p.add_argument("--meta", type=float, help="taxa mínima aceitável em %%")
    p.add_argument("--salvar", help="grava o relatório em Markdown neste caminho")
    args = p.parse_args(argv)

    try:
        base = carregar_base(args.base)
        casos = carregar_casos(args.casos)
    except (ErroBase, OSError, ValueError, KeyError) as e:
        print(f"Erro: {e}", file=sys.stderr)
        return 2

    res = calcular(base, casos)
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
