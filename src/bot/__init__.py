from bot.commands.abstract import AbstractCommand
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from . import commands


class BotInstance:
    """
    A class responsible for creating and managing the bot application.
    """

    def __init__(self, name: str, bot_token: str, poll_interval_seconds: int):
        """
        Initializes the BotCreator instance.

        Args:
            name (str): The name of the bot.
            bot_token (str): The token required to authenticate the bot.
            poll_interval_seconds (int): The interval, in seconds, at which the bot should poll for updates.
        """
        self.name = name
        self.bot_token = bot_token
        self.poll_interval_seconds = poll_interval_seconds
        self.app = Application.builder().token(self.bot_token).build()
        self.app.add_error_handler(MessageHandler(filters.TEXT, self.handle_error))

    def add_handler(self, instance: AbstractCommand):
        """
        Adds a command handler to the bot application.

        Args:
            command (AbstractCommand): An instance of the command to be added.

        Returns:
            CommandHandler: The added command handler.
        """
        command = instance.command
        callback = instance.execute
        handler = CommandHandler(command, callback)
        self.app.add_handler(handler)

    def handle_error(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(f"Update {update} caused an error: {context.error}")

    def start_polling(self):
        """
        Starts polling for updates from the bot application.
        """
        print("Starting bot polling...")
        self.app.run_polling(poll_interval=self.poll_interval_seconds)
