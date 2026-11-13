# Roteiro do vídeo: respostas e erros (Miguel) — alvo ~1min30

**Preparação:** terminal limpo na raiz do repo; fonte grande; `python src/sistema.py` (ou `python src/demo_miguel.py` se o menu ainda não estiver integrado). Ensaiar uma vez antes de gravar.

| Tempo | Tela | Fala (sugestão) |
|---|---|---|
| 0:00 | Menu aberto | "Eu sou o Miguel e vou mostrar como o assistente responde e como ele trata os erros." |
| 0:10 | Digitar `3` (Serviços) e escolher a pergunta da **Farmácia Popular** | "Escolhendo o tema Serviços, o sistema lista as perguntas e eu abro a da Farmácia Popular." |
| 0:25 | Mostrar o Modelo 1 na tela (rolar devagar) | "Este é o Modelo 1, direto e técnico: pergunta, procedimento em passos, observações importantes, e no final a fonte oficial, a data de verificação e o aviso de que o assistente não substitui o canal oficial." |
| 0:50 | Voltar ao menu e apertar **Enter vazio** | "Primeiro erro: entrada vazia. O programa explica o que digitar e não quebra." |
| 1:00 | Digitar `futebol` | "Segundo: tema inexistente. Ele avisa e lista os temas disponíveis." |
| 1:10 | Digitar `carteira`, depois escolher a opção `2` | "Terceiro: ambiguidade. 'Carteira' serve para Documentação e para Serviços, então ele pergunta qual eu quero em vez de adivinhar." |
| 1:25 | Resposta aparece | "Nos três casos o programa continua funcionando. Obrigado!" |

**Checklist antes de gravar**
- [ ] Os 3 erros foram testados ao vivo uma vez
- [ ] A fonte e o aviso aparecem no final da resposta
- [ ] Nenhum dado pessoal visível no terminal
