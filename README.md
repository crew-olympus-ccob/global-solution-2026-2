# Crew Olympus: CitizenTech, assistente de orientação ao cidadão
 
Assistente em Python, executado no terminal, desenvolvido para a Global Solution 2026 da FIAP. Ele orienta o cidadão sobre documentação, direitos do consumidor e serviços de saúde e assistência, a partir de uma base de conhecimento em JSON.
 
## Equipe Crew Olympus
 
| Nome | RM |
|--------|--------|
| Gabriel Tavares Martins de Oliveira | RM573718 |
| Lucas Araujo de Carvalho | RM571060 |
| Matheus Henrique Pedrozo Traiba | RM571817 |
| Miguel Monteiro Moreira | RM572904 |
| Pedro Henrique de Lima Costa | RM573008 |
 
---
 
# Sobre o Projeto
 
## O problema
 
Muita gente não sabe por onde começar quando precisa emitir um documento, fazer valer um direito do consumidor ou acessar um serviço público. As informações existem, mas ficam espalhadas em vários sites e nem sempre estão em linguagem simples. O resultado é tempo perdido, idas desnecessárias a órgãos públicos e, em alguns casos, o risco de cair em sites falsos que cobram por serviços gratuitos.
 
## Público beneficiado
 
Cidadãos em geral, principalmente quem tem pouca familiaridade com serviços digitais do governo e precisa de um passo a passo direto, com a fonte oficial indicada.
 
## Temas abordados
 
A base reúne 15 registros em três temas. As orientações e referências devem ser revisadas antes da entrega:
 
| Tema | Assuntos |
|---|---|
| Documentação | Carteira de Identidade Nacional (CIN), CPF, título de eleitor, Carteira de Trabalho Digital e certidão de antecedentes criminais |
| Direitos do Consumidor | Direito de arrependimento, garantia legal, cobrança indevida, cancelamento de serviços e reclamação no consumidor.gov.br |
| Serviços | Cartão do SUS, Farmácia Popular, vacinação, CadÚnico e isenção de taxas em concursos |
 
---
 
# Estrutura do Projeto
 
```text
global-solution-2026-2/
│
├── data/
│   └── base_conhecimento.json     # base com 15 registros em 3 temas
│
├── src/
│   ├── sistema.py                 # menu principal em loop (ponto de entrada)
│   ├── carregador.py              # leitura segura do JSON
│   ├── busca.py                   # busca por pergunta livre
│   ├── busca_tema.py              # busca por tema ou palavra relacionada
│   ├── erros.py                   # erros e escolha em caso de ambiguidade
│   ├── navegacao.py               # assuntos relacionados
│   ├── respostas.py               # Modelo 1: Direto e Técnico
│   ├── saida.py                   # Modelo 2: Educativo e Detalhado
│   ├── fonte_aviso.py             # fonte, data de verificação e aviso
│   ├── tempo_consulta.py          # medição do tempo de consulta
│   └── indicador.py               # taxa de acerto das buscas
│
├── tests/
│   ├── perguntas_teste.json       # 12 perguntas de teste com o id esperado
│   ├── perguntas_extras.json      # casos adicionais do indicador
│   ├── fixtures/base_teste.json
│   ├── test_unidades.py
│   ├── test_integracao.py
│   └── test_miguel.py
│
├── docs/
│   ├── uso_ia.md
│   ├── revisao_base.md
│   └── resultado_indicador.md
│
├── CHANGELOG.md
└── README.md
```
 
---
 
# Como Executar
 
Requisitos informados pela equipe: Python 3.8 ou superior. Não há dependências externas. A execução e os testes desta revisão foram realizados com Python 3.13.5; as demais versões não foram verificadas nesta revisão.
 
## Clone o projeto
 
```bash
git clone https://github.com/crew-olympus-ccob/global-solution-2026-2
```
 
## Entre na pasta
 
```bash
cd global-solution-2026-2
```
 
## Execução

A partir da raiz do projeto:

```bash
python src/sistema.py
```

O menu principal oferece:

| Opção | O que faz |
|---|---|
| 1. Fazer uma pergunta | Busca por pergunta livre. Mostra a resposta mais provável, o tempo da consulta e outros resultados parecidos para escolher |
| 2. Buscar por tema | Lista os temas e, dentro do tema escolhido, os assuntos disponíveis |
| 3. Trocar formato da resposta | Alterna entre o Modelo 1 (Direto e Técnico) e o Modelo 2 (Educativo e Detalhado) |
| 0. Sair | Encerra o programa |

Depois de cada resposta, o menu oferece os assuntos relacionados do mesmo tema. Toda resposta termina com a fonte, a data de verificação e o aviso de não-oficialidade. Entradas vazias, letras no lugar de números, números fora da lista e o fim da entrada (Ctrl+D ou Ctrl+Z) são tratados sem encerrar o programa com erro.

Por exemplo, escolha **1**, digite `Como acessar a Carteira de Trabalho Digital?` e confira a resposta. Para navegar por categoria, escolha **2**, informe um tema e selecione um assunto. A opção **3** alterna o formato das respostas.

Para medir o tempo de busca das perguntas de teste e calcular a taxa de acerto:

```bash
python src/tempo_consulta.py
python src/indicador.py
```

A medição de tempo considera apenas a execução da busca; leitura de dados, digitação e exibição ficam fora do tempo.

Para rodar os testes automatizados:

```bash
python -m unittest discover -s tests
```

## Resultados e limitações

Na revisão de 17/11/2026, os **61 testes automatizados passaram**. O indicador avaliou **63 casos**, com **53 acertos (84,1%)**: 48 de 58 casos por pergunta (82,8%) e 5 de 5 por tema (100%). Para as perguntas, o cálculo considera somente o primeiro resultado retornado; nos casos que esperam ausência de resposta, retornar algum resultado conta como erro. Casos pendentes são excluídos da taxa.

Esses números descrevem apenas o conjunto de testes disponível. A busca usa correspondência de palavras e pode interpretar sinônimos de forma incorreta ou sugerir assuntos fora da intenção do usuário. Por exemplo, `cancelar compra` não retornou o assunto esperado nessa execução. O sistema mostra alternativas e permite navegar pelos temas; sempre confira a pergunta exibida e a fonte oficial antes de seguir a orientação.

O arquivo `docs/resultado_indicador.md` registra uma execução anterior, de 16/11/2026; para obter os resultados atuais, execute novamente `python src/indicador.py`. Para atualizar o relatório, use:

```bash
python src/indicador.py --salvar docs/resultado_indicador.md
```

O tempo mostrado pelo sistema se refere à busca por pergunta e varia conforme a máquina. A busca por tema não é cronometrada pelo menu. No script `tempo_consulta.py`, são executadas as 12 perguntas de `tests/perguntas_teste.json`.

## Estrutura da base

O arquivo `data/base_conhecimento.json` contém uma lista de objetos. Cada registro possui:

| Campo | Conteúdo |
|---|---|
| `id` | Identificador numérico do registro |
| `tema` | Categoria da orientação |
| `pergunta_chave` | Pergunta principal que identifica o assunto |
| `conteudo` | Orientação apresentada ao cidadão |
| `referencia` | Endereço da fonte consultada |
| `data_verificacao` | Data de verificação, no formato `AAAA-MM-DD` |

Por exemplo, um registro é representado assim:

```json
{
  "id": 1,
  "tema": "Documentação",
  "pergunta_chave": "Como emitir a Carteira de Identidade Nacional?",
  "conteudo": "Consulte as orientações do órgão de identificação do seu estado.",
  "referencia": "https://www.gov.br/identidade",
  "data_verificacao": "2026-11-12"
}
```

O exemplo ilustra o formato; consulte a base para a orientação completa. As referências podem reunir mais de um endereço, separados por ` | `.
 
---
 
# Aviso
 
As respostas são informativas e não oficiais. Em caso de dúvida, confirme sempre no canal oficial indicado na fonte de cada resposta.
