import logging
from telegram import Message, Update


class LoggerInstance:
    def __init__(self):
        """
        Initializes the LoggerInstance.
        """
        self.instance = logging.getLogger(__name__)
        self.instance.setLevel(logging.INFO)
        formatter = logging.Formatter("[%(levelname)s]-%(asctime)s: %(message)s")
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        self.instance.addHandler(ch)

    def info(self, msg: str):
        """
        Logs an info-level message.

        Args:
            msg: The message to be logged.
        """
        self.instance.info(msg)

    def warn(self, msg: str):
        """
        Logs a warning message.

        Args:
            msg: The message to be logged.
        """
        self.instance.warning(msg)

    def error(self, msg: str):
        """
        Logs an error message.

        Args:
            msg: The message to be logged.
        """
        self.instance.error(msg)

    async def reply_text(self, update: Update, msg: str):
        """
        Replies to a Telegram message and logs the reply as an info-level message.

        Args:
            update: The Telegram update.
            msg: The reply message text.
        """
        message = update.message
        if isinstance(message, Message):
            await message.reply_text(msg)
            self.info(msg)
        else:
            error_msg = "Expected Message type for update, received different type."
            self.error(error_msg)
            raise TypeError(error_msg)

    async def reply_warn(self, update: Update, msg: str):
        """
        Logs a warning message, then replies to the Telegram update with the same message.

        Args:
            update: The Telegram update.
            msg: The message to be logged and replied with.
        """
        self.warn(msg)
        await self.reply_text(update, msg)

    async def reply_error(self, update: Update, msg: str):
        """
        Logs an error message, then replies to the Telegram update with the same message.

        Args:
            update: The Telegram update.
            msg: The message to be logged and replied with.
        """
        self.error(msg)
        await self.reply_text(update, msg)
