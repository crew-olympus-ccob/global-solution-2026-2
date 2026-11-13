# Guia para escrever os registros (equipe)

Arquivo: `data/base_conhecimento.json`. É uma **lista**. Cada um acrescenta os
seus registros no fim, seguindo o modelo dos registros 1 a 5 (Gabriel).

## Numeração combinada

| Tema | ids |
|---|---|
| Documentação e Identificação Civil | 1 a 5 (Gabriel, prontos) |
| Direitos do Consumidor | 6 a 10 |
| Saúde Pública e Serviços Comunitários | 11 a 15 |

Use **exatamente** o mesmo texto de `tema` em todos os registros do mesmo tema:
o menu agrupa pelo texto, e "Saúde" ≠ "Saúde Pública".

## Campos

| Campo | Obrigatório | O que escrever |
|---|---|---|
| `id` | sim | número inteiro da tabela acima |
| `tema` | sim | nome do tema, igual em todos os registros dele |
| `pergunta_chave` | sim | a pergunta como o cidadão faria. Ex.: "Como emitir o Cartão do SUS?" |
| `conteudo` | sim | a orientação, em frases curtas. **Uma ação por frase.** Comece com a resposta principal |
| `referencia` | sim | link oficial (gov.br, tse.jus.br, planalto.gov.br…) |
| `data_verificacao` | sim | dia em que **você conferiu** a fonte, `AAAA-MM-DD` |
| `palavras_chave` | **recomendado** | como as pessoas **falam**: `["remedio gratis", "farmacia popular"]`. Sem acento também funciona |
| `passos` | opcional | lista com o passo a passo; se existir, o Modelo 2 mostra "PASSO A PASSO" |
| `alerta` | opcional | golpe comum, prazo que vence, o que não fazer |
| `autor` | opcional | seu nome |

### Por que `palavras_chave` importa

Sem elas, a busca só enxerga as palavras da `pergunta_chave`. Medimos isso: com
os registros 1 a 5 sem palavras-chave, "quero tirar o RG", "onde consigo minha
CTPS" e "posso votar?" **não achavam nada**. Com elas, acham.

**Evite palavras-chave genéricas** ("documento", "cadastro", "digital",
"cancelar"). Elas fazem o programa responder o assunto errado. Uma expressão
composta como `"multa eleitoral"` só conta quando aparece inteira; já uma
palavra solta como `"multa"` conta sempre.

### Como o Modelo 2 usa o `conteudo`

O texto é dividido em frases:
- a **1ª frase** vira "EM RESUMO";
- as demais viram a lista "COMO FAZER";
- frases que começam com *Desconfie, Cuidado, Atenção, Nunca, Evite, Não* vão
  para "ATENÇÃO".

Por isso: **comece pela resposta**, uma ação por frase, e os avisos começando
com uma dessas palavras.

## Checklist antes de subir

1. `python -m unittest discover -s tests` passou.
2. `python src/indicador.py`: meus ids não aparecem em "falharam" nem em "falso positivo".
3. Acrescentei perguntas em `tests/perguntas_teste.json`
   (`{"pergunta": "...", "id_esperado": N}`), de preferência para os temas **dos colegas**.
4. A informação veio da fonte oficial, não de IA nem de blog.
