from decimal import Decimal
from requests import get
from json import loads
from os import getenv
from django.core.mail import send_mail

from tunnel_monitor.models import Tunnel, PriceLog

api_key = getenv("ALPHA_KEY", "")

def get_ticker_data(symbol: str) -> dict:
    response = get(f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={symbol}.sao&apikey={api_key}")
    return loads(response.content)

def get_quote(symbol: str) -> Decimal:
    '''
    Returns the current price for a given symbol.
    '''
    response = get(f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}.sao&apikey={api_key}")
    content = loads(response.content)

    if "05. price" in content["Global Quote"]:
        price = Decimal(content["Global Quote"]["05. price"])
    else:
        price = Decimal(0)

    return price

def get_last_quote(tunnel_id: int) -> Decimal:
    '''
    Returns the last logged price for a given tunnel.
    '''
    try:
        price = PriceLog.objects.filter(tunnel=tunnel_id).latest("time")
        return price.price
    except PriceLog.DoesNotExist:
        return None

def log_quotes(interval: int) -> None:
    '''
    Logs the current price of every tunnel with the provided interval.

    If any of the bounds have been crossed, the user will be notified
    via email, and the tunnel will be marked as inactive.
    '''
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

        if price_buffer[ticker] >= tunnel.upper_bound:
            send_mail(
                subject=f"{ticker} has crossed the upper bound",
                message=f"{ticker} has crossed the upper bound ({tunnel.upper_bound})",
                from_email=None,
                recipient_list=[tunnel.auth_user.email],
                fail_silently=True
            )
            tunnel.active = False
            tunnel.save()
        if price_buffer[ticker] <= tunnel.lower_bound:
            send_mail(
                subject=f"{ticker} has crossed the lower bound",
                message=f"{ticker} has crossed the lower bound ({tunnel.lower_bound})",
                from_email=None,
                recipient_list=[tunnel.auth_user.email],
                fail_silently=True
            )
            tunnel.active = False
            tunnel.save()
        