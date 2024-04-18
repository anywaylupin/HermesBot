import logging
from telegram import Update

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
        msg (str): The message to be logged.
    """
    instance.info(msg)


def warn(msg: str):
    """
    Log a warning message.

    Parameters:
        msg (str): The message to be logged.
    """
    instance.warning(msg)


def error(msg: str):
    """
    Log an error message.

    Parameters:
        msg (str): The message to be logged.
    """
    instance.error(msg)


async def update_warn(update: Update, msg: str):
    """
    Log a warning message and reply to the user.

    Parameters:
        update (telegram.Update): The incoming update.
        msg (str): The message to be logged and replied.
    """
    warn(msg)
    await update.message.reply_text(msg)


async def update_error(update: Update, msg: str):
    """
    Log an error message and reply to the user.

    Parameters:
        update (telegram.Update): The incoming update.
        msg (str): The message to be logged and replied.
    """
    error(msg)
    await update.message.reply_text(msg)
