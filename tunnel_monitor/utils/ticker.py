from decimal import Decimal
from pprint import pprint
from requests import get
from json import loads
from os import getenv

from tunnel_monitor.models import Tunnel, PriceLog

api_key = getenv("ALPHA_KEY", "")

def get_ticker_data(symbol: str) -> dict:
    response = get(f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={symbol}.sao&apikey={api_key}")
    return loads(response.content)

def get_quote(symbol: str) -> Decimal:
    response = get(f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}.sao&apikey={api_key}")
    content = loads(response.content)

    if "05. price" in content["Global Quote"]:
        price = Decimal(content["Global Quote"]["05. price"])
    else:
        price = None

    return price

def log_quotes(interval: int) -> None:
    tunnels = Tunnel.objects.filter(active=True, interval=interval)

    for tunnel in tunnels:
        price = get_quote(tunnel.ticker)
        log = PriceLog(tunnel=tunnel, price=price)
        log.save()
    
        