import ccxt
import time
from config import TRADE_INTERVAL_SECONDS, TRADE_SYMBOL
from config.keys import API_KEY, SECRET_KEY
from helpers.calculate import calculate_average_and_last_price, calculate_trade_quantity, print_trade_details
from helpers.logging import log_info, log_error

exchange = ccxt.binance({
    'apiKey': API_KEY,
    'secret': SECRET_KEY,
})

exchange.set_sandbox_mode(True)

def fetch_recent_prices():
    log_info(f"Fetching recent prices for {TRADE_SYMBOL} pair...")
    recent_prices = exchange.fetch_ohlcv(TRADE_SYMBOL, '1m', limit=TRADE_INTERVAL_SECONDS)
    log_info("Recent prices fetched successfully.")
    return recent_prices

def process_prices(recent_prices):
    log_info("Processing recent prices...")
    return calculate_average_and_last_price(recent_prices)

def determine_trade_direction(average_price, last_price):
    log_info("Determining trade direction...")
    return "sell" if last_price > average_price else "buy"

def execute_trade(direction, quantity):
    log_info("Executing trade...")
    return exchange.create_market_order(TRADE_SYMBOL, direction, quantity)

def print_trade_info(average_price, last_price, direction, quantity, order):
    log_info("Printing trade details...")
    print_trade_details(average_price, last_price, direction, quantity, order)
    log_info("Trade details printed successfully.")

def fetch_and_print_balance(btc_price):
    log_info("Fetching balance...")
    balance = exchange.fetch_balance()
    total_btc = balance['BTC']['total']
    total_usdt = (total_btc - 1) * btc_price + balance['USDT']['total']
    log_info(f"Balance: BTC {total_btc}, USDT: {balance['USDT']['total']}")
    log_info(f"Total USDT: {total_usdt}\n")
    return balance

def run_trading():
    while True:
        try:
            recent_prices = fetch_recent_prices()
            average_price, last_price = process_prices(recent_prices)
            direction = determine_trade_direction(average_price, last_price)
            quantity = calculate_trade_quantity(last_price)
            order = execute_trade(direction, quantity)
            print_trade_info(average_price, last_price, direction, quantity, order)
            btc_price = last_price
            fetch_and_print_balance(btc_price)
            log_info("Waiting for the next iteration...")
            time.sleep(TRADE_INTERVAL_SECONDS)

        except Exception as e:
            log_error(str(e))
