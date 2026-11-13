# Resultado do indicador: taxa de acerto

Gerado em 13/11/2026 13:27 com `python src/indicador.py`.

Taxa de acerto geral: 65.3% (32/49 casos avaliados)
  - Palavra-chave: 65.3% (49 casos)

Casos que falharam:
  - [palavra_chave] "quero tirar o RG" -> esperado 1, retornou 2
  - [palavra_chave] "onde consigo minha CTPS" -> esperado 4, retornou 10
  - [palavra_chave] "atestado de nada consta para emprego" -> esperado 5, retornou 1
  - [palavra_chave] "como faço o cartão do SUS" -> esperado 11, falso positivo: o registro 11 não existe e respondeu [3]
  - [palavra_chave] "baixar o Meu SUS Digital" -> esperado 11, falso positivo: o registro 11 não existe e respondeu [4]
  - [palavra_chave] "remédio de graça na farmácia popular" -> esperado 12, falso positivo: o registro 12 não existe e respondeu [2]
  - [palavra_chave] "como conseguir medicamento gratuito" -> esperado 12, falso positivo: o registro 12 não existe e respondeu [1]
  - [palavra_chave] "onde tomar vacina de graça" -> esperado 13, falso positivo: o registro 13 não existe e respondeu [2]
  - [palavra_chave] "como me inscrever no CadÚnico" -> esperado 14, falso positivo: o registro 14 não existe e respondeu [2]
  - [palavra_chave] "atualizar cadastro no CRAS" -> esperado 14, falso positivo: o registro 14 não existe e respondeu [3]
  - [palavra_chave] "não tenho dinheiro para pagar a inscrição do concurso" -> esperado 15, falso positivo: o registro 15 não existe e respondeu [9]
  - [palavra_chave] "receita de bolo de cenoura" -> esperado None, deveria não achar nada, achou [2]
  - [palavra_chave] "previsão do tempo amanhã" -> esperado None, deveria não achar nada, achou [1]
  - [palavra_chave] "documento do carro" -> esperado None, deveria não achar nada, achou [1]
  - [palavra_chave] "cancelar compra" -> esperado 6, retornou 9
  - [palavra_chave] "preciso de um documento" -> esperado None, deveria não achar nada, achou [1]
  - [palavra_chave] "posso votar?" -> esperado 3, nada encontrado

Pendentes (fora da conta):
  - 3 pergunta(s) esperam registros que ainda não existem (ids 12, 13, 15)
  - 5 pergunta(s) aguardando a busca por tema (src/busca_tema.py)
