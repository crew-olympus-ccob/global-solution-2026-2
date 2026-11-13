"""Tratamento dos 3 cenários de erro do protótipo (Dia 4 - Miguel).

Cenários exigidos:
  1. Entrada vazia        -> EntradaVaziaError
  2. Tema inexistente     -> TemaInexistenteError
  3. Ambiguidade          -> AmbiguidadeError (a pessoa escolhe entre as opções)

Regra de ouro: nenhum desses erros pode derrubar o programa. Quem chama usa
`executar_seguro(...)` ou captura `ErroDeConsulta`.
"""

from __future__ import annotations


class ErroDeConsulta(Exception):
    """Base dos erros previstos. Sempre traz uma mensagem pronta para a pessoa."""

    def __init__(self, mensagem: str):
        super().__init__(mensagem)
        self.mensagem = mensagem


class EntradaVaziaError(ErroDeConsulta):
    def __init__(self):
        super().__init__(
            "Você não digitou nada. Escreva uma pergunta ou o nome/número de um tema "
            "(ex.: 'vacina', 'cadunico' ou '3')."
        )


class TemaInexistenteError(ErroDeConsulta):
    def __init__(self, entrada: str, temas_disponiveis: list[str], sugestao: str | None = None):
        self.entrada = entrada
        self.temas_disponiveis = temas_disponiveis
        self.sugestao = sugestao
        msg = f"Não encontrei nenhum tema para \"{entrada}\"."
        if sugestao:
            msg += f" Você quis dizer \"{sugestao}\"?"
        msg += " Temas disponíveis: " + "; ".join(
            f"{i}) {t}" for i, t in enumerate(temas_disponiveis, 1)
        ) + "."
        super().__init__(msg)


class AmbiguidadeError(ErroDeConsulta):
    """A entrada combina com mais de uma opção (temas ou registros)."""

    def __init__(self, entrada: str, opcoes: list[str]):
        self.entrada = entrada
        self.opcoes = opcoes
        super().__init__(
            f"\"{entrada}\" pode significar mais de uma coisa. Qual destes você quer? "
            + "; ".join(f"{i}) {o}" for i, o in enumerate(opcoes, 1))
        )


def executar_seguro(funcao, *args, **kwargs):
    """Chama `funcao` sem deixar um ErroDeConsulta quebrar o programa.

    Retorna (True, resultado) em caso de sucesso ou (False, erro) se houve um
    ErroDeConsulta previsto. Qualquer outra exceção é um bug de verdade e sobe.
    """
    try:
        return True, funcao(*args, **kwargs)
    except ErroDeConsulta as erro:
        return False, erro


def escolher_opcao(opcoes: list[str], entrada_fn=input, saida_fn=print, tentativas: int = 3):
    """Resolve uma ambiguidade pedindo que a pessoa digite o número da opção.

    Devolve o índice (0-based) escolhido, ou None se a pessoa desistir
    (Enter vazio) ou errar `tentativas` vezes. Nunca levanta exceção.
    """
    for i, opcao in enumerate(opcoes, 1):
        saida_fn(f"  {i}) {opcao}")
    for _ in range(tentativas):
        try:
            resposta = entrada_fn("Digite o número da opção (Enter para cancelar): ").strip()
        except (EOFError, KeyboardInterrupt):
            return None
        if not resposta:
            return None
        if resposta.isdigit() and 1 <= int(resposta) <= len(opcoes):
            return int(resposta) - 1
        saida_fn(f"Opção inválida. Escolha um número de 1 a {len(opcoes)}.")
    saida_fn("Muitas tentativas inválidas; voltando ao menu.")
    return None
