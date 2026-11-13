# Como encaixar a parte do Miguel no repositório

Copie as pastas para a raiz do repo (mesma estrutura):

| Arquivo | Destino | Dia |
|---|---|---|
| `data/servicos.json` | entra em `data/base_conhecimento.json` (Lucas junta os 3 blocos, ids 11-15) | 1 |
| `src/busca_tema.py` | `src/` | 2 |
| `src/respostas.py` (Modelo 1) | `src/` | 3 |
| `src/erros.py` | `src/` | 4 |
| `tests/test_miguel.py` | `tests/` | 4 |
| `docs/readme_testes_e_conclusoes.md` | colar no `README.md` | 5 |
| `docs/roteiro_video_miguel.md` | só para o vídeo | 6 |
| `entrega/links.txt` | arquivo .TXT final (colocar o link do YouTube) | 6 |

## Como o `src/sistema.py` (Matheus) deve chamar

```python
from busca_tema import buscar_por_tema, listar_temas
from erros import ErroDeConsulta, AmbiguidadeError, escolher_opcao
from respostas import formatar_modelo_1

try:
    tema, registros = buscar_por_tema(base, entrada)
except AmbiguidadeError as erro:
    print(erro.mensagem)
    i = escolher_opcao(erro.opcoes)          # None = a pessoa cancelou
    ...
except ErroDeConsulta as erro:               # vazia ou tema inexistente
    print(erro.mensagem)
```

- `base` é a lista de dicionários que a função de leitura do Gabriel devolve.
- Para a busca **por pergunta** (Matheus), as mesmas exceções servem: levante `EntradaVaziaError()` quando a entrada for vazia e `AmbiguidadeError(entrada, opcoes)` quando mais de um registro empatar.
- Modelo 1 e Modelo 2 (Pedro) usam a mesma assinatura: `formatar_modelo_1(registro, rodape=funcao_do_lucas)`. Se o Lucas entregar a função de fonte e aviso, é só passá-la em `rodape`.
- Se o time mudar o texto do `tema` no JSON (ex.: "Documentação e Identificação Civil"), a busca continua funcionando: ela casa pelo início do nome.
