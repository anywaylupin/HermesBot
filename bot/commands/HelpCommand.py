from . import AbstractCommand
from telegram import Update

COMMAND = "help"
REPLY_TEXT = (
    "Available commands:\n"
    "/help - Display the available commands and their descriptions\n"
    "/balance - Display the user's current balance for a specified cryptocurrency symbol\n"
    "/sandbox - Toggle the exchange sandbox mode\n"
    "/start - To start watching Binance graphs that match the smart money concept\n"
)


class HelpCommand(AbstractCommand):
    """
    A command to display the available commands and their descriptions.
    """

    def __init__(self):
        """
        Initializes the HelpCommand.
        """
        super().__init__(COMMAND, REPLY_TEXT)

    async def on_execute(self, update: Update, text: str):
        await self.reply_text(update, self.default_text)
