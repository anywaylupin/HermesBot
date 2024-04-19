import logging
from telegram import Message, Update

# Initialize instance
instance = logging.getLogger(__name__)
instance.setLevel(logging.INFO)
formatter = logging.Formatter("[%(levelname)s]-%(asctime)s: %(message)s")

# Set up console handler
ch = logging.StreamHandler()
ch.setFormatter(formatter)
instance.addHandler(ch)


def info(msg: str):
    """
    Logs an info-level message.

    Args:
        msg: The message to be logged.
    """
    instance.info(msg)


def warn(msg: str):
    """
    Logs a warning message.

    Args:
        msg: The message to be logged.
    """
    instance.warning(msg)


def error(msg: str):
    """
    Logs an error message.

    Args:
        msg: The message to be logged.
    """
    instance.error(msg)


async def reply_text(update: Update, msg: str):
    """
    Replies to a Telegram message and logs the reply as an info-level message.

    Args:
        update: The Telegram update.
        msg: The reply message text.
    """
    message = update.message
    if isinstance(message, Message):
        await message.reply_text(msg)
        info(msg)
    else:
        error_msg = "Expected Message type for update, received different type."
        error(error_msg)
        raise TypeError(error_msg)


async def reply_warn(update: Update, msg: str):
    """
    Logs a warning message, then replies to the Telegram update with the same message.

    Args:
        update: The Telegram update.
        msg: The message to be logged and replied with.
    """
    warn(msg)
    await reply_text(update, msg)


async def reply_error(update: Update, msg: str):
    """
    Logs an error message, then replies to the Telegram update with the same message.

    Args:
        update: The Telegram update.
        msg: The message to be logged and replied with.
    """
    error(msg)
    await reply_text(update, msg)
