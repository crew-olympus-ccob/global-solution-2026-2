# Uso de Inteligência Artificial no projeto

## 1. Resumo

Usamos ferramentas de IA generativa como **apoio** para estruturar o código,
os prompts de trabalho, os testes e a documentação. A IA também ajudou na
revisão e na redação de ajustes em orientações da base. As fontes oficiais
consultadas estão registradas na base e em `docs/revisao_base.md`.

| Ferramenta         | Onde ajudou                                                                                                     | Quem revisou   |
| ------------------ | --------------------------------------------------------------------------------------------------------------- | -------------- |
| Claude (Anthropic) | Modelo 2 (`src/saida.py`), indicador (`src/indicador.py`), testes em `tests/`, rascunho deste arquivo           | Pedro Lima     |
| Codex (OpenAI)     | Revisão da base e das referências, documentação, função de fonte e aviso, medição do tempo e execução de testes | Lucas Carvalho |

## 2. Como a IA apoiou a estruturação de prompts

Escrevemos os pedidos à IA com **contexto, restrições e critério de pronto**,
em vez de pedidos genéricos. Exemplos reais do que foi pedido:

1. **Testar a parte de cada integrante**

   > "Projeto em Python, só biblioteca padrão, dividido entre 5 pessoas. A base é
   > um JSON com id, tema, pergunta_chave, conteudo, referencia e
   > data_verificacao. Escreva testes que usem as funções dos colegas pelos nomes
   > combinados e fiquem aguardando enquanto o arquivo de cada um não existir."

   _Decisão nossa a partir da resposta:_ os testes da busca por tema, do Modelo 1
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

## 4. Limites do uso de IA

- A revisão assistida por IA comparou orientações com fontes oficiais; os registros
  contêm `referencia` e `data_verificacao`, sem campo individual de autor.
- O código deve ser revisado pelos integrantes; os testes podem ser executados com
  `python -m unittest discover -s tests`.
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

| Integrante                                             | Ferramenta     | Para quê                                                                                      | O que foi conferido / alterado                                                                                                                                                                                                     |
| ------------------------------------------------------ | -------------- | --------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Pedro Lima: Git/Admin, Integração, Modelo 2, Indicador | Claude         | estrutura do código, testes, este documento                                                   | Rodei os testes no meu computador a cada entrega; revisei o código gerado e pedi para retirar comentários e as partes que pertenciam a outros integrantes; conferi os erros encontrados pelo indicador antes de reportar ao grupo. |
| Gabriel Tavares: Dados e carregamento                  |                |                                                                                               |                                                                                                                                                                                                                                    |
| Matheus Traiba: Busca e menu                           |                |                                                                                               |                                                                                                                                                                                                                                    |
| Miguel Moreira: Respostas e erros                      |                |                                                                                               |                                                                                                                                                                                                                                    |
| Lucas Carvalho: Revisão e indicadores                  | Codex (OpenAI) | Revisão da base e das referências, README, função de fonte e aviso, medição de tempo e testes | Comparação com fontes oficiais registrada em `docs/revisao_base.md`; execução local das perguntas, da suíte de testes e do indicador.                                                                                              |

---

_Última atualização: 17/11/2026._
