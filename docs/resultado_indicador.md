# Resultado do indicador: taxa de acerto

Gerado em 16/11/2026 15:36 com `python src/indicador.py`.

Taxa de acerto geral: 81.0% (51/63 casos avaliados)
  - Menu (tema > assunto): 100.0% (5 casos)
  - Palavra-chave: 79.3% (58 casos)

Casos que falharam:
  - [palavra_chave] "quero tirar o RG" -> esperado 1, retornou 2
  - [palavra_chave] "onde consigo minha CTPS" -> esperado 4, retornou 10
  - [palavra_chave] "atestado de nada consta para emprego" -> esperado 5, retornou 12
  - [palavra_chave] "como me inscrever no CadÚnico" -> esperado 14, retornou 15
  - [palavra_chave] "receita de bolo de cenoura" -> esperado None, deveria não achar nada, achou [2]
  - [palavra_chave] "previsão do tempo amanhã" -> esperado None, deveria não achar nada, achou [1]
  - [palavra_chave] "meu celular novo estragou" -> esperado 7, retornou 11
  - [palavra_chave] "documento do carro" -> esperado None, deveria não achar nada, achou [13]
  - [palavra_chave] "remédio no posto de saúde" -> esperado 12, retornou 11
  - [palavra_chave] "cancelar compra" -> esperado 6, retornou 9
  - [palavra_chave] "preciso de um documento" -> esperado None, deveria não achar nada, achou [13]
  - [palavra_chave] "posso votar?" -> esperado 3, nada encontrado
