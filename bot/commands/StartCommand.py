from . import AbstractCommand
from libs import exchange, logger, plotter
from telegram import Update

COMMAND = "start"


class StartCommand(AbstractCommand):
    """
    A command to start watching Binance graphs that match the smart money concept.
    """

    def __init__(self):
        """
        Initializes the StartCommand.
        """
        super().__init__(COMMAND)

    async def on_execute(self, update: Update, text: str):
        """
        Executes the StartCommand.

        Args:
            update: The incoming update.
        """
        try:
            data_set = exchange.fetch_ohlcv("BTC/USDT")

            await self.reply_text(
                update, "Started watching Binance graphs for smart money concept."
            )

            for data in data_set:
                await self.reply_text(
                    update,
                    f"Timestamp: {data["timestamp"]}\nO: {data['open']}\nH: {data['high']}\nL: {data['low']}\nC: {data['close']}\nV: {data['volume']}\n",
                )
        except Exception as e:
            await logger.reply_error(
                update,
                f"Failed to start watching Binance graphs. Error: {str(e)}",
            )
