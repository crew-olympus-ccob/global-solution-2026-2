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
│   └── base_conhecimento.json
│
├── src/
│   ├── carregador.py
│   ├── busca.py
│   ├── fonte_aviso.py
│   └── navegacao.py
│
├── tests/
│   └── perguntas_teste.json
│
├── docs/
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
 
## Execução

O menu principal `src/sistema.py` ainda está em desenvolvimento. Quando estiver integrado, o comando planejado será:
 
```bash
python src/sistema.py
```
 
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
