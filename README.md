# Desafio Inoa

## Introdução
Este projeto consiste de duas aplicações: `register`, que cuida da autenticação, e `tunnel_monitor`, que é a aplicação principal.

O usuário, depois de registrado, poderá criar túneis, cujos ativos terão os valores monitorados com a periodicidade selecionada.
Quando o ativo de determinado túnel atingir algum dos limites (inferior ou superior), usuário será notificado por e-mail e o túnel será desativado.

## Limitações, melhorias e observações
- Devido a limitações da API utilizada, períodos menores do que 1 dia não funcionarão adequadamente. Para corrigir, será necessário utilizar outra API, que permita obter cotações em tempo real. Uma possibilidade livre de custos, mas não ideal, é utilizar o pacote [yfinance](https://github.com/ranaroussi/yfinance), que obtém dados do Yahoo Finance.

- Não foram escritos testes unitários.

- O scheduler idealmente seria executado em um serviço separado, a ser definido em `docker-compose.yml`, e não no mesmo da aplicação.

## Configuração e execução
Este projeto requer uma chave de acesso à API da [Alpha Vantage](https://www.alphavantage.co/), que deve estar na variável de ambiente `ALPHA_KEY`.

Para o envio de emails, adicione as informções necessárias às variáveis de ambiente, conforme `.env.example`

Para montar o projeto:
```
docker-compose build
```

Para executar o projeto:
```
docker-compose up
```

Para criar um superusuário, conecte-se ao container `inoa_web` e entre o comando:
```
python3 manage.py createsuperuser
```

Para forçar a cotação de todos os túneis ativos configurados com um determinado intervalo, conecte-se ao container e utilize o comando:
```
python3 manage.py log_quotes --interval INTERVALO
```
A aplicação poderá ser acessada em localhost:8000.