<!-- Trecho do README.md (Dia 5 - Miguel). Colar na seção "Resultados dos testes e conclusões".
     Os campos marcados com PREENCHER dependem do Pedro (taxa de acerto) e do Lucas (tempo de consulta). -->

## 🧪 Resultados dos testes e conclusões

### Testes automatizados (tratamento de erros, busca por tema e Modelo 1)

```bash
python -m unittest tests/test_miguel.py -v
```

Resultado da última execução: **21 testes, 0 falhas**. Eles cobrem a estrutura do JSON de Serviços (5 registros, campos padronizados, referência com link e data válida), a busca por tema (número, nome, palavra relacionada, acentos e erro de digitação), o Modelo 1 de resposta e os três cenários de erro.

### Cenários de erro

Nenhum deles interrompe o programa: a pessoa recebe uma mensagem clara e volta ao menu.

| Cenário | Entrada de teste | Comportamento |
|---|---|---|
| Entrada vazia | Enter, espaços | Pede que a pessoa escreva uma pergunta ou escolha um tema e dá exemplos |
| Tema inexistente | `futebol`, `99` | Informa que não achou o tema e lista os temas disponíveis (com sugestão quando há algo parecido) |
| Ambiguidade | `carteira`, `cadastro` | Mostra as opções que combinam (ex.: Documentação e Serviços) e pede que a pessoa digite o número da desejada |

Quando a pessoa erra três vezes seguidas na escolha de uma opção, ou cancela com Enter, o programa volta ao menu.

### Indicadores

| Indicador | Resultado |
|---|---|
| Perguntas de teste | PREENCHER (mínimo 12) |
| Taxa de acerto | PREENCHER (acertos ÷ total, em %) |
| Tempo médio de consulta | PREENCHER (segundos, medido com `time`) |

### Conclusões

- A base de 15 registros em JSON é suficiente para o protótipo responder as perguntas dos três temas, e o padrão de campos (`id`, `tema`, `pergunta_chave`, `conteudo`, `referencia`, `data_verificacao`) permitiu que cada integrante escrevesse sua parte sem conflito.
- A busca por tema tolera acentos, caixa alta e pequenos erros de digitação, o que reduz respostas "não encontrado" por detalhes de escrita.
- Tratar a ambiguidade em vez de escolher um tema "no chute" evita dar uma resposta errada com aparência de certeza, o que importa em assuntos como saúde e direitos.
- **Limitações:** as palavras relacionadas a cada tema são uma lista mantida à mão (`SINONIMOS` em `src/busca_tema.py`); a base é pequena; e as regras mudam com o tempo (por exemplo, o Cartão SUS passou a se basear no CPF e a lista da Farmácia Popular foi ampliada). Por isso cada registro guarda a fonte e a `data_verificacao`.
- **Próximos passos:** ampliar a base, buscar por similaridade de texto no lugar de listas manuais e criar uma rotina que avise quando um registro passar de um prazo sem nova verificação.
