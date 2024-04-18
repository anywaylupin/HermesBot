from . import abstract
from ccxt.base.types import Balance
from helpers import logger
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

    async def on_execute(self, update: Update):
        """
        Executes the BalanceCommand by fetching and replying with the user's balance.

        Args:
            update: The incoming update.
        """
        symbol = update.message.text.split(f"/{self.command}")[1].strip()
        try:
            if self.currencies is None:
                self.currencies = fetch_currencies()
                if isinstance(self.currencies, list):
                    self.currencies.sort()

            if symbol in self.currencies:
                balance = fetch_balance(symbol)
                await update.message.reply_text(
                    f"Your balance for {symbol} is:\n{format_balance_message(balance)}"
                )
            else:
                await self.__reply_currencies(update, symbol)

        except Exception as e:
            await logger.update_error(
                update,
                f"Sorry, could not retrieve balance. Please try again.\n{str(e)}",
            )

    async def __reply_currencies(self, update: Update, symbol: str):
        """
        Replies with a message listing available currencies if the specified symbol is invalid.

        Args:
            update: The incoming update.
            symbol: The invalid symbol provided by the user.
        """
        if self.currencies:
            reply = (
                (
                    f"Sorry, could not retrieve balance for {symbol}."
                    if symbol
                    else "Please provide symbol to retrieve balance."
                )
                + "\nAvailable currencies in your account:\n"
                + " | ".join(f"{currency}" for currency in self.currencies)
            )

        else:
            reply = "There are no available currencies in your account."

        await update.message.reply_text(reply)


def fetch_balance(symbol: str):
    """
    Fetches the balance for the specified cryptocurrency symbol.

    Args:
        symbol: The cryptocurrency symbol.

    Returns:
        The balance information.
    """
    balance = exchange.fetch_balance()
    return balance.get(symbol)


def fetch_currencies():
    """
    Fetches the list of available cryptocurrencies in the user's account.

    Returns:
        A list of available cryptocurrency symbols.
    """
    info = fetch_balance("info")
    balances = info.get("balances")
    return [balance["asset"] for balance in balances]


def format_balance_message(balance: Balance):
    """
    Formats the balance message.

    Args:
        balance: The balance information.

    Returns:
        The formatted balance message.
    """
    return (
        f"Free: {balance['free']}\nUsed: {balance['used']}\nTotal: {balance['total']}"
    )
