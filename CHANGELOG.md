# Changelog

Todas as mudanças relevantes do projeto ficam registradas aqui, da mais recente para a mais antiga.

## 12/11/2026 (2)

### Adicionado
- **Pedro Lima**: `src/base.py`: validação dos registros por cima do `carregador.py` (campos obrigatórios, id inteiro único, data `AAAA-MM-DD`); campos opcionais `palavras_chave`, `passos`, `alerta`, `autor`.
- **Pedro Lima**: `src/busca.py`: busca por palavra-chave (acentos, plural/conjugação, erro de digitação, desempate) e por menu tema → assunto.
- **Pedro Lima**: `src/saida.py`: **Modelo 2 (Educativo e Detalhado)**: em resumo, como fazer/passo a passo, atenção, fonte com data, veja também e aviso de limitação. Modelo 1 provisório (em aberto).
- **Pedro Lima**: `src/main.py`: programa de terminal integrando as duas buscas, a troca de modelo e a navegação de relacionados.
- **Pedro Lima**: `src/indicador.py`: taxa de acerto automática, com casos ambíguos e falsos positivos contados como erro.
- **Pedro Lima**: `tests/test_unidades.py` e `tests/test_integracao.py` (61 testes, incluindo entradas estranhas) e `tests/fixtures/base_teste.json`.
- **Pedro Lima**: `docs/uso_ia.md`, `docs/guia_registros.md`, `docs/resultado_indicador.md`; seções de estrutura e execução do `README.md`.
- **Pedro Lima**: `palavras_chave` nos registros 1 a 5 (sem alterar o conteúdo). **Gabriel, revise.**
- **Pedro Lima**: 51 perguntas novas em `tests/perguntas_teste.json`, no formato do Gabriel.

### Corrigido
- `src/navegacao.py`: digitar `²` derrubava o programa (`"²".isdigit()` é True, mas `int("²")` falha); Ctrl+D na escolha também derrubava.

## 12/11/2026

### Adicionado
- **Gabriel Tavares**: `data/base_conhecimento.json` com 5 registros do tema Documentação (ids 1 a 5): Carteira de Identidade, CPF, título de eleitor, Carteira de Trabalho Digital e certidão de antecedentes criminais.
- **Gabriel Tavares**: `src/carregador.py` com a função `carregar_base()`, que lê o JSON com segurança e trata arquivo ausente ou corrompido sem encerrar o programa.
- **Gabriel Tavares**: `src/navegacao.py` com `buscar_relacionados()` e `escolher_relacionado()`, para navegar entre assuntos do mesmo tema.
- **Gabriel Tavares**: `tests/perguntas_teste.json` com 6 perguntas de teste e o `id_esperado` de cada uma.
- **Gabriel Tavares**: `README.md` com as seções do problema e de como executar.
- **Gabriel Tavares**: `CHANGELOG.md` com o registro das entregas.