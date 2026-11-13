from __future__ import annotations

import io
from contextlib import redirect_stdout
from datetime import date
from pathlib import Path

import carregador

RAIZ = Path(__file__).resolve().parent.parent
CAMINHO_PADRAO = Path(carregador.CAMINHO_PADRAO).resolve()

CAMPOS_OBRIGATORIOS = ("id", "tema", "pergunta_chave", "conteudo", "referencia", "data_verificacao")

AVISO_LIMITACAO = (
    "Este assistente é informativo e não substitui orientação jurídica, médica "
    "ou o atendimento do órgão oficial. Confirme sempre na fonte indicada."
)


class ErroBase(Exception):
    pass


def _lista_de_textos(valor, campo: str, ident) -> list[str]:
    if valor is None or valor == "":
        return []
    if isinstance(valor, str):
        valor = [valor]
    if not isinstance(valor, list):
        raise ErroBase(f"Registro {ident}: '{campo}' deve ser uma lista de textos.")
    return [str(v).strip() for v in valor if str(v).strip()]


def normalizar_registro(bruto: dict, posicao: int = 0) -> dict:
    if not isinstance(bruto, dict):
        raise ErroBase(f"Item na posição {posicao} não é um registro (objeto JSON).")

    ident = bruto.get("id", f"na posição {posicao}")
    faltando = [c for c in CAMPOS_OBRIGATORIOS if bruto.get(c) in (None, "")]
    if faltando:
        raise ErroBase(f"Registro {ident}: campo(s) obrigatório(s) ausente(s) ou vazio(s): {', '.join(faltando)}.")

    if isinstance(bruto["id"], bool) or not str(bruto["id"]).strip().isdecimal():
        raise ErroBase(f"Registro {ident}: 'id' deve ser um número inteiro (ex.: 6).")

    try:
        date.fromisoformat(str(bruto["data_verificacao"]))
    except ValueError:
        raise ErroBase(
            f"Registro {ident}: 'data_verificacao' deve estar no formato AAAA-MM-DD "
            f"(recebido: {bruto['data_verificacao']!r})."
        ) from None

    return {
        "id": int(str(bruto["id"]).strip()),
        "tema": str(bruto["tema"]).strip(),
        "pergunta_chave": str(bruto["pergunta_chave"]).strip(),
        "conteudo": str(bruto["conteudo"]).strip(),
        "referencia": str(bruto["referencia"]).strip(),
        "data_verificacao": str(bruto["data_verificacao"]).strip(),
        "palavras_chave": _lista_de_textos(bruto.get("palavras_chave"), "palavras_chave", ident),
        "passos": _lista_de_textos(bruto.get("passos"), "passos", ident),
        "alerta": str(bruto.get("alerta") or "").strip(),
        "autor": str(bruto.get("autor") or "").strip(),
    }


def carregar_base(caminho: str | Path | None = None) -> list[dict]:
    caminho = Path(caminho) if caminho else CAMINHO_PADRAO
    saida_carregador = io.StringIO()
    with redirect_stdout(saida_carregador):
        brutos = carregador.carregar_base(str(caminho))
    if not brutos:
        motivo = saida_carregador.getvalue().strip() or "A base não tem nenhum registro."
        if motivo.startswith("Erro: "):
            motivo = motivo[len("Erro: "):]
        raise ErroBase(motivo)

    registros = [normalizar_registro(r, i) for i, r in enumerate(brutos)]

    vistos: set[int] = set()
    for r in registros:
        if r["id"] in vistos:
            raise ErroBase(f"ID repetido na base: {r['id']}")
        vistos.add(r["id"])
    return registros
