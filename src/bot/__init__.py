from commands.abstract import AbstractCommand
from telegram import Update
from telegram.constants import ChatType
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)


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

        self.app.add_handler(MessageHandler(filters.TEXT, self.handle_message))

    def add_handler(self, instance: AbstractCommand):
        """
        Adds a command handler to the bot application.

        Args:
            instance (AbstractCommand): An instance of the command to be added.

        Returns:
            CommandHandler: The added command handler.
        """
        command = instance.command
        callback = instance.execute
        handler = CommandHandler(command, callback)
        self.app.add_handler(handler)

    def handle_error(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(f"Update {update} caused an error: {context.error}")

    def handle_message(self, text: str):
        processed: str = text.lower()

        if "hello" in processed:
            return "Hey there"
        if "how are you" in processed:
            return "I am good!"
        if "i love python" in processed:
            return "Really!"

        return "I do not understand what you wrote..."

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        message_type: ChatType = update.message.chat.type
        message_text: str = update.message.text

        print(f'User {update.message.chat.id} in {message_type}: "{message_text}"')

        if message_type == ChatType.GROUP:
            if self.name in message_text:
                new_text: str = message_text.replace(self.name, "").strip()
                response: str = self.handle_response(new_text)
            else:
                return
        else:
            response: str = self.handle_response(message_text)

        print(f"Bot: {response}")

        await update.message.reply_text(response)

    def start_polling(self):
        """
        Starts polling for updates from the bot application.
        """
        print("Starting bot polling...")
        self.app.run_polling(poll_interval=self.poll_interval_seconds)
