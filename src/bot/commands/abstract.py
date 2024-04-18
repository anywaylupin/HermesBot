from abc import ABC, abstractmethod
from helpers import logger
from telegram import Update
from telegram.ext import ContextTypes


class AbstractCommand(ABC):
    def __init__(self, command: str, reply_text=""):
        self.command = command
        self.reply_text = reply_text

    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            logger.info(f"Executing command /{self.command}")
            await self.on_execute(update)
        except Exception as e:
            await logger.update_error(
                update,
                f"Sorry, an error occurred while processing your request.\n{str(e)}",
            )

    @abstractmethod
    async def on_execute(self, update: Update):
        pass
