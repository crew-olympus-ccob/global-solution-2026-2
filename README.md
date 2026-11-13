# FIAP - Faculdade de Informática e Administração Paulista

<br>

# Nome do projeto/atividade

## Nome do grupo

## 👨‍🎓 Integrantes: 
- <a href="Link do perfil no LinkedIn ou GitHub">Nome do integrante 1</a>
- <a href="Link do perfil no LinkedIn ou GitHub">Nome do integrante 2</a>
- <a href="Link do perfil no LinkedIn ou GitHub">Nome do integrante 3</a> 
- <a href="Link do perfil no LinkedIn ou GitHub">Nome do integrante 4</a> 
- <a href="Link do perfil no LinkedIn ou GitHub">Nome do integrante 5</a>

## 👩‍🏫 Professores:

### Tutor(a)
- <a href="Link do perfil no LinkedIn">Nome do Tutor</a>
  
### Coordenador(a)
- <a href="https://www.linkedin.com/in/andregodoichiovato/">André Godoi Chiovato</a>

## 📜 Descrição

*Descreva aqui seu projeto em detalhes de forma estruturada e organizada*

## 📁 Estrutura de pastas

* **`data/`**: `base_conhecimento.json`: os registros de orientação (um por assunto), cada um com referência oficial e data de verificação.
* **`src/`**: código-fonte em Python (só biblioteca padrão):
  * `main.py`: programa de terminal (menu, as duas formas de busca, troca de modelo de resposta);
  * `carregador.py`: leitura segura do JSON com tratamento de arquivo ausente ou corrompido;
  * `base.py`: validação dos campos de cada registro (usa o `carregador.py`);
  * `busca.py`: busca por palavra-chave (com correção de digitação) e por menu tema → assunto;
  * `navegacao.py`: navegação entre assuntos relacionados do mesmo tema;
  * `saida.py`: Modelo 1 (direto) e Modelo 2 (educativo e detalhado);
  * `indicador.py`: cálculo automático da taxa de acerto (%).
* **`tests/`**: testes automatizados (`unittest`), perguntas do indicador (`perguntas_teste.json`) e base fixa de testes (`fixtures/`).
* **`docs/`**: documentação, `uso_ia.md`, `guia_registros.md`, `resultado_indicador.md`.
* **`README.md`**: este arquivo.

## 📎 Links e Observações

### 🔗 Links do Projeto

*Substitua ou duplique a estrutura abaixo para cada link relevante do projeto:*

* **[Nome do Link (ex: Vídeo de Entrega no YouTube)]**(http://url-aqui) - Breve descrição.

### 🧠 Decisões Técnicas

**Só a biblioteca padrão do Python.** Não há nada para instalar, o que facilita rodar em qualquer máquina do laboratório.

**Formato da base (`data/base_conhecimento.json`).** Uma lista de registros:

| Campo | Obrigatório | Uso |
|---|---|---|
| `id` | sim | número inteiro único |
| `tema` | sim | agrupa os assuntos no menu |
| `pergunta_chave` | sim | título do assunto e principal fonte da busca |
| `conteudo` | sim | a orientação, em frases curtas |
| `referencia` | sim | link ou documento oficial |
| `data_verificacao` | sim | `AAAA-MM-DD`, dia em que a fonte foi conferida |
| `palavras_chave` | não | como as pessoas falam ("ctps", "nada consta"); melhora muito a busca |
| `passos` | não | passo a passo explícito para o Modelo 2 |
| `alerta` | não | o que evitar, golpes comuns |

**Leitura e validação.** O `carregador.py` lê o arquivo tratando arquivo ausente ou corrompido. O `base.py` confere cada registro (campos obrigatórios, `id` inteiro e sem repetição, data válida). Se algo estiver errado, o programa para com uma mensagem clara, em vez de seguir funcionando com a base vazia.

**Busca por palavra-chave (`busca.py`).**
- O texto é normalizado: sem acento, minúsculas, sem pontuação, sem palavras que não indicam assunto ("como", "quero", "meu").
- As palavras são reduzidas ao radical removendo terminações, para que "comprei", "compra" e "compras" se encontrem, sem confundir "compra" com "comprovante".
- Palavras desconhecidas de 5 letras ou mais são corrigidas pela mais parecida da base (`difflib`, semelhança mínima 0,85): "identidae" vira "identidade".
- Pontuação de cada registro: palavra-chave inteira encontrada vale 2 por palavra dela; palavra presente na `pergunta_chave` ou numa palavra-chave de uma palavra só vale 2; palavra que só aparece no `conteudo` vale 1.
- Um registro só pode responder se a pergunta bater com a `pergunta_chave` ou as `palavras_chave` dele. Palavras que só aparecem no texto do conteúdo desempatam, mas sozinhas não bastam. Sem essa regra, "atualizar cadastro no CRAS" respondia com o registro do CPF.
- Uma palavra-chave composta ("multa eleitoral") só conta quando aparece inteira, para "multa de trânsito" não cair no título de eleitor.
- Abaixo de 2 pontos, a resposta é "não encontrei". Se dois assuntos empatam no topo, o programa pergunta qual a pessoa quer.

**Busca por menu.** Tema e depois assunto, escolhidos por número. Qualquer entrada que não seja um número da lista é recusada com aviso, inclusive casos como `-1`, `1.5` e `²`.

**Modelo 2 (Educativo e Detalhado, `saida.py`).** A resposta é montada em seções a partir do registro, e seção sem conteúdo não aparece:
- **Em resumo:** a 1ª frase do `conteudo`.
- **Passo a passo:** os `passos` do registro. Sem eles, as demais frases do conteúdo viram a lista **Como fazer**.
- **Atenção:** o `alerta` e as frases que começam com "Desconfie", "Cuidado", "Atenção", "Nunca", "Evite" ou "Não".
- **Fonte:** referência e data de verificação, com aviso se a informação tiver mais de 1 ano. Links nunca são quebrados, para continuarem funcionando ao copiar.
- **Veja também:** os outros assuntos do mesmo tema (`navegacao.py`).
- **Aviso** de que o assistente não substitui orientação jurídica, médica ou o órgão oficial.

O Modelo 1 (Direto) ainda está em aberto: a função existe com uma versão mínima, para o responsável substituir mantendo a mesma assinatura.

**Indicador (`indicador.py`).** Taxa de acerto = acertos / perguntas avaliadas × 100, sobre `tests/perguntas_teste.json`. O critério é rigoroso de propósito:
- acerto: o programa devolve um único registro e ele é o esperado, ou não devolve nada quando o esperado é `null`;
- empate no primeiro lugar conta como erro, porque a pessoa não recebeu uma resposta direta;
- pergunta sobre um registro que ainda não existe fica fora da conta, a não ser que o programa responda com outro registro: aí é falso positivo e conta como erro.

**Entradas do teclado.** Toda leitura passa por uma função que trata Enter vazio, Ctrl+C, Ctrl+D e textos com mais de 200 caracteres sem derrubar o programa. Os testes em `tests/test_integracao.py` rodam o programa de verdade com uma bateria de entradas estranhas.

### 📢 Observações Gerais

*Indique obrigatoriamente no campo abaixo a decisão da equipe quanto à participação na competição:*

* **Participação na Competição:** [ ] Sim, aceitamos participar / [ ] Não vamos participar.
* *Outras observações gerais (opcional):* Escreva aqui...

## 🔧 Como executar o código

**Pré-requisito:** Python 3.8 ou mais recente. Não há bibliotecas para instalar.

```bash
git clone https://github.com/crew-olympus-ccob/global-solution-2026-2.git
cd global-solution-2026-2

# programa interativo
python src/main.py

# atalhos (sem menu)
python src/main.py --buscar "perdi meu cpf"
python src/main.py --id 2 --modelo 1

# testes automatizados (integração + entradas estranhas)
python -m unittest discover -s tests -v

# indicador: taxa de acerto
python src/indicador.py
python src/indicador.py --salvar docs/resultado_indicador.md
```

No Windows, use `py` no lugar de `python` se necessário.

---

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/fiap-tutoria/FIAP-PORTFOLIO-AI">TEMPLATE - FIAP PORTFÓLIO AI</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">FIAP</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>
