import sys

from busca import buscar_por_pergunta
from carregador import carregar_base
from fonte_aviso import formatar_fonte_aviso
from navegacao import buscar_relacionados
from saida import modelo_2_educativo
from tempo_consulta import medir_consulta

try:
    from busca_tema import buscar_por_tema
except ImportError:
    buscar_por_tema = None

try:
    from respostas import formatar_modelo_1
except ImportError:
    formatar_modelo_1 = None

MAX_ENTRADA = 200
MAX_ALTERNATIVAS = 3
NOMES_MODELO = {1: "Direto e Técnico", 2: "Educativo e Detalhado"}


class Saida(Exception):
    """Sinaliza que a pessoa encerrou a entrada (Ctrl+D / Ctrl+Z ou fim do arquivo)."""


def ler(mensagem):
    """input() protegido: limpa espaços e caracteres de controle e corta textos enormes."""
    try:
        texto = input(mensagem)
    except (EOFError, KeyboardInterrupt):
        print()
        raise Saida
    texto = "".join(c for c in texto if c.isprintable())
    return texto.strip()[:MAX_ENTRADA]


def ler_numero(mensagem, maximo):
    """Lê um número entre 0 e maximo. Devolve None se a entrada for inválida."""
    escolha = ler(mensagem)
    # isdecimal + isascii: recusa "²", "١", "-1", "0.5" e "1e9"
    if escolha.isascii() and escolha.isdecimal() and 0 <= int(escolha) <= maximo:
        return int(escolha)
    return None


def mostrar_resposta(registro, modelo):
    """Exibe o registro no modelo escolhido, sempre com fonte e aviso."""
    if modelo == 1 and formatar_modelo_1 is not None:
        texto = formatar_modelo_1(registro, rodape=formatar_fonte_aviso)
    else:
        # sem a base: os assuntos relacionados aparecem logo abaixo, como lista interativa
        texto = modelo_2_educativo(registro, None, rodape=formatar_fonte_aviso)
    print()
    print(texto)


def proximos_assuntos(registro, base, alternativas):
    """Lista outros resultados da pergunta e assuntos do mesmo tema; devolve o escolhido."""
    opcoes = []
    if alternativas:
        print("\nNão era isso? Outros resultados para a sua pergunta:")
        for r in alternativas:
            opcoes.append(r)
            print(f"  {len(opcoes)}. {r['pergunta_chave']}")
    relacionados = [r for r in buscar_relacionados(base, registro) if r not in opcoes]
    if relacionados:
        print(f"\nOutros assuntos de {registro['tema']}:")
        for r in relacionados:
            opcoes.append(r)
            print(f"  {len(opcoes)}. {r['pergunta_chave']}")
    if not opcoes:
        return None
    print("  0. Voltar ao menu")
    escolha = ler_numero("Escolha uma opção (Enter para voltar): ", len(opcoes))
    return opcoes[escolha - 1] if escolha else None


def explorar(registro, base, modelo, alternativas=None):
    """Mostra a resposta e permite seguir para outro resultado ou assunto relacionado."""
    while registro is not None:
        mostrar_resposta(registro, modelo)
        registro = proximos_assuntos(registro, base, alternativas)
        alternativas = None


def opcao_pergunta(base, modelo):
    """Busca por pergunta livre, com o tempo da consulta."""
    pergunta = ler("\nDigite sua pergunta (Enter para voltar): ")
    if not pergunta:
        print("Nenhuma pergunta digitada. Voltando ao menu.")
        return
    resultados, segundos = medir_consulta(buscar_por_pergunta, pergunta, base)
    if not resultados:
        print("Não encontrei esse assunto na base. Tente outras palavras ou use a busca por tema.")
        print(f"(Consulta em {segundos * 1000:.2f} ms)")
        return
    print(f"(Consulta em {segundos * 1000:.2f} ms, {len(resultados)} resultado(s))")
    explorar(resultados[0], base, modelo, resultados[1:1 + MAX_ALTERNATIVAS])


def opcao_tema(base, modelo):
    """Busca por tema: escolhe o tema e depois o assunto."""
    if buscar_por_tema is None:
        print("\nA busca por tema ainda está em desenvolvimento (src/busca_tema.py).")
        return
    temas = sorted({r["tema"] for r in base})
    print("\nTemas disponíveis:")
    for numero, tema in enumerate(temas, start=1):
        print(f"  {numero}. {tema}")
    print("  0. Voltar ao menu")
    entrada = ler("Digite o número ou o nome do tema: ")
    if not entrada or entrada == "0":
        return
    if entrada.isascii() and entrada.isdecimal() and 1 <= int(entrada) <= len(temas):
        entrada = temas[int(entrada) - 1]
    try:
        tema, registros = buscar_por_tema(base, entrada)
    except Exception:
        print("Tema não encontrado. Escolha um dos temas da lista.")
        return
    if not registros:
        print("Esse tema não tem assuntos cadastrados.")
        return
    print(f"\nAssuntos de {tema}:")
    for numero, r in enumerate(registros, start=1):
        print(f"  {numero}. {r['pergunta_chave']}")
    print("  0. Voltar ao menu")
    escolha = ler_numero("Escolha um assunto: ", len(registros))
    if escolha is None:
        print("Opção inválida. Voltando ao menu.")
        return
    if escolha:
        explorar(registros[escolha - 1], base, modelo)


def opcao_modelo(modelo):
    """Alterna entre os dois modelos de resposta."""
    if formatar_modelo_1 is None:
        print("\nO Modelo 1 (Direto e Técnico) ainda está em desenvolvimento (src/respostas.py).")
        return modelo
    novo = 2 if modelo == 1 else 1
    print(f"\nFormato das respostas alterado para Modelo {novo}: {NOMES_MODELO[novo]}.")
    return novo


def menu(base):
    """Loop principal. Sai pela opção 0 ou ao terminar a entrada."""
    modelo = 1 if formatar_modelo_1 is not None else 2
    print("=" * 72)
    print("CitizenTech: orientação ao cidadão")
    print(f"{len(base)} orientações sobre documentação, direitos do consumidor e serviços.")
    print("=" * 72)
    while True:
        print("\nMENU PRINCIPAL")
        print("  1. Fazer uma pergunta")
        print("  2. Buscar por tema")
        print(f"  3. Trocar formato da resposta (atual: Modelo {modelo}, {NOMES_MODELO[modelo]})")
        print("  0. Sair")
        opcao = ler("Escolha uma opção: ")
        if opcao == "1":
            opcao_pergunta(base, modelo)
        elif opcao == "2":
            opcao_tema(base, modelo)
        elif opcao == "3":
            modelo = opcao_modelo(modelo)
        elif opcao == "0":
            return
        elif not opcao:
            print("Nenhuma opção digitada. Escolha 1, 2, 3 ou 0.")
        else:
            print("Opção inválida. Escolha 1, 2, 3 ou 0.")


def main():
    try:
        sys.stdout.reconfigure(errors="replace")
    except AttributeError:
        pass
    base = carregar_base()
    if not base:
        print("Não foi possível iniciar: a base de conhecimento está vazia ou indisponível.")
        return 1
    try:
        menu(base)
    except Saida:
        pass
    print("Até logo! Confirme sempre as informações nos canais oficiais.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())