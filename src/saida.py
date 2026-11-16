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


PASSO_NUMERADO = re.compile(r"^\d{1,2}\)\s*")


def separar_conteudo(texto: str) -> tuple[list[str], list[str], list[str]]:
    linhas = [l.strip() for l in texto.splitlines() if l.strip()]
    if not any(PASSO_NUMERADO.match(l) or l.startswith("- ") for l in linhas):
        return dividir_frases(texto), [], []
    corrido, passos, itens = [], [], []
    for linha in linhas:
        if PASSO_NUMERADO.match(linha):
            passos.append(PASSO_NUMERADO.sub("", linha))
        elif linha.startswith("- "):
            itens.append(linha[2:].strip())
        else:
            corrido += dividir_frases(linha)
    return corrido, passos, itens


def modelo_2_educativo(registro: dict, base: list[dict] | None = None, fonte_e_aviso: str = "",
                       rodape=None) -> str:
    if rodape is not None:
        fonte_e_aviso = rodape(registro)
    frases, passos_do_texto, itens = separar_conteudo(registro["conteudo"])
    alertas = [f for f in frases + itens if _eh_alerta(f)]
    normais = [f for f in frases if not _eh_alerta(f)]
    observacoes = [i for i in itens if not _eh_alerta(i)]
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

    passos = registro.get("passos") or passos_do_texto
    if passos:
        blocos += ["", "PASSO A PASSO"] + [_numerado(n, p) for n, p in enumerate(passos, 1)]
        if resto:
            blocos += ["", "ENTENDA MELHOR", _quebrar(" ".join(resto), "  ")]
    elif resto:
        blocos += ["", "COMO FAZER"] + [_numerado(n, p) for n, p in enumerate(resto, 1)]

    if observacoes:
        blocos += ["", "BOM SABER"] + [textwrap.fill(o, width=LARGURA, initial_indent="  - ", subsequent_indent="    ")
                                     for o in observacoes]

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
