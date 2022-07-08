# Desafio Inoa

Este projeto requer uma chave de acesso à API da [Alpha Vantage](https://www.alphavantage.co/), que deve estar na variável de ambiente `ALPHA_KEY`.

Para o envio de emails, adicione as informções necessárias às variáveis de ambiente, conforme `.env.example`

Para criar um superusuário, conecte-se ao container `inoa_web` e entre o comando:
```python3 manage.py createsuperuser```

Para forçar a cotação de todos os túneis ativos configurados com um determinado intervalo, conecte-se ao container e utilize o comando:
```python3 manage.py log_quotes --interval INTERVALO```

Para executar o projeto:
```docker-compose up```