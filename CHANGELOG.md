# Changelog

Todas as mudanças relevantes do projeto ficam registradas aqui, da mais recente para a mais antiga.

## 12/11/2026

### Adicionado
- **Gabriel Tavares**: `data/base_conhecimento.json` com 5 registros do tema Documentação (ids 1 a 5): Carteira de Identidade, CPF, título de eleitor, Carteira de Trabalho Digital e certidão de antecedentes criminais.
- **Gabriel Tavares**: `src/carregador.py` com a função `carregar_base()`, que lê o JSON com segurança e trata arquivo ausente ou corrompido sem encerrar o programa.
- **Gabriel Tavares**: `src/navegacao.py` com `buscar_relacionados()` e `escolher_relacionado()`, para navegar entre assuntos do mesmo tema.
- **Gabriel Tavares**: `tests/perguntas_teste.json` com 6 perguntas de teste e o `id_esperado` de cada uma.
- **Gabriel Tavares**: `README.md` com as seções do problema e de como executar.
- **Gabriel Tavares**: `CHANGELOG.md` com o registro das entregas.