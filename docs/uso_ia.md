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
| Claude (Anthropic) | Modelo 2 (`src/saida.py`), indicador (`src/indicador.py`), testes em `tests/`, rascunho deste arquivo | [nome do responsável] |
| [outra ferramenta, se houver] | [uso] | [nome] |

## 2. Como a IA apoiou a estruturação de prompts

Escrevemos os pedidos à IA com **contexto, restrições e critério de pronto**,
em vez de pedidos genéricos. Exemplos reais do que foi pedido:

1. **Testar a parte de cada integrante**
   > "Projeto em Python, só biblioteca padrão, dividido entre 5 pessoas. A base é
   > um JSON com id, tema, pergunta_chave, conteudo, referencia e
   > data_verificacao. Escreva testes que usem as funções dos colegas pelos nomes
   > combinados e fiquem aguardando enquanto o arquivo de cada um não existir."

   *Decisão nossa a partir da resposta:* os testes da busca por tema, do Modelo 1
   e do menu (`sistema.py`) ficam marcados como "aguardando" até o código chegar,
   e passam a rodar sozinhos quando ele entrar no repositório.

2. **Formato do Modelo 2**
   > "Defina seções fixas para uma resposta educativa: resumo, passo a passo,
   > atenção e assuntos relacionados. Seção sem conteúdo não deve aparecer em
   > branco. A fonte e o aviso vêm de outra função, feita por outro integrante."

3. **Testes de entradas estranhas**
   > "Liste entradas de teclado que costumam quebrar programas de terminal em
   > Python (Enter vazio, Ctrl+D, números negativos, decimais, caracteres Unicode
   > que parecem dígitos, textos enormes, emojis)."

   Essa lista virou a lista `ESTRANHAS` em `tests/test_integracao.py`, usada para
   testar o programa de verdade no terminal.

## 3. Como a IA apoiou os testes e o indicador

- **Perguntas de teste** (`tests/perguntas_extras.json`): a IA sugeriu frases no jeito que
  um cidadão escreveria ("perdi meu CPF", "comprei pela internet e me arrependi").
  Revisamos e acrescentamos casos próprios.
- **Ponto crítico que identificamos:** na primeira rodada o indicador deu **100%**.
  Concluímos que o número estava **viciado**: as mesmas pessoas (e a mesma IA)
  escreveram as palavras-chave e as perguntas de teste. Por isso incluímos casos
  **difíceis** (erro de digitação, sinônimo, assunto fora da base) marcados com
  `"dificil": true`, e a taxa passou a mostrar as limitações reais.
- **Segundo ponto cego:** perguntas sobre assuntos que ainda não estavam na base
  eram ignoradas pelo indicador. Ao conferir, várias recebiam uma resposta
  **errada** de outro tema. Passamos a contar isso como erro ("falso positivo").
- **Peças provisórias retiradas:** para testar antes de o código do grupo
  existir, a IA chegou a escrever uma busca, um menu e um programa principal
  provisórios. Eles foram retirados para não duplicar as partes dos colegas, e o
  indicador e os testes passaram a usar o código oficial de cada um.
- **Casos que continuam falhando** ficam no arquivo de propósito, porque mostram as
  limitações reais (ver `docs/resultado_indicador.md`).

## 4. O que a IA NÃO fez

- Não escreveu nem validou as orientações da base. Cada registro tem `autor`,
  `referencia` e `data_verificacao` preenchidos por um integrante.
- Não decidiu sozinha: todo código gerado foi lido, executado e testado pela equipe
  (`python -m unittest discover -s tests`).
- Não substitui orientação jurídica ou médica. O aviso de limitação aparece nas
  respostas.

## 5. Limitações e riscos que consideramos

- **Alucinação:** IA pode inventar prazos, artigos de lei ou links. Por isso nada
  da base veio da IA sem conferência na fonte oficial.
- **Viés do teste:** quem escreve a base e os testes tende a acertar o próprio
  vocabulário. Mitigação: casos difíceis e testes cruzados entre integrantes.
- **Busca por palavra-chave tem teto:** sinônimos que não aparecem no texto
  ("estragou" × "defeito") não são encontrados.

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
