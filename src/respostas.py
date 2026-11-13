"""Modelo 1 de resposta: Direto e Técnico (Dia 3 - Miguel).

Formato: sem introdução, passos numerados, observações em tópicos, fonte e data.
O conteúdo dos registros usa linhas "1) ..." para passos e "- ..." para
observações; se um registro vier em texto corrido, ele é exibido quebrado em
linhas sem perder nada.
"""

from __future__ import annotations

import re
import textwrap
from datetime import datetime

LARGURA = 88

AVISO_PADRAO = (
    "AVISO: este assistente é informativo e NÃO é um canal oficial nem substitui "
    "orientação jurídica, médica ou do órgão responsável. Confirme nos canais oficiais."
)


def _data_br(valor) -> str:
    try:
        return datetime.strptime(str(valor), "%Y-%m-%d").strftime("%d/%m/%Y")
    except ValueError:
        return str(valor) if valor else "não informada"


def _quebrar(texto: str, prefixo: str, largura: int, recuo: str | None = None) -> str:
    """Quebra em linhas sem cortar palavras nem URLs (URL longa passa da largura)."""
    recuo = " " * len(prefixo) if recuo is None else recuo
    return textwrap.fill(
        texto, width=largura, initial_indent=prefixo, subsequent_indent=recuo,
        break_long_words=False, break_on_hyphens=False,
    )


def rodape_padrao(registro: dict, largura: int = LARGURA) -> str:
    """Fonte + aviso. Se o time já tiver a função oficial (Dia 3, Lucas), passe-a
    em `formatar_modelo_1(..., rodape=funcao)` e esta aqui deixa de ser usada."""
    fontes = [f.strip() for f in str(registro.get("referencia", "")).split("|") if f.strip()]
    linhas = ["FONTE:"] + [_quebrar(f, "  - ", largura) for f in (fontes or ["não informada"])]
    linhas.append(f"VERIFICADO EM: {_data_br(registro.get('data_verificacao'))}")
    linhas.append(_quebrar(AVISO_PADRAO, "", largura))
    return "\n".join(linhas)


def formatar_modelo_1(registro: dict, rodape=rodape_padrao, largura: int = LARGURA) -> str:
    """Monta o texto do Modelo 1 (Direto e Técnico) para um registro."""
    cabecalho = f"[{registro.get('id', '?')}] {str(registro.get('tema', '')).upper()}"
    linhas = [cabecalho, _quebrar(str(registro.get("pergunta_chave", "")), "PERGUNTA: ", largura), ""]

    passos, observacoes, corrido = [], [], []
    for linha in str(registro.get("conteudo", "")).splitlines():
        linha = linha.strip()
        if not linha:
            continue
        if re.match(r"^\d{1,2}\)\s", linha):
            passos.append(linha)
        elif linha.startswith("- "):
            observacoes.append(linha[2:].strip())
        else:
            corrido.append(linha)

    if passos:
        linhas.append("PROCEDIMENTO:")
        linhas += [_quebrar(p, "  ", largura, recuo="     ") for p in passos]
    if corrido:
        linhas.append("RESPOSTA:")
        linhas += [_quebrar(c, "  ", largura) for c in corrido]
    if observacoes:
        linhas.append("ATENÇÃO:")
        linhas += [_quebrar(o, "  - ", largura) for o in observacoes]
    if not (passos or corrido or observacoes):
        linhas.append("RESPOSTA: (registro sem conteúdo)")

    linhas.append("")
    linhas.append(rodape(registro))
    return "\n".join(linhas)


def exibir_modelo_1(registro: dict, rodape=rodape_padrao) -> None:
    print(formatar_modelo_1(registro, rodape=rodape))
