from . import abstract
from helpers import logger
from telegram import Update

COMMAND = "start"
DESCRIPTION = "To start watching Binance graphs that match the smart money concept"


class StartCommand(abstract.AbstractCommand):
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
            await self.reply_text(
                update, "Started watching Binance graphs for smart money concept."
            )
        except Exception as e:
            await logger.reply_error(
                update,
                f"Failed to start watching Binance graphs. Error: {str(e)}",
            )
