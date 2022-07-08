from decimal import Decimal
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
        price = Decimal(0)

    return price

def get_last_quote(tunnel_id: int) -> Decimal:
    try:
        price = PriceLog.objects.filter(tunnel=tunnel_id).latest("time")
        return price.price
    except PriceLog.DoesNotExist:
        return None

def log_quotes(interval: int) -> None:
    tunnels = Tunnel.objects.filter(active=True, interval=interval)

    price_buffer = {}
    for tunnel in tunnels:
        ticker = tunnel.ticker

        # Saving current price in a buffer to increase performance
        # for repeated tickers and reduce number of api calls.
        if ticker not in price_buffer:
            price_buffer[ticker] = get_quote(tunnel.ticker)

        log = PriceLog(tunnel=tunnel, price=price_buffer[ticker])
        log.save()