from __future__ import annotations

import re
import textwrap

from navegacao import buscar_relacionados

LARGURA = 72
LINHA = "=" * LARGURA

INICIO_DE_ALERTA = ("desconfie", "cuidado", "atenção", "atencao", "nunca", "evite", "não ", "nao ")


def _quebrar(texto: str, recuo: str = "") -> str:
    return textwrap.fill(texto, width=LARGURA, initial_indent=recuo, subsequent_indent=recuo)


def _numerado(n: int, texto: str) -> str:
    prefixo = f"  {n}. "
    return textwrap.fill(texto, width=LARGURA, initial_indent=prefixo, subsequent_indent=" " * len(prefixo))


def dividir_frases(texto: str) -> list[str]:
    partes = re.split(r"(?<=[.!?])\s+(?=[A-ZÀ-Ú])", texto.strip())
    return [p.strip() for p in partes if p.strip()]


def _eh_alerta(frase: str) -> bool:
    return frase.lower().startswith(INICIO_DE_ALERTA)


def modelo_2_educativo(registro: dict, base: list[dict] | None = None, fonte_e_aviso: str = "") -> str:
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

    if base:
        relacionados = buscar_relacionados(base, registro)
        if relacionados:
            blocos += ["", "VEJA TAMBÉM"]
            blocos += [_quebrar(f"[{r['id']}] {r['pergunta_chave']}", "  ") for r in relacionados]

    if fonte_e_aviso:
        blocos += ["", fonte_e_aviso]
    blocos.append(LINHA)
    return "\n".join(blocos)
