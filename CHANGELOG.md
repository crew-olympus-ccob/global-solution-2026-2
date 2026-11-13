# Changelog

Todas as mudanças relevantes do projeto ficam registradas aqui, da mais recente para a mais antiga.

## 13/11/2026

### Adicionado
- **Matheus Traiba**: `data/base_conhecimento.json` com 5 registros do tema Direitos do Consumidor (ids 6 a 10): direito de arrependimento em compras online, garantia legal de produtos duráveis e não duráveis, cobrança indevida, cancelamento de serviços de telecomunicações e registro de reclamações no Consumidor.gov.br.
- **Matheus Traiba**: Protótipo inicial do algoritmo de busca léxica em Python (`src/busca.py`) com normalização de texto (remoção de acentos e pontuação), filtragem de stopwords e pontuação de relevância por correspondência parcial de palavras-chave.
- **Matheus Traiba**: Definição da arquitetura do projeto, escolha dos temas cidadãos e planejamento da divisão de tarefas (Sprint de 6 dias) para a equipe.

### Adicionado
- **Pedro Lima**: `src/main.py` com o programa de terminal, que integra as duas formas de busca (palavra-chave e menu por tema), a troca de modelo de resposta e a navegação entre assuntos relacionados.
- **Pedro Lima**: `src/saida.py` com o Modelo 2 (Educativo e Detalhado), que organiza a resposta em resumo, como fazer, atenção, fonte com data de verificação, veja também e aviso de limitação.
- **Pedro Lima**: `src/busca.py` com a busca por palavra-chave (ignora acentos, reconhece plural e conjugação, corrige erro de digitação e pergunta ao usuário em caso de empate) e a busca por menu de tema.
- **Pedro Lima**: `src/base.py` com a validação dos registros lidos pelo `carregador.py` (campos obrigatórios, id inteiro e único, data no formato `AAAA-MM-DD`).
- **Pedro Lima**: `src/indicador.py` com o cálculo automático da taxa de acerto (%) das buscas sobre as perguntas de teste.
- **Pedro Lima**: `tests/test_unidades.py`, `tests/test_integracao.py` e `tests/fixtures/base_teste.json` com 61 testes automatizados, incluindo entradas estranhas como Enter vazio, Ctrl+D e textos muito longos.
- **Pedro Lima**: 51 perguntas novas em `tests/perguntas_teste.json`.
- **Pedro Lima**: `docs/uso_ia.md` com a explicação de como ferramentas de IA apoiaram a estruturação de prompts e testes.
- **Pedro Lima**: `docs/guia_registros.md` com as instruções para a equipe escrever os registros e `docs/resultado_indicador.md` com o relatório do indicador.

### Alterado
- **Pedro Lima**: `data/base_conhecimento.json` com o campo `palavras_chave` nos registros 1 a 5, sem alterar o conteúdo.
- **Pedro Lima**: `README.md` com a seção "Decisões Técnicas", os comandos de testes e do indicador e a estrutura de pastas atualizada.

### Corrigido
- **Pedro Lima**: `src/navegacao.py` não encerra mais o programa ao digitar `²` ou apertar Ctrl+D na escolha de assunto relacionado.

## 12/11/2026

- **Gabriel Tavares**: `data/base_conhecimento.json` com 5 registros do tema Documentação (ids 1 a 5): Carteira de Identidade, CPF, título de eleitor, Carteira de Trabalho Digital e certidão de antecedentes criminais.
- **Gabriel Tavares**: `src/carregador.py` com a função `carregar_base()`, que lê o JSON com segurança e trata arquivo ausente ou corrompido sem encerrar o programa.
- **Gabriel Tavares**: `src/navegacao.py` com `buscar_relacionados()` e `escolher_relacionado()`, para navegar entre assuntos do mesmo tema.
- **Gabriel Tavares**: `tests/perguntas_teste.json` com 6 perguntas de teste e o `id_esperado` de cada uma.
- **Gabriel Tavares**: `README.md` com as seções do problema e de como executar.
- **Gabriel Tavares**: `CHANGELOG.md` com o registro das entregas.