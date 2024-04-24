from . import AbstractCommand
from ccxt.base.types import OrderSide
from libs import exchange, logger
from time import sleep
from telegram import Update
from typing import TypedDict, Union

COMMAND = "bottom_fishing"


class BottomFishingOptions(TypedDict):
    symbol: str
    timeframe: str
    limit: int
    delay: int
    trade_size: float


class BottomFishingCommand(AbstractCommand):
    def __init__(self):
        """
        Initializes the BottomFishingCommand.
        """
        super().__init__(COMMAND)
        self.__started = False
        self.__running = False
        self.__options: BottomFishingOptions = {
            "symbol": "BTC/USDT",
            "timeframe": "1m",
            "limit": 5,
            "delay": 60,
            "trade_size": 100.0,  # Default trade size
        }

    async def on_execute(self, update: Update, text: str):
        """
        Executes the BottomFishingCommand.

        Args:
            update: The incoming update.
            text: The text command.
        """
        try:
            options = self.__parse_options(text)
            if "stop" in options:
                await self.reply_text(
                    update,
                    "Stopped watching Binance graphs for bottom fishing strategy.",
                )
                self.__running = False
            else:
                self.__options.update(options)
                await self.reply_text(
                    update,
                    "Started watching Binance graphs for bottom fishing strategy.",
                )
                self.__running = True

                if not self.__started:
                    self.__started = True
                    await self.__start_tick(update)

        except Exception as e:
            await logger.reply_error(
                update, f"Command failed to execute. Error: {str(e)}"
            )

    def __parse_options(self, text: str) -> BottomFishingOptions:
        option_pairs = text.split(f"/{self.command}")[1].strip().split()
        options = self.__options
        for pair in option_pairs:
            key, value = pair.split("=")
            options[key.lower()] = value
        return options

    async def __tick(self, update: Update):
        symbol = self.__options["symbol"]
        limit = self.__options["limit"]
        timeframe = self.__options["timeframe"]

        balance = exchange.fetch_balance(symbol)
        data_set = exchange.fetch_ohlcv(symbol, timeframe, None, limit)

        average_price = sum(price["close"] for price in data_set) / limit
        last_price = data_set[-1]["close"]
        side: OrderSide = "sell" if last_price > average_price else "buy"
        trade_size = self.__options["trade_size"]
        amount = trade_size / last_price
        order = None

        if side == "sell" and balance is not None:
            balance_free = balance["free"]

            if isinstance(balance_free, (int, float)):
                if balance_free > 0 and balance_free < amount:
                    order = exchange.create_market_order(symbol, side, balance_free)
                else:
                    message = f"Balance is insufficient for placing a sell order. Current balance: {balance}"
        else:
            order = exchange.create_market_order(symbol, side, amount)

            if side == "sell":
                profit = amount * (last_price - average_price)
            else:
                profit = None
            message = (
                f"The market trend suggests it's time to {side.upper()}!\n"
                f"Trade Size - {trade_size}\nAmount - {amount}\nProfit - {profit}\n"
                f"Current Balance - {balance}"
            )

        await self.reply_text(update, message)
        return order

    async def __start_tick(self, update: Update):
        while self.__running:
            await self.__tick(update)
            sleep(self.__options["delay"])
