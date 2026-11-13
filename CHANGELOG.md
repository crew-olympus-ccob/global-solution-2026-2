# Changelog

Todas as mudanças relevantes do projeto ficam registradas aqui, da mais recente para a mais antiga.

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