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

Para rodar os testes utilize:
```
docker build -t crawler_teste .
docker run -it crawler_teste python -m unittest
```

Você também pode rodar o crawler em um ambiente virtual, após criar o ambiente virtual utilize os comandos:
```
pip install -r requirements.txt
python main.py
```
Você precisa alterar a variável de ambiente REGION para buscar os dados da region desejada ou passar a região desejada como parâmetro.
```
python main.py <REGION>
python main.py Brazil
python main.py Argentina
python main.py New Zealand
```
Por padrão a region é Brazil e os arquivos são salvos no diretório que há o main.py, sendo assim no final 
2 arquivos são salvos na pasta sendo que arquivos tem o nome da region selecionada.

Para rodar os testes utilize:
```
python -m unittest
```


As vezes podem ocorrer erros causados pela conexão ou pelo login, então tente rodar novamente.
