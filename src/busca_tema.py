"""Busca por escolha de tema (Dia 2 - Miguel).

A base é uma lista de dicionários com os campos padronizados:
id, tema, pergunta_chave, conteudo, referencia, data_verificacao.

A pessoa pode escolher o tema por número (1, 2, 3...), pelo nome
("Serviços", "servicos") ou por uma palavra relacionada ("vacina", "procon").
A busca ignora acentos e maiúsculas e tolera pequenos erros de digitação.
"""

from __future__ import annotations

import difflib
import re
import unicodedata

from erros import AmbiguidadeError, EntradaVaziaError, TemaInexistenteError

# Palavras que levam a cada tema. A chave é o INÍCIO do nome do tema já
# normalizado (sem acento, minúsculo), então funciona mesmo se o time
# escrever "Documentação e Identificação Civil" no JSON.
SINONIMOS = {
    "documentacao": [
        "documentacao", "documento", "documentos", "identidade", "rg", "cin", "cpf",
        "titulo", "eleitor", "eleitoral", "carteira", "trabalho", "antecedentes",
        "certidao", "cadastro", "civil",
    ],
    "direitos": [
        "direitos", "direito", "consumidor", "consumo", "compra", "compras", "garantia",
        "cobranca", "devolucao", "procon", "reclamacao", "cancelamento", "arrependimento",
        "internet", "telecomunicacao",
    ],
    "servicos": [
        "servicos", "servico", "saude", "sus", "vacina", "vacinas", "vacinacao",
        "farmacia", "medicamento", "medicamentos", "remedio", "remedios", "cadunico",
        "cras", "concurso", "concursos", "vestibular", "isencao", "social", "carteira",
        "cadastro", "cartao",
    ],
}


def normalizar(texto: str) -> str:
    """minúsculas, sem acentos, espaços colapsados."""
    texto = unicodedata.normalize("NFKD", str(texto))
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", texto.lower()).strip()


def listar_temas(base: list[dict]) -> list[str]:
    """Temas na ordem em que aparecem na base, sem repetir."""
    vistos: list[str] = []
    for registro in base:
        tema = registro.get("tema")
        if tema and tema not in vistos:
            vistos.append(tema)
    return vistos


def _sinonimos_do_tema(tema: str) -> set[str]:
    norm = normalizar(tema)
    palavras = set(re.findall(r"[a-z0-9]+", norm))
    for chave, lista in SINONIMOS.items():
        if norm.startswith(chave):
            palavras.update(lista)
    return palavras


def _pontuar(tokens: list[str], temas: list[str]) -> dict[str, int]:
    """Quantos tokens da entrada apontam para cada tema (com tolerância a typos)."""
    pontos = {t: 0 for t in temas}
    for token in tokens:
        for tema in temas:
            palavras = _sinonimos_do_tema(tema)
            if token in palavras:
                pontos[tema] += 2
            elif len(token) >= 4 and difflib.get_close_matches(token, palavras, n=1, cutoff=0.8):
                pontos[tema] += 1
    return {t: p for t, p in pontos.items() if p > 0}


def resolver_tema(base: list[dict], escolha) -> str:
    """Converte a escolha da pessoa em um tema da base.

    Levanta EntradaVaziaError, TemaInexistenteError ou AmbiguidadeError.
    """
    temas = listar_temas(base)
    if escolha is None or not str(escolha).strip():
        raise EntradaVaziaError()

    entrada = str(escolha).strip()
    norm = normalizar(entrada)

    # 1) número do menu
    if norm.isdigit():
        indice = int(norm)
        if 1 <= indice <= len(temas):
            return temas[indice - 1]
        raise TemaInexistenteError(entrada, temas)

    # 2) nome do tema (exato ou contido)
    for tema in temas:
        if norm == normalizar(tema):
            return tema
    contidos = [t for t in temas if len(norm) >= 3 and norm in normalizar(t)]
    if len(contidos) == 1:
        return contidos[0]

    # 3) palavras relacionadas / erros de digitação
    tokens = re.findall(r"[a-z0-9]+", norm)
    pontos = _pontuar(tokens, temas)
    if pontos:
        melhor = max(pontos.values())
        lideres = [t for t, p in pontos.items() if p == melhor]
        if len(lideres) == 1:
            return lideres[0]
        raise AmbiguidadeError(entrada, lideres)

    # 4) nada serviu: sugere o tema mais parecido
    parecidos = difflib.get_close_matches(norm, [normalizar(t) for t in temas], n=1, cutoff=0.5)
    sugestao = next((t for t in temas if normalizar(t) == parecidos[0]), None) if parecidos else None
    raise TemaInexistenteError(entrada, temas, sugestao)


def buscar_por_tema(base: list[dict], escolha) -> tuple[str, list[dict]]:
    """Devolve (tema_resolvido, registros_do_tema) na ordem de id."""
    tema = resolver_tema(base, escolha)
    registros = sorted((r for r in base if r.get("tema") == tema), key=lambda r: r.get("id", 0))
    return tema, registros
