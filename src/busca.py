from __future__ import annotations

import difflib
import re
import unicodedata

STOPWORDS = {
    "a", "o", "as", "os", "um", "uma", "uns", "umas", "de", "do", "da", "dos", "das",
    "e", "em", "no", "na", "nos", "nas", "para", "pra", "pro", "por", "com", "sem",
    "que", "como", "qual", "quais", "onde", "quando", "eu", "meu", "minha", "me", "se",
    "ao", "aos", "pela", "pelo", "pelas", "pelos", "ou", "num", "numa", "fazer", "faco",
    "quero", "preciso", "posso", "tirar", "sobre", "isso", "esse", "essa", "ter", "tem",
    "ja", "nao", "sim", "mais", "minhas", "meus", "seu", "sua", "ele", "ela", "voce",
    "esta", "estou", "ser", "foi", "vai", "pode", "deve", "precisa", "so", "tambem",
    "depois", "dia", "qualquer", "outro", "outra", "outros", "todas", "todo", "toda",
    "cada",
}

PONTUACAO_MINIMA = 2
CORTE_DIGITACAO = 0.85


def normalizar(texto: str) -> str:
    texto = unicodedata.normalize("NFKD", str(texto))
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    texto = texto.lower()
    texto = re.sub(r"[^a-z0-9]+", " ", texto)
    return " ".join(texto.split())


SUFIXOS = (
    "amentos", "imentos", "amento", "imento", "acoes", "icoes", "acao", "icao",
    "mente", "ando", "endo", "indo", "aram", "eram", "iram",
    "ados", "idos", "adas", "idas", "ado", "ido", "ada", "ida",
    "ar", "er", "ir", "ei", "ou", "eu", "iu", "as", "es", "os", "is",
    "a", "e", "o", "i", "s",
)
RADICAL_MINIMO = 4


def _radical(token: str) -> str:
    for suf in SUFIXOS:
        if token.endswith(suf) and len(token) - len(suf) >= RADICAL_MINIMO:
            return token[: -len(suf)]
    return token


def palavras(texto: str) -> list[str]:
    return [t for t in normalizar(texto).split() if t not in STOPWORDS]


def tokens(texto: str) -> list[str]:
    return [_radical(t) for t in palavras(texto)]


def _contem_sequencia(seq: list[str], sub: list[str]) -> bool:
    n = len(sub)
    return n > 0 and any(seq[i:i + n] == sub for i in range(len(seq) - n + 1))


PESO_EXPRESSAO = 2
PESO_PERGUNTA = 2
PESO_CONTEUDO = 1


def _indices(registro: dict) -> tuple[list[list[str]], set[str], set[str]]:
    expressoes = [tokens(c) for c in registro.get("palavras_chave", [])]
    principal = set(tokens(registro["pergunta_chave"]))
    secundario = set(tokens(registro["conteudo"]))
    for e in expressoes:
        (principal if len(e) == 1 else secundario).update(e)
    return expressoes, principal, secundario - principal


def pontuar(consulta: str, registro: dict) -> int:
    toks = tokens(consulta)
    if not toks:
        return 0
    expressoes, principal, conteudo = _indices(registro)
    pontos = sum(PESO_EXPRESSAO * len(e) for e in expressoes if _contem_sequencia(toks, e))
    bateu_principal = pontos > 0
    for t in set(toks):
        if t in principal:
            pontos += PESO_PERGUNTA
            bateu_principal = True
        elif t in conteudo:
            pontos += PESO_CONTEUDO
    return pontos if bateu_principal else 0


def vocabulario(registros: list[dict]) -> set[str]:
    vocab: set[str] = set()
    for r in registros:
        vocab.update(palavras(r["pergunta_chave"]))
        vocab.update(palavras(r["conteudo"]))
        for chave in r.get("palavras_chave", []):
            vocab.update(palavras(chave))
    return vocab


def corrigir_digitacao(consulta: str, registros: list[dict]) -> str:
    vocab = vocabulario(registros)
    radicais = {_radical(v) for v in vocab}
    saida = []
    for t in palavras(consulta):
        if _radical(t) not in radicais and len(t) >= 5 and not t.isdigit():
            parecidas = difflib.get_close_matches(t, vocab, n=1, cutoff=CORTE_DIGITACAO)
            saida.append(parecidas[0] if parecidas else t)
        else:
            saida.append(t)
    return " ".join(saida)


def buscar_por_palavra_chave(consulta: str, registros: list[dict], limite: int = 3) -> list[dict]:
    if not consulta or not consulta.strip():
        return []
    consulta = corrigir_digitacao(consulta, registros)
    pontuados = [(pontuar(consulta, r), i, r) for i, r in enumerate(registros)]
    pontuados = [p for p in pontuados if p[0] >= PONTUACAO_MINIMA]
    pontuados.sort(key=lambda p: (-p[0], p[1]))
    return [r for _, _, r in pontuados[:limite]]


def melhor_resultado(consulta: str, registros: list[dict]) -> dict | None:
    achados = buscar_por_palavra_chave(consulta, registros, limite=1)
    return achados[0] if achados else None


def empate_no_topo(consulta: str, registros: list[dict]) -> list[dict]:
    if not consulta or not consulta.strip():
        return []
    consulta = corrigir_digitacao(consulta, registros)
    pontos = [(pontuar(consulta, r), r) for r in registros]
    maior = max((p for p, _ in pontos), default=0)
    if maior < PONTUACAO_MINIMA:
        return []
    return [r for p, r in pontos if p == maior]


def listar_temas(registros: list[dict]) -> list[str]:
    vistos: list[str] = []
    for r in registros:
        if r["tema"] not in vistos:
            vistos.append(r["tema"])
    return vistos


def registros_do_tema(tema: str, registros: list[dict]) -> list[dict]:
    return [r for r in registros if r["tema"] == tema]


def buscar_por_id(ident, registros: list[dict]) -> dict | None:
    texto = str(ident).strip()
    if not texto.isdecimal():
        return None
    try:
        n = int(texto)
    except ValueError:
        return None
    return next((r for r in registros if r["id"] == n), None)


def escolher_por_numero(entrada: str, opcoes: list) -> object | None:
    entrada = (entrada or "").strip()
    if not entrada.isdecimal():
        return None
    try:
        n = int(entrada)
    except ValueError:
        return None
    if 1 <= n <= len(opcoes):
        return opcoes[n - 1]
    return None
