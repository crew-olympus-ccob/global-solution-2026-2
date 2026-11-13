import json
import unicodedata
import re

# Palavras comuns que não ajudam a identificar o assunto
STOPWORDS = {
    "a", "o", "as", "os", "de", "do", "da", "dos", "das", "em", "no", "na",
    "nos", "nas", "para", "por", "com", "como", "qual", "quais", "que", "um",
    "uma", "e", "ou", "se", "ao", "aos", "pelo", "pela", "sobre", "fazer", "ter"
}

def normalizar_texto(texto: str) -> str:
    """Remove acentos, pontuação e converte para minúsculas."""
    texto = texto.lower().strip()
    # Remove acentos
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    # Mantém apenas letras, números e espaços
    texto = re.sub(r"[^a-z0-9\s]", " ", texto)
    return texto

def extrair_palavras_chave(pergunta: str) -> list:
    """Quebra a pergunta em uma lista de palavras relevantes."""
    texto_limpo = normalizar_texto(pergunta)
    palavras = texto_limpo.split()
    # Filtra stopwords e palavras muito curtas (ex: 'de', 'o')
    return [p for p in palavras if p not in STOPWORDS and len(p) > 2]

def buscar_por_pergunta(pergunta: str, base_dados: list) -> list:
    """
    Busca registros na base (lista de dicionários) por correspondência parcial.
    Retorna uma lista de dicionários ordenados pela maior pontuação de relevância.
    """
    palavras_busca = extrair_palavras_chave(pergunta)
    
    # Se o usuário digitou apenas stopwords ou algo inválido
    if not palavras_busca:
        return []

    resultados_pontuados = []

    for registro in base_dados:
        pontuacao = 0
        
        pergunta_reg = normalizar_texto(registro.get("pergunta_chave", ""))
        tema_reg = normalizar_texto(registro.get("tema", ""))
        conteudo_reg = normalizar_texto(registro.get("conteudo", ""))

        for palavra in palavras_busca:
            # Correspondência parcial (ex: "cancelar" encontra "cancelamento")
            raiz = palavra[:5] if len(palavra) >= 6 else palavra

            if raiz in pergunta_reg:
                pontuacao += 3  # Peso maior se bater com a pergunta principal
            if raiz in tema_reg:
                pontuacao += 2  # Peso médio se bater com o tema
            if raiz in conteudo_reg:
                pontuacao += 1  # Peso menor se aparecer apenas no texto

        if pontuacao > 0:
            resultados_pontuados.append({
                "pontuacao": pontuacao,
                "registro": registro
            })

    # Ordena do maior score para o menor
    resultados_pontuados.sort(key=lambda item: item["pontuacao"], reverse=True)
    
    # Retorna apenas a lista de registros ordenados
    return [item["registro"] for item in resultados_pontuados]