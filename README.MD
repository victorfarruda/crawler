# Serviço Crawler Yahoo Finance

Este Serviço Recebe como paramêtro uma Region(Brazil, Argentina, etc.) e busca os dados de name, symbol e price(intraday)
da region selecionada no site: https://finance.yahoo.com/screener/new e cria dois arquivos, um csv e um json dos dados.

Para rodar o projeto basta rodar os comandos:
```
docker-compose build
docker-compose up

```
Você pode alterar a variável de ambiente REGION no docker-compose.yml e fazer a raspagem na region em que deseja.

No final 2 arquivos são salvos na pasta /src com o nome da region selecionada.


Você também pode rodar o crawler em um ambiente virtual, após criar o ambiente virtual utilize o comando:
```
pip install -r src/requirements.txt
python src/main.py
```
Você precisa alterar a variável de ambiente REGION para buscar os dados da region desejada. Por padrão a region é Brazil.
Por padrão os arquivos são salvos no diretório em que o comando é executado, sendo assim no final 2 arquivos são salvos na pasta em que o comando foi rodado tendo os arquivos o nome da region selecionada.

Para rodar os testes utilize:
```
python -m unittest
```


As vezes podem ocorrer erros causados pela conexão ou pelo login, então tente rodar novamente.
