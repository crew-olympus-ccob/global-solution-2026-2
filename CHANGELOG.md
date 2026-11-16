# Changelog

Todas as mudanças relevantes do projeto ficam registradas aqui, da mais recente para a mais antiga.

## 16/11/2026

### Adicionado
- **Matheus Traiba**: `src/sistema.py` com o menu interativo em loop (`while True`): busca por pergunta com tempo de consulta e outros resultados, busca por tema, troca entre Modelo 1 e Modelo 2, navegação entre assuntos relacionados e saída segura em entradas inválidas ou fim da entrada. Usa a busca por tema (`src/busca_tema.py`) e o Modelo 1 (`src/respostas.py`) assim que estiverem no repositório.
- **Matheus Traiba**: 6 perguntas de teste em `tests/perguntas_teste.json` (ids 7, 8, 9, 10, 11 e 14), completando 12 perguntas.
- **Matheus Traiba**: `docs/roteiro_video.md` com o roteiro e a ordem de gravação do vídeo.

### Alterado
- **Matheus Traiba**: README com a estrutura completa do repositório, o uso do menu e os comandos de teste.

### Alterado
- **Pedro Lima**: `src/saida.py` com o Modelo 2 reconhecendo conteúdo em linhas (passos `1)` e itens `- `), como nos registros de Serviços, e aceitando a função de rodapé no parâmetro `rodape`, no mesmo formato do Modelo 1.
- **Pedro Lima**: `tests/test_unidades.py` integrado à função `formatar_fonte_aviso()` e ao Modelo 1 (`formatar_modelo_1()`); `docs/resultado_indicador.md` atualizado com a base de 15 registros.
- **Pedro Lima**: `tests/test_miguel.py` lendo os registros de Serviços de `data/base_conhecimento.json` e comparando a data e o link com o próprio registro, em vez dos valores fixos do antigo `data/servicos.json`.
- **Pedro Lima**: integração da busca por tema, do Modelo 1 e dos cenários de erro do Miguel em uma branch nova a partir da main, sem apagar arquivos dos colegas (PR #9); testes de integração do menu (`src/sistema.py`) passando com entradas estranhas.

## 14/11/2026

### Adicionado
- **Miguel Moreira e Lucas Carvalho**: reunião dos cinco registros de Serviços com os demais, totalizando 15 registros.
- **Lucas Carvalho**: revisão das orientações e referências em `docs/revisao_base.md` e função de fonte e aviso em `src/fonte_aviso.py`.
- **Lucas Carvalho**: `src/tempo_consulta.py` para medir consultas e executar as perguntas de teste disponíveis.

### Alterado
- **Lucas Carvalho**: README com o formato da base, estado do menu e uso da medição de tempo.

## 13/11/2026

### Adicionado
- **Matheus Traiba**: `data/base_conhecimento.json` com 5 registros do tema Direitos do Consumidor (ids 6 a 10): direito de arrependimento em compras online, garantia legal de produtos duráveis e não duráveis, cobrança indevida, cancelamento de serviços de telecomunicações e registro de reclamações no Consumidor.gov.br.
- **Matheus Traiba**: Protótipo inicial do algoritmo de busca léxica em Python (`src/busca.py`) com normalização de texto (remoção de acentos e pontuação), filtragem de stopwords e pontuação de relevância por correspondência parcial de palavras-chave.
- **Matheus Traiba**: Definição da arquitetura do projeto, escolha dos temas cidadãos e planejamento da divisão de tarefas (Sprint de 6 dias) para a equipe.

### Adicionado
- **Pedro Lima**: `src/saida.py` com o Modelo 2 (Educativo e Detalhado), que organiza a resposta em resumo, passo a passo ou como fazer, atenção e veja também, e recebe a fonte e o aviso prontos.
- **Pedro Lima**: `src/indicador.py` com o cálculo automático da taxa de acerto (%) das duas formas de busca sobre as perguntas de teste.
- **Pedro Lima**: `tests/test_unidades.py` e `tests/test_integracao.py` com os testes de integração da leitura do JSON, das duas buscas, dos dois modelos de resposta e do menu, incluindo entradas estranhas; as partes ainda não entregues ficam marcadas como aguardando.
- **Pedro Lima**: `tests/perguntas_extras.json` com 51 perguntas para o indicador e `tests/fixtures/base_teste.json` com a base fixa dos testes.
- **Pedro Lima**: `docs/uso_ia.md` com a explicação de como ferramentas de IA apoiaram a estruturação de prompts e testes.
- **Pedro Lima**: `docs/resultado_indicador.md` com o relatório do indicador.
- **Pedro Lima**: `.gitignore` do repositório.

## 12/11/2026

- **Gabriel Tavares**: `data/base_conhecimento.json` com 5 registros do tema Documentação (ids 1 a 5): Carteira de Identidade, CPF, título de eleitor, Carteira de Trabalho Digital e certidão de antecedentes criminais.
- **Gabriel Tavares**: `src/carregador.py` com a função `carregar_base()`, que lê o JSON com segurança e trata arquivo ausente ou corrompido sem encerrar o programa.
- **Gabriel Tavares**: `src/navegacao.py` com `buscar_relacionados()` e `escolher_relacionado()`, para navegar entre assuntos do mesmo tema.
- **Gabriel Tavares**: `tests/perguntas_teste.json` com 6 perguntas de teste e o `id_esperado` de cada uma.
- **Gabriel Tavares**: `README.md` com as seções do problema e de como executar.
- **Gabriel Tavares**: `CHANGELOG.md` com o registro das entregas.