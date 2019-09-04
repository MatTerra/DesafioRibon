# Desafio processo seletivo Ribon

Esse projeto consiste em uma API REST para armazenar dados de um jogo e conceder troféus baseado nos pontos obtidos pelo usuário. O desafio é o seguinte:

Você deve criar um de sistema de troféus para um jogo. Pode usar o framework de desenvolvimento que preferir e não é necessário ter uma interface bonita. Gaste seu tempo com a arquitetura do código e dos dados.
Vou descrever um sistema base simples que captam os registros e ela vai ter uma estrutura rigida, que não está disponível a melhorias e mudanças. É permitido a criação de novas tabelas e campos na tabela de usuário, mas não é permitido alterar a estrutura das tabelas com registros transacionais. Assuma que as tabelas de registros transacionais podem ter dezenas de milhões de registros então faça sua estrutura resolvendo possiveis problemas de performance. A principal parte da avaliação é como você vai construir o sistema de troféus em cima desse sistema de coleta de registros que já existe. Para a parte da lógica dos troféus você pode usar qualquer ferramenta que preferir, como um banco não relacional ou um framework de sua preferência.
Sistema base de coleta de registro
```
user: id
collected_coin: id, user_id, value
monster: id, name
killed_monster: id, user_id, monster_id
deaths: id, user_id, timestamp
```
As tabelas collected_coin, killed_monster e deaths são tabelas transacionais, isto é, cada vez que um usuário coleta uma moeda por exemplo, é criado um registro nessa tabela com o valor user_id=1 e value=10 que é igual ao valor da moeda, essa tabela não guarda a soma ou o valor atual das moedas do usuário.

Vão existir três categorias de troféus, número de moedas coletadas, número de monstros que você matou, número de vezes que você morreu.
Cada categoria vão ter 5 níveis
Para moedas os níveis vão ser:

-> 1 moeda

-> 100 moedas

-> 1.000 moedas

-> 10.000 moedas

-> 100.000 moedas

Para número de vezes que você morreu os níveis vão ser:

-> 1 morte

-> 10 mortes

-> 25 mortes

-> 50 mortes

-> 100 mortes

Para o número de monstros que você matou, vai seguir uma contagem para cada monstro na tabela de monstros, por exemplo: turtle e bowser

-> 1 turtle

-> 100 turtles

-> 1.000 turtles

-> 10.000 turtles

-> 100.000 turtles

e

-> 1 bowser

-> 100 bowsers

-> 1.000 bowsers

-> 10.000 bowsers

-> 100.000 bowsers

O que o sistema de trofeus deve fazer ?
- Quando um registro for feito em qualquer uma das tabelas transacionais e a soma for suficiente para o usuário receber um troféu o sistema deve criar um registro dando para o usuário aquele troféu

## Primeiros Passos

Aqui colocamos instruções para configurarmos um ambiente local para desenvolvimento e testes. Veja as notas de deploy para instruções de como fazer o deploy do sistema para produção.

### Pré requisitos

Dependências necessárias e como instalá-las

```
Dê exemplos
```

### Instalando

Uma série de exemplos passo a passo que ensinam a configurar um ambiente de desenvolvimento.

Diga o que será o passo

```
Dê o exemplo
```

E repita

```
Até acabar
```

Termine com um exemplo de um teste rápido do sistema

## Rodando os testes

Explique como rodar os testes automatizados para este sistema

### Quebre em teste de ponta a ponta

Explique o que é testado e porque

```
Dê um exemplo
```

### E testes de estilo de código

Explique o que é testado e porque

```
Dê um exemplo
```

## Deploy

Adicione notas para deploy para produção

## Ferramentas de build

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contribuindo

Por favor leia [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) para detalhes do nosso código de conduta e do processo de submissão de PR's para nós.

## Versionamento

Usamos [SemVer](http://semver.org/) para versionamento. Para versões disponíveis, veja as [tags nesse repositório](https://github.com/your/project/tags). 

## Autores

* **Billie Thompson** - *Trabalho Inicial* - [PurpleBooth](https://github.com/PurpleBooth)
* **Mateus Berardo** - *Tradução para português* - [MatTerra](https://github.com/MatTerra)
Veja também a lista de [contribuidores](https://github.com/your/project/contributors) que participaram nesse projeto.

## Licença

Esse projeto está licenciado sob uma licença do MIT - veja o arquivo [LICENSE.md](LICENSE.md) para detalhes

## Agradecimentos

* Menção a todos que contribuíram para o repo
* Inspirações
* etc
