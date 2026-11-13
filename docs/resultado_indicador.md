# Resultado do indicador: taxa de acerto

Gerado em 13/11/2026 11:40 com `python src/indicador.py`.

Taxa de acerto geral: 91.7% (44/48 casos avaliados)
  - Menu (tema > assunto): 100.0% (5 casos)
  - Palavra-chave: 90.7% (43 casos)

Casos que falharam:
  - [palavra_chave] "baixar o Meu SUS Digital" -> esperado 11, falso positivo: o registro 11 não existe e respondeu [4]
  - [palavra_chave] "não tenho dinheiro para pagar a inscrição do concurso" -> esperado 15, falso positivo: o registro 15 não existe e respondeu [9]
  - [palavra_chave] "meu celular novo estragou" -> esperado 7, nada encontrado
  - [palavra_chave] "cancelar compra" -> esperado 6, ambíguo: 6, 9

Pendentes (fora da conta): 9 pergunta(s) esperam registros que ainda não existem (ids 11, 12, 13, 14, 15).
