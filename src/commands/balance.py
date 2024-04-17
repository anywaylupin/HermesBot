from . import abstract
from exchange import exchange
from telegram import Update

COMMAND = "balance"
REPLY_TEXT = (
    "Please select a cryptocurrency symbol from the list or manually type it in:"
)


class BalanceCommand(abstract.AbstractCommand):
    """
    A command to display the user's current balance.
    """

    def __init__(self):
        super().__init__(COMMAND, REPLY_TEXT)

    def extract_symbol(self, message_text: str):
        if message_text.startswith(f"/{self.command}"):
            return message_text.split(f"/{self.command}")[1].strip()
        else:
            return message_text.strip()

    def fetch_balance(self, symbol: str):
        balance = exchange.fetch_balance().get(symbol)
        return balance

    def fetch_currencies(self):
        balance_info = exchange.fetch_balance()
        balances = balance_info.get("balances", [])
        symbols = [balance["asset"] for balance in balances]

        return {symbol: None for symbol in symbols}

    async def on_execute(self, update: Update):
        symbol = self.extract_symbol(update.message.text)
        print(exchange.fetch_balance())
        if symbol:
            balance = self.fetch_balance(symbol)
            if balance is not None:
                await self.reply_balance(update, symbol, balance)
            else:
                await self.reply_error(update, symbol)
        else:
            await self.reply_symbol_required(update)

    async def reply_balance(self, update: Update, symbol: str, balance: dict):
        formatted_balance = f"Free: {balance['free']}\nUsed: {balance['used']}\nTotal: {balance['total']}"
        await update.message.reply_text(
            f"Your balance for {symbol} is:\n{formatted_balance}"
        )

    async def reply_error(self, update: Update, symbol: str):
        await update.message.reply_text(
            f"Sorry, could not retrieve balance for {symbol}. Please try again."
        )

    async def reply_symbol_required(self, update: Update):
        await update.message.reply_text("Please specify a cryptocurrency symbol.")
