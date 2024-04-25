from . import AbstractCommand
from ccxt.base.types import OrderSide
from libs import exchange, logger
from time import sleep
from telegram import Update
from typing import TypedDict

COMMAND = "bottom_fishing"


class BottomFishingOptions(TypedDict):
    symbol: str
    timeframe: str
    limit: int
    delay: int
    trade_size: float
    stop: bool


class BottomFishingCommand(AbstractCommand):
    def __init__(self):
        """
        Initializes the BottomFishingCommand.
        """
        super().__init__(COMMAND)
        self.__started = False
        self.__options: BottomFishingOptions = {
            "symbol": "BTC/USDT",
            "timeframe": "1m",
            "limit": 5,
            "delay": 60,
            "trade_size": 100.0,  # Default trade size
            "stop": True,
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
            self.__options.update(options)

            if self.__options["stop"]:
                await self.reply_text(
                    update,
                    "Stopped watching Binance graphs for bottom fishing strategy.",
                )
            else:
                await self.reply_text(
                    update,
                    "Started watching Binance graphs for bottom fishing strategy.",
                )
                self.__options["stop"] = False

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
        options["stop"] = False
        for pair in option_pairs:
            if "=" in pair:
                key, value = pair.split("=")
                options[key.lower()] = value
            elif pair == "stop":
                options["stop"] = True

        return options

    async def __tick(self, update: Update):
        symbol = self.__options["symbol"]
        limit = self.__options["limit"]
        timeframe = self.__options["timeframe"]

        balance = exchange.fetch_balance()
        balance_total = balance["total"]
        total_btc = int(balance_total["BTC"])  # type: ignore
        total_usdt = int(balance_total["USDT"])  # type: ignore

        data_set = exchange.fetch_ohlcv(symbol, timeframe, None, limit)

        average_price = sum(price["close"] for price in data_set) / limit
        last_price = data_set[-1]["close"]
        side: OrderSide = "sell" if last_price > average_price else "buy"
        trade_size = self.__options["trade_size"]
        amount = trade_size / last_price

        try:
            exchange.create_market_order(symbol, side, amount)
            message = "\n".join(
                [
                    f"Average Price: {average_price}",
                    f"Last Price: {last_price}",
                    f"Order Side: {side} {amount} BTC",
                    f"Balance: BTC {total_btc}, USDT {total_usdt}",
                    f"Total USD: {total_btc - 1 * last_price + total_usdt}",
                ]
            )
            await self.reply_text(update, message)
        except Exception as e:
            logger.error(str(e))
            await self.reply_text(update, str(e))

    async def __start_tick(self, update: Update):
        while not self.__options["stop"]:
            await self.__tick(update)
            sleep(self.__options["delay"])
