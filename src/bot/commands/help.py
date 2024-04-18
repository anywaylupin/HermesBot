from . import abstract
from . import balance
from . import sandbox
from telegram import Update

COMMAND = "help"
DESCRIPTION = "Display the available commands and their descriptions"
REPLY_TEXT = (
    "Available commands:\n"
    f"/{COMMAND} - {DESCRIPTION}\n"
    f"/{balance.COMMAND} - {balance.DESCRIPTION}\n"
    f"/{sandbox.COMMAND} - {sandbox.DESCRIPTION}\n"
)


class HelpCommand(abstract.AbstractCommand):
    """
    A command to display the available commands and their descriptions.
    """

    def __init__(self):
        """
        Initializes the HelpCommand.
        """
        super().__init__(COMMAND, REPLY_TEXT)

    async def on_execute(self, update: Update):
        """
        Executes the HelpCommand by replying with the available commands and their descriptions.
        """
        await update.message.reply_text(self.reply_text)
