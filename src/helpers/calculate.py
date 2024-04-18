import datetime


def calculate_average_and_last_price(prices):
    closes = [price[4] for price in prices]
    average_price = sum(closes) / len(closes)
    last_price = prices[-1][4]
    return average_price, last_price


def print_trade_details(average_price, last_price, direction, quantity, order):
    print(f"Average Price: {average_price}")
    print(f"Last Price: {last_price}")
    print(
        f"{datetime.datetime.now().isoformat()}: {direction} {quantity} BTC at {last_price}"
    )
    print(order)
