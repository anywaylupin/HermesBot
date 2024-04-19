import logging
from telegram import Message, Update

# Initialize logger
instance = logging.getLogger(__name__)
instance.setLevel(logging.INFO)
formatter = logging.Formatter("[%(levelname)s]-%(asctime)s: %(message)s")

# Set up console handler
ch = logging.StreamHandler()
ch.setFormatter(formatter)
instance.addHandler(ch)


def info(msg: str):
    """
    Log an info-level message.

    Parameters:
        msg: The message to be logged.
    """
    instance.info(msg)


def warn(msg: str):
    """
    Log a warning message.

    Parameters:
        msg: The message to be logged.
    """
    instance.warning(msg)


def error(msg: str):
    """
    Log an error message.

    Parameters:
        msg: The message to be logged.
    """
    instance.error(msg)


async def reply_text(update: Update, msg: str):
    message = update.message
    if isinstance(message, Message):
        await message.reply_text(msg)
        info(msg)
    else:
        error_msg = "Expected Message type for update, got something else"
        error(error_msg)
        raise TypeError(error_msg)


async def reply_warn(update: Update, msg: str):
    """
    Log a warning message and reply to the user.

    Parameters:
        update: The incoming update.
        msg: The message to be logged and replied.
    """
    warn(msg)
    await reply_text(update, msg)


async def reply_error(update: Update, msg: str):
    error(msg)
    await reply_text(update, msg)
