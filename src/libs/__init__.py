import ccxt
from keys import API_KEY, SECRET_KEY

exchange_config = {
    "apiKey": API_KEY,
    "secret": SECRET_KEY,
}

exchange = ccxt.binance(exchange_config)
