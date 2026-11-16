import sys
import textwrap
import unicodedata

from busca import buscar_por_pergunta
from carregador import carregar_base
from erros import AmbiguidadeError, ErroDeConsulta, TemaInexistenteError, escolher_opcao
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
MAX_TENTATIVAS = 3

# Nome completo, resumo e fontes de cada tema. A chave é o início do nome do
# tema no JSON, sem acento e em minúsculas, então funciona tanto com
# "Serviços" quanto com "Saúde Pública e Serviços Comunitários".
TEMAS_INFO = [
    ("documentacao", "Documentação e Identificação Civil",
     "CIN/RG, CPF, título de eleitor, Carteira de Trabalho Digital e antecedentes criminais.",
     "gov.br, TSE e Receita Federal"),
    ("direitos", "Direitos do Consumidor",
     "Arrependimento em compras online, garantia, cobrança indevida, cancelamento de "
     "internet/telefone e reclamação no Consumidor.gov.br.",
     "Código de Defesa do Consumidor (Lei nº 8.078/1990), Procon e Consumidor.gov.br"),
    ("saude", "Saúde Pública e Serviços Comunitários",
     "Cartão do SUS, Farmácia Popular, vacinação, CadÚnico no CRAS e isenção de taxas em "
     "concursos e vestibulares.",
     "Ministério da Saúde, Ministério do Desenvolvimento Social e gov.br"),
    ("servicos", "Saúde Pública e Serviços Comunitários",
     "Cartão do SUS, Farmácia Popular, vacinação, CadÚnico no CRAS e isenção de taxas em "
     "concursos e vestibulares.",
     "Ministério da Saúde, Ministério do Desenvolvimento Social e gov.br"),
]


def normalizar(texto):
    """Minúsculas, sem acentos e com espaços simples (para comparar nomes)."""
    texto = unicodedata.normalize("NFKD", str(texto))
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return " ".join(texto.lower().split())


def info_tema(tema):
    """Devolve (nome completo, resumo, fontes) de um tema da base."""
    norm = normalizar(tema)
    for chave, nome, resumo, fontes in TEMAS_INFO:
        if norm.startswith(chave):
            return nome, resumo, fontes
    return tema, "", ""


def nome_tema(tema):
    return info_tema(tema)[0]


def temas_da_base(base):
    """Temas na ordem em que aparecem na base (Documentação = 1, Direitos = 2...)."""
    temas = []
    for registro in sorted(base, key=lambda r: r.get("id", 0)):
        if registro.get("tema") and registro["tema"] not in temas:
            temas.append(registro["tema"])
    return temas


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
        print(f"\nOutros assuntos de {nome_tema(registro['tema'])}:")
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


def mostrar_temas(base, temas):
    """Lista os temas com nome completo, quantidade de assuntos, resumo e fontes."""
    print("\nBUSCAR POR TEMA")
    for numero, tema in enumerate(temas, start=1):
        nome, resumo, fontes = info_tema(tema)
        quantidade = sum(1 for r in base if r.get("tema") == tema)
        print(f"\n  {numero}. {nome} ({quantidade} assuntos)")
        if resumo:
            print(textwrap.fill(resumo, width=72, initial_indent="     ", subsequent_indent="     "))
        if fontes:
            print(textwrap.fill(f"Fontes: {fontes}", width=72, initial_indent="     ",
                                subsequent_indent="             "))
    print("\n  0. Voltar ao menu")


def escolher_tema(base, temas):
    """Pede o tema por número, nome ou palavra relacionada. Devolve o tema ou None."""
    for _ in range(MAX_TENTATIVAS):
        entrada = ler("\nDigite o número, o nome do tema ou uma palavra (ex.: vacina, cpf, procon): ")
        if not entrada or entrada == "0":
            return None
        if entrada.isascii() and entrada.isdecimal() and 1 <= int(entrada) <= len(temas):
            return temas[int(entrada) - 1]
        for tema in temas:
            if normalizar(entrada) == normalizar(nome_tema(tema)):
                return tema
        try:
            tema, _ = buscar_por_tema(base, entrada)
            return tema
        except AmbiguidadeError as erro:
            print(f"\n\"{entrada}\" aparece em mais de um tema. Qual deles você quer?")
            indice = escolher_opcao([nome_tema(o) for o in erro.opcoes], entrada_fn=ler)
            return None if indice is None else erro.opcoes[indice]
        except TemaInexistenteError as erro:
            mensagem = f"Não encontrei um tema para \"{entrada}\"."
            if erro.sugestao:
                mensagem += f" Você quis dizer \"{nome_tema(erro.sugestao)}\"?"
            print(mensagem + f" Digite um número de 1 a {len(temas)}.")
        except ErroDeConsulta as erro:
            print(erro.mensagem)
    print("Muitas tentativas inválidas. Voltando ao menu.")
    return None


def opcao_tema(base, modelo):
    """Busca por tema: escolhe o tema e depois o assunto."""
    if buscar_por_tema is None:
        print("\nA busca por tema ainda está em desenvolvimento (src/busca_tema.py).")
        return
    temas = temas_da_base(base)
    mostrar_temas(base, temas)
    tema = escolher_tema(base, temas)
    if tema is None:
        return
    registros = sorted((r for r in base if r.get("tema") == tema), key=lambda r: r.get("id", 0))
    if not registros:
        print("Esse tema não tem assuntos cadastrados.")
        return
    while True:
        print(f"\n{nome_tema(tema).upper()}")
        for numero, r in enumerate(registros, start=1):
            print(textwrap.fill(r["pergunta_chave"], width=72, initial_indent=f"  {numero}. ",
                                subsequent_indent="     "))
        print("  0. Voltar ao menu principal")
        escolha = ler_numero("Escolha um assunto: ", len(registros))
        if escolha is None:
            print(f"Opção inválida. Digite um número de 0 a {len(registros)}.")
            continue
        if escolha == 0:
            return
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
    nomes = [nome_tema(t) for t in temas_da_base(base)]
    print(f"{len(base)} orientações sobre: " + ", ".join(nomes) + ".")
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