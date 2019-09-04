# Desafio processo seletivo Ribon

Esse projeto consiste em uma API para armazenar dados de um jogo e conceder troféus baseado nos pontos obtidos pelo usuário. O desafio é o seguinte:

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

O projeto foi desenvolvido para rodar como uma GCloud Function em um runtime python. Para fazer o deploy utilizamos o Google Cloud SDK ou criamos um arquivo zip para fazer upload no Google Cloud Console.
Além da função, é necessário configurar um banco de dados de tempo real no Firebase para armazenar os dados e troféus.

### Pré requisitos

Para instalar o Google Cloud SDK siga os passos referentes ao seu sistema operacional. A SDK depende de uma instalação do Python 2.7

#### Arch Linux/Manjaro

Os passos estão disponíveis em [Setting Up Google Cloud SDK For GCP On Arch/Manjaro Linux](https://dev.to/nabbisen/setting-up-google-cloud-sdk-of-gcp-on-archmanjaro-linux-19mk)

Primeiro vamos criar uma conta na plataforma de nuvem do Google no seguinte link [Teste Gratuito da Nuvem do Google](https://console.cloud.google.com/freetrial/)

Em seguida vamos prosseguir para instalação do pacote google-cloud-sdk, que está disponível na AUR. (Podemos também seguir a instalação manual descrita no [guia de início rápido do Google](https://cloud.google.com/sdk/docs/quickstart-linux?hl=pt-br))

Podemos utilizar um gerenciador de pacotes da AUR como o [yay](https://aur.archlinux.org/packages/yay/) ou [yaourt](https://archlinux.fr/yaourt-en)(**DESCONTINUADO!!!**) para instalar o SDK, ou realizar a instalação manual.

Caso queira utilizar o `yay`, o comando será o seguinte:
```bash
yay -Sy google-cloud-sdk
```

Para a instalação manual do pacote da AUR, siga os passos abaixo:

Primeiro vamos clonar o repositório da AUR
```bash
git clone https://aur.archlinux.org/google-cloud-sdk.git
```

Em seguida vamos fazer o build do pacote
```bash
cd google-cloud-sdk/ && makepkg -si
```

Depois da instalação, vamos remover nossa cópia local do repositório
```bash
cd .. && rm -rf google-cloud-sdk/
```

Pronto, agora temos o sdk instalado e podemos partir para a inicialização dele que está na parte de instalação deste README

#### Ubuntu/Debian >= Wheezy

Os passos estão disponíveis em [Guia de início rápido para Debian e Ubuntu](https://cloud.google.com/sdk/docs/quickstart-debian-ubuntu?hl=pt-br)

Para instalar no Ubuntu pode ser necessário instalar o pacote lsb_release para recuperar o nome correto da versão Canonical. Em seguida rode os comandos abaixo

```bash
# Create environment variable for correct distribution
export CLOUD_SDK_REPO="cloud-sdk-$(lsb_release -c -s)"

# Add the Cloud SDK distribution URI as a package source
echo "deb http://packages.cloud.google.com/apt $CLOUD_SDK_REPO main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list

# Import the Google Cloud Platform public key
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -

# Update the package list and install the Cloud SDK
sudo apt-get update && sudo apt-get install google-cloud-sdk
```

Pronto, agora temos o sdk instalado e podemos partir para a inicialização dele que está na parte de instalação deste README


### Instalando

Antes de inicializar o SDK na máquina local, vamos [criar um projeto do Google Cloud](https://console.cloud.google.com/cloud-resource-manager?hl=pt-br) que irá armazenar nossa função. Caso você já tenha projetos, siga para os passos seguintes.


Para configurar o sdk, basta rodar o seguinte comando e seguir as instruções dele. Ele irá pedir que você faça login e selecione seu projeto.

```bash
gcloud init
```

Pronto, a instalação está concluída e os comando gcloud e gsutil estão prontos para serem usados.

A documentação do gcloud pode ser encontrada [aqui](https://cloud.google.com/sdk/gcloud/reference/) e a documentação do gsutil, [aqui](https://cloud.google.com/storage/docs/gsutil/).

Vamos agora fazer o primeiro deploy da função para nosso projeto utilizando o seguinte comando

```bash
gcloud beta functions deploy trophyAPI --runtime python37 --trigger-http
```

Aguarde a conclusão do deploy, que poderá levar até 2 minutos. Ao finalizar, ele te fornecerá o link da sua função, você pode testá-la pelo seu [console do Google Cloud](https://console.cloud.google.com) ou utilizando o comando cURL da seguinte forma:
```bash
curl -X POST LINK_DA_FUNCAO -H "Content-Type:application/json"  -d 'JSON_TESTE'
```

Sua função ainda não funcionará, pois não inicializamos o banco de dados dela e nem fornecemos as credenciais necessárias para acesso ao banco. Na próxima sessão abordaremos como configurar o banco de dados.


### Firebase

Além do Cloud Functions, precisamos de um banco de dados firebase. Primeiro, crie um projeto do [Firebase](https://console.firebase.google.com/).

Depois, na barra de opções, selecione a opção `database` (https://console.firebase.google.com/project/*PROJECT_NAME*/database) e crie um banco de dados de tempo real. Seu banco terá um link como *https://*PROJECT_NAME*/firebaseio.com*. Na aba *rules* do banco, copie e cole o seguinte:

```json
{
  "rules": {
    ".read": false,
    ".write": false,
    "users": {
      ".indexOn": ["id"]
    },
    "monsters":{
      ".indexOn":["name"]
    }
  }
}
```

Para utilizar a função, é necessário criar entradas no banco de dados de usuários e de monstros(para utilizar o comando `killed_monster`).

Depois de inicializar o banco, precisamos fornecer à função as credenciais de acesso, para isso vamos acessar as configurações do nosso projeto do Firebase e vamos clicar na aba *Contas de Serviço* e gerar uma nova chave privada. Com isso, baixaremos um arquivo json com nossa chave. Vamos mover o arquivo para o mesmo diretório do nosso arquivo `main.py`. **ATENÇÃO: ** *Essa chave não deve ser compartilhada com ninguém e nem disponibilizada em repositórios públicos ou aplicações cliente*. Depois de baixar, atualize o arquivo main.py com o nome do arquivo json e refaça o deploy.
```python
    ...
    # Initialize DB connection
    cred = credentials.Certificate('seu-arquivo.json')
    try:
    ...
```

Pronto, agora sua função tem acesso ao seu banco de dados e poderá ser testada. Lembre que para o funcionamento correto é necessário criar ao menos um usuário e para o comando `killed_monster`, ao menos um monstro.

## Autores

* **Mateus Berardo** - *Autor* - [MatTerra](https://github.com/MatTerra)
Veja também a lista de [contribuidores](https://github.com/MatTerra/DesafioRibon/contributors) que participaram nesse projeto.

## Licença

Esse projeto está licenciado sob uma licença do MIT - veja o arquivo [LICENSE.md](LICENSE.md) para detalhes

## Agradecimentos

* A big thanks to **Billie Thompson** - *README template* - [PurpleBooth](https://github.com/PurpleBooth)