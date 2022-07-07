from pprint import pprint
from requests import get
from json import loads
from os import getenv

def get_ticker_data(symbol: str) -> dict:
    api_key = getenv("ALPHA_KEY", "")
    response = get(f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={symbol}.sao&apikey={api_key}")
    return loads(response.content)