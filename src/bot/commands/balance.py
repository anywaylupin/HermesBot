from . import abstract
from ccxt.base.types import Balance
from libs import exchange
from telegram import Update

COMMAND = "balance"
DESCRIPTION = "Display the user's current balance for a specified cryptocurrency symbol"


class BalanceCommand(abstract.AbstractCommand):
    """
    A command to display the user's current balance for a specified cryptocurrency symbol.
    """

    def __init__(self):
        """
        Initializes the BalanceCommand.
        """
        super().__init__(COMMAND)
        self.currencies = None

    async def on_execute(self, update: Update, text: str):
        try:
            symbol = text.split(f"/{self.command}")[1].strip()

            if self.currencies is None:
                self.currencies = exchange.fetch_currencies()
                if not isinstance(self.currencies, list):
                    raise TypeError(
                        "Expected list type for currencies, got something else"
                    )
                self.currencies.sort()

            if symbol in self.currencies:
                balance = exchange.fetch_balance(symbol)
                await self.reply_text(
                    update,
                    f"Your balance for {symbol} is:\n{format_balance_message(balance)}",
                )
            else:
                await self.__reply_currencies(update, symbol)
        except Exception as e:
            await self.reply_error(
                update,
                f"Sorry, could not retrieve balance. Please try again. Error: {str(e)}",
            )

    async def __reply_currencies(self, update: Update, symbol: str):
        """
        Replies with a message listing available currencies if the specified symbol is invalid.

        Args:
            update: The incoming update.
            symbol: The invalid symbol provided by the user.
        """
        try:
            if self.currencies:
                reply = (
                    f"Sorry, could not retrieve balance for {symbol}."
                    if symbol
                    else "Please provide a symbol to retrieve the balance."
                )
                reply += "\nAvailable currencies in your account:\n"
                reply += " | ".join(f"{currency}" for currency in self.currencies)
            else:
                reply = "There are no available currencies in your account."

            await self.reply_text(update, reply)
        except Exception as e:
            raise ValueError(e)


def format_balance_message(balance: Balance | None):
    """
    Formats the balance message.

    Args:
        balance: The balance information.

    Returns:
        The formatted balance message.
    """
    return f"Free: {balance['free']}\nUsed: {balance['used']}\nTotal: {balance['total']}"  # type: ignore
