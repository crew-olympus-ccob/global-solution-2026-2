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
│   └── base_conhecimento.json
│
├── src/
│   ├── sistema.py
│   ├── carregador.py
│   └── navegacao.py
│
├── tests/
│   └── perguntas_teste_1.json
│
├── docs/
│   └── uso_ia.md
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
python src/sistema.py
```
 
Siga o menu no terminal para buscar por pergunta ou escolher um tema.
 
---
 
# Aviso
 
As respostas são informativas e não oficiais. Em caso de dúvida, confirme sempre no canal oficial indicado na fonte de cada resposta.
