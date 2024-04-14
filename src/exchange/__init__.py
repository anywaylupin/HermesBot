import ccxt
from keys import API_KEY, SECRET_KEY

# Create a connection to the Binance exchange
exchange = ccxt.binance(
    {
        "apiKey": API_KEY,
        "secret": SECRET_KEY,
    }
)

# Set sandbox mode for testing (if applicable)
exchange.set_sandbox_mode(True)
