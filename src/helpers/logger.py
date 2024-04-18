import logging
from telegram import Update

instance = logging.getLogger(__name__)
instance.setLevel(logging.INFO)
formatter = logging.Formatter("[%(levelname)s]-%(asctime)s: %(message)s")

ch = logging.StreamHandler()
ch.setFormatter(formatter)
instance.addHandler(ch)


def info(msg: str):
    """
    Log an info-level message.
    """
    instance.info(msg)


def warn(msg: str):
    """
    Log a warning message.
    """
    instance.warning(msg)


def error(msg: str):
    """
    Log an error message.
    """
    instance.error(msg)


async def update_error(update: Update, msg: str):
    error(msg)
    await update.message.reply_text(msg)
