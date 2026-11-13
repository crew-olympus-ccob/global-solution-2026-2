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
 
A base de conhecimento tem 15 registros, divididos em três temas:
 
| Tema | Assuntos |
|---|---|
| Documentação | Carteira de Identidade Nacional (CIN), CPF, título de eleitor, Carteira de Trabalho Digital e certidão de antecedentes criminais |
| Direitos do Consumidor | Direito de arrependimento, garantia legal, cobrança indevida, cancelamento de serviços e reclamação no consumidor.gov.br |
| Saúde Pública e Serviços Comunitários | Cartão do SUS, Farmácia Popular, vacinação, CadÚnico e isenção de taxas em concursos |
 
---
 
# Estrutura do Projeto
 
```text
global-solution-2026-2/
│
├── data/
│   └── base_conhecimento.json     base de conhecimento (registros)
│
├── src/
│   ├── main.py                    programa principal (menu no terminal)
│   ├── carregador.py              leitura segura do JSON
│   ├── base.py                    validação dos registros
│   ├── busca.py                   busca por palavra-chave e por tema
│   ├── navegacao.py               assuntos relacionados
│   ├── saida.py                   Modelo 1 e Modelo 2 de resposta
│   └── indicador.py               taxa de acerto
│
├── tests/
│   ├── perguntas_teste.json       perguntas do indicador
│   ├── test_unidades.py
│   ├── test_integracao.py
│   └── fixtures/base_teste.json   base fixa usada pelos testes
│
├── docs/
│   ├── uso_ia.md
│   ├── guia_registros.md
│   └── resultado_indicador.md
│
├── CHANGELOG.md
└── README.md
```
 
---
 
# Como Executar
 
Requisitos: Python 3.8 ou superior. Não há dependências externas.
 
## Clone o projeto
 
```bash
git clone https://github.com/crew-olympus-ccob/global-solution-2026-2
```
 
## Entre na pasta
 
```bash
cd global-solution-2026-2
```
 
## Execute o sistema
 
```bash
python src/main.py
```
 
Siga o menu no terminal para buscar por pergunta ou escolher um tema.
 
Atalhos sem menu:
 
```bash
python src/main.py --buscar "perdi meu cpf"
python src/main.py --id 2 --modelo 1
```
 
## Testes e indicador
 
```bash
python -m unittest discover -s tests
python src/indicador.py
```
 
O segundo comando mostra a taxa de acerto das buscas sobre `tests/perguntas_teste.json`. Para salvar o relatório: `python src/indicador.py --salvar docs/resultado_indicador.md`.
 
---
 
# Decisões Técnicas

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
 
---
 
# Aviso
 
As respostas são informativas e não oficiais. Em caso de dúvida, confirme sempre no canal oficial indicado na fonte de cada resposta.
