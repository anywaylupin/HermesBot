from . import abstract
from exchange import exchange
from telegram import Update

COMMAND = "balance"
REPLY_TEXT = "Your current balance is: "


class BalanceCommand(abstract.AbstractCommand):
    """
    A command to display the user's current balance.
    """

    def __init__(self):
        super().__init__(COMMAND, REPLY_TEXT)

    async def _execute(self, update: Update):
        """
        Executes the BalanceCommand by fetching and replying with the user's balance.
        """
        balance = await exchange.fetch_balance()
        await update.message.reply_text(f"{self.reply_text} {balance}")
