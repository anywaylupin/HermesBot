from abc import ABC, abstractmethod
from telegram import Update
from telegram.ext import ContextTypes


class AbstractCommand(ABC):
    def __init__(self, command: str, reply_text: str):
        self.command = command
        self.reply_text = reply_text

    async def execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            print(f"Executing command: {self.command}")
            await self.on_execute(update)
        except Exception as e:
            print(
                f"An error occurred while executing command '{self.command}': {str(e)}"
            )
            await update.message.reply_text(
                "Sorry, an error occurred while processing your request."
            )

    @abstractmethod
    async def on_execute(self, update: Update):
        pass
