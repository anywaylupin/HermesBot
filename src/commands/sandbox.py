# Set sandbox mode for testing (if applicable)
exchange.set_sandbox_mode(True)

from . import abstract
from telegram import Update
from exchange import exchange

COMMAND = "sandbo"
REPLY_TEXT = (
    "Available commands:\n"
    "/help - Display this help message\n"
    "/balance - Display your current balance\n"
    "/open_orders - Display your open orders\n"
    "/trade_history - Display your trade history\n"
    "/buy <symbol> <quantity> - Place a buy order\n"
    "/sell <symbol> <quantity> - Place a sell order"
)


class HelpCommand(abstract.AbstractCommand):
    """
    A command to display the available commands and their descriptions.
    """

    def __init__(self):
        super().__init__(COMMAND, REPLY_TEXT)

    async def on_execute(self, update: Update):
        """
        Executes the HelpCommand by replying with the available commands and their descriptions.
        """
        await update.message.reply_text(self.reply_text)
