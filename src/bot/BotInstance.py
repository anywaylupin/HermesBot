from bot.commands.abstract import AbstractCommand
from bot.messages import handle_error
from helpers import logger
from telegram.ext import Application, CommandHandler, MessageHandler, filters


class BotInstance:
    """
    A class responsible for creating and managing the bot application.
    """

    def __init__(self, name: str, bot_token: str, poll_interval_seconds=5):
        """
        Initializes the BotInstance.

        Args:
            name: The name of the bot.
            bot_token: The token required to authenticate the bot.
            poll_interval_seconds: The interval, in seconds, at which the bot should poll for updates.
        """
        self.name = name
        self.bot_token = bot_token
        self.poll_interval_seconds = poll_interval_seconds
        self.app = Application.builder().token(self.bot_token).build()
        self.app.add_error_handler(MessageHandler(filters.TEXT, handle_error))

    def start_polling(self):
        """
        Starts polling for updates from the bot application.
        """
        logger.info("Bot is polling...")
        self.app.run_polling(poll_interval=self.poll_interval_seconds)

    def add_command(self, instance: AbstractCommand):
        """
        Adds a command handler to the bot application.

        Args:
            instance: An instance of the command to be added.

        Returns:
            CommandHandler: The added command handler.
        """
        command = instance.command
        callback = instance.execute
        handler = CommandHandler(command, callback)
        self.app.add_handler(handler)

    def add_handler(self, filters: filters.BaseFilter | None, callback):
        handler = MessageHandler(filters, callback)
        self.app.add_handler(handler)
