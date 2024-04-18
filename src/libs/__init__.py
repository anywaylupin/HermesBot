import ccxt
from keys import API_KEY, SECRET_KEY

# Create a connection to the Binance exchange
exchange = ccxt.binance(
    {
        "apiKey": API_KEY,
        "secret": SECRET_KEY,
    }
)
