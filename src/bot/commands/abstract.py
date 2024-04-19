from abc import ABC, abstractmethod
from libs import logger
from telegram import Message, Update
from telegram.ext import ContextTypes


class AbstractCommand(ABC):
    def __init__(self, command: str, default_text=""):
        self.command = command
        self.default_text = default_text

    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            if not isinstance(update.message, Message):
                raise TypeError("Expected message type for update, got something else")

            if not isinstance(update.message.text, str):
                raise TypeError("Expected text type for message, got something else")

            await self.on_execute(update, update.message.text)
        except Exception as e:
            await logger.reply_error(
                update,
                f"Sorry, an error occurred while processing your request.\n{str(e)}",
            )

    @abstractmethod
    async def on_execute(self, update: Update, text=""):
        """
        Executes the command.

        Args:
            update: The incoming update.
            text: The text message from user's input.
        """
        pass

    async def reply_text(self, update: Update, msg: str):
        logger.info(f"Executing command /{self.command}...")
        await logger.reply_text(update, msg)

    async def reply_error(self, update: Update, msg: str):
        await logger.reply_error(update, msg)
