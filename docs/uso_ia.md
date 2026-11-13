# Uso de Inteligência Artificial no projeto

> **Status:** rascunho da seção de Git/Admin/Integração. Cada integrante completa a
> parte **"Uso por integrante"** com o que *de fato* fez com IA. Não inventem uso
> que não houve, porque a banca pode perguntar.

## 1. Resumo

Usamos ferramentas de IA generativa como **apoio** para estruturar o código,
os prompts de trabalho e, principalmente, os **testes**. A IA **não** foi usada
como fonte das orientações ao cidadão: todo o conteúdo da base
(`data/base_conhecimento.json`) foi escrito pelos integrantes a partir de fontes
oficiais, com referência e data de verificação em cada registro.

| Ferramenta | Onde ajudou | Quem revisou |
|---|---|---|
| Claude (Anthropic) | Estrutura do código em `src/`, testes em `tests/`, formato do Modelo 2, cálculo do indicador, rascunho deste arquivo | [nome do responsável] |
| [outra ferramenta, se houver] | [uso] | [nome] |

## 2. Como a IA apoiou a estruturação de prompts

Escrevemos os pedidos à IA com **contexto, restrições e critério de pronto**,
em vez de pedidos genéricos. Exemplos reais do que foi pedido:

1. **Estrutura do programa**
   > "Projeto de assistente em Python, só biblioteca padrão. A base é um JSON com
   > registros (id, tema, pergunta_chave, conteudo, referencia, data de
   > verificação). Preciso de duas formas de busca (palavra-chave e menu por
   > tema) e de uma saída 'educativa e detalhada'. Separe leitura do JSON,
   > busca e formatação em módulos diferentes."

   *Decisão nossa a partir da resposta:* só `src/base.py` conhece os campos do
   JSON. A primeira versão gerada usava outro formato e precisou ser adaptada ao
   formato que a equipe já tinha adotado (`carregador.py` e os registros 1 a 5).

2. **Formato do Modelo 2**
   > "Defina seções fixas para uma resposta educativa: o que fazer, passo a passo,
   > por que isso importa, atenção, fonte com data. Seção sem conteúdo não deve
   > aparecer em branco."

3. **Testes de entradas estranhas**
   > "Liste entradas de teclado que costumam quebrar programas de terminal em
   > Python (Enter vazio, Ctrl+D, números negativos, decimais, caracteres Unicode
   > que parecem dígitos, textos enormes, emojis)."

   Essa lista virou a classe `TestEntradasEstranhas` em
   `tests/test_integracao.py`, e a equipe completou com os casos encontrados na
   validação manual.

## 3. Como a IA apoiou os testes e o indicador

- **Perguntas de teste** (`tests/perguntas_teste.json`): a IA sugeriu frases no jeito que
  um cidadão escreveria ("perdi meu CPF", "comprei pela internet e me arrependi").
  Revisamos e acrescentamos casos próprios.
- **Ponto crítico que identificamos:** na primeira rodada o indicador deu **100%**.
  Concluímos que o número estava **viciado**: as mesmas pessoas (e a mesma IA)
  escreveram as palavras-chave e as perguntas de teste. Por isso incluímos casos
  **difíceis** (erro de digitação, sinônimo, assunto fora da base) marcados com
  `"dificil": true`. A taxa caiu, e os erros mostraram o que melhorar:
  - erro de digitação ("identidae") → corrigido com `difflib` (biblioteca padrão);
  - palavra genérica sozinha ("documento do carro") respondia errado → nota mínima 2;
  - verbo conjugado ("comprei", "arrependi") não casava → remoção de terminações (radical simples).
- **Segundo ponto cego:** perguntas sobre assuntos que ainda não estavam na base
  eram ignoradas pelo indicador. Ao conferir, 11 delas recebiam uma resposta
  **errada** de outro tema (ex.: "atualizar cadastro no CRAS" respondia com o
  registro do CPF). Passamos a contar isso como erro ("falso positivo") e
  corrigimos a busca: palavras que só aparecem no texto do conteúdo não bastam
  para responder, e o radical das palavras deixou de juntar "compra" com
  "comprovante".
- **Casos que continuam falhando** ficam no arquivo de propósito, porque mostram as
  limitações reais (ver `docs/resultado_indicador.md`).

## 4. O que a IA NÃO fez

- Não escreveu nem validou as orientações da base. Cada registro tem `autor`,
  `referencia` e `data_verificacao` preenchidos por um integrante.
- Não decidiu sozinha: todo código gerado foi lido, executado e testado pela equipe
  (`python -m unittest discover -s tests`).
- Não substitui orientação jurídica ou médica. O programa mostra esse aviso em
  toda resposta do Modelo 2.

## 5. Limitações e riscos que consideramos

- **Alucinação:** IA pode inventar prazos, artigos de lei ou links. Por isso nada
  da base veio da IA sem conferência na fonte oficial.
- **Viés do teste:** quem escreve a base e os testes tende a acertar o próprio
  vocabulário. Mitigação: casos difíceis e testes cruzados entre integrantes.
- **Busca por palavra-chave tem teto:** sinônimos que não estão na base
  ("estragou" × "defeito") não são encontrados. Melhorar exige ampliar as
  palavras-chave, não só o código.

## 6. Uso por integrante

> Cada um preenche a sua linha. Se não usou IA, escreva "não usei".

| Integrante | Ferramenta | Para quê | O que foi conferido / alterado |
|---|---|---|---|
| Pedro Lima: Git/Admin, Integração, Modelo 2, Indicador | Claude | estrutura do código, testes, este documento | [preencher] |
| [nome] | | | |
| [nome] | | | |
| [nome] | | | |
| [nome] | | | |

---
*Última atualização: 12/11/2026.*
