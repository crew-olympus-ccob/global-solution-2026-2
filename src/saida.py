from __future__ import annotations

import re
import textwrap
from datetime import date

from base import AVISO_LIMITACAO
from navegacao import buscar_relacionados

LARGURA = 72
LINHA = "=" * LARGURA
SUBLINHA = "-" * LARGURA

INICIO_DE_ALERTA = ("desconfie", "cuidado", "atenção", "atencao", "nunca", "evite", "não ", "nao ")


def _quebrar(texto: str, recuo: str = "") -> str:
    return textwrap.fill(texto, width=LARGURA, initial_indent=recuo, subsequent_indent=recuo)


def _numerado(n: int, texto: str) -> str:
    prefixo = f"  {n}. "
    return textwrap.fill(texto, width=LARGURA, initial_indent=prefixo, subsequent_indent=" " * len(prefixo))


def _data_br(iso: str) -> str:
    try:
        return date.fromisoformat(iso).strftime("%d/%m/%Y")
    except ValueError:
        return iso


def _idade_em_dias(iso: str, hoje: date | None = None) -> int | None:
    try:
        return ((hoje or date.today()) - date.fromisoformat(iso)).days
    except ValueError:
        return None


def dividir_frases(texto: str) -> list[str]:
    partes = re.split(r"(?<=[.!?])\s+(?=[A-ZÀ-Ú])", texto.strip())
    return [p.strip() for p in partes if p.strip()]


def _eh_alerta(frase: str) -> bool:
    return frase.lower().startswith(INICIO_DE_ALERTA)


def modelo_1_direto(registro: dict, base: list[dict] | None = None, aviso: str = AVISO_LIMITACAO) -> str:
    partes = [
        registro["pergunta_chave"],
        registro["conteudo"],
        f"Fonte: {registro['referencia']} (verificado em {_data_br(registro['data_verificacao'])})",
    ]
    if aviso:
        partes.append(f"Aviso: {aviso}")
    return "\n".join(partes)


def modelo_2_educativo(registro: dict, base: list[dict] | None = None,
                       aviso: str = AVISO_LIMITACAO, hoje: date | None = None) -> str:
    frases = dividir_frases(registro["conteudo"])
    alertas = [f for f in frases if _eh_alerta(f)]
    normais = [f for f in frases if not _eh_alerta(f)]
    if registro.get("alerta"):
        alertas.insert(0, registro["alerta"])

    resumo = normais[0] if normais else ""
    resto = normais[1:]

    blocos = [
        LINHA,
        _quebrar(registro["pergunta_chave"].upper()),
        f"Tema: {registro['tema']}  |  Código: {registro['id']}",
        LINHA,
    ]
    if resumo:
        blocos += ["", "EM RESUMO", _quebrar(resumo, "  ")]

    passos = registro.get("passos") or []
    if passos:
        blocos += ["", "PASSO A PASSO"] + [_numerado(n, p) for n, p in enumerate(passos, 1)]
        if resto:
            blocos += ["", "ENTENDA MELHOR", _quebrar(" ".join(resto), "  ")]
    elif resto:
        blocos += ["", "COMO FAZER"] + [_numerado(n, p) for n, p in enumerate(resto, 1)]

    if alertas:
        blocos += ["", "ATENÇÃO"] + [textwrap.fill(a, width=LARGURA, initial_indent="  ! ", subsequent_indent="    ")
                                  for a in alertas]

    ref = registro["referencia"]
    blocos += ["", "FONTE", f"  {ref}" if ref.startswith("http") else _quebrar(ref, "  ")]
    linha_data = f"  Informação verificada em {_data_br(registro['data_verificacao'])}"
    idade = _idade_em_dias(registro["data_verificacao"], hoje)
    if idade is not None and idade > 365:
        linha_data += " (há mais de 1 ano, confira se continua válida)."
    blocos.append(linha_data)

    if base:
        relacionados = buscar_relacionados(base, registro)
        if relacionados:
            blocos += ["", "VEJA TAMBÉM"]
            blocos += [_quebrar(f"[{r['id']}] {r['pergunta_chave']}", "  ") for r in relacionados]

    if aviso:
        blocos += ["", SUBLINHA, _quebrar(f"Aviso: {aviso}")]
    blocos.append(LINHA)
    return "\n".join(blocos)


MODELOS = {
    "1": ("Direto (resumido)", modelo_1_direto),
    "2": ("Educativo e detalhado", modelo_2_educativo),
}
