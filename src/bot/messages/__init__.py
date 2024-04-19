from helpers import logger
from telegram import Update
from telegram.ext import CallbackContext


async def handle_message(update: Update, context: CallbackContext):
    """
    Handles messages when no command is recognized.

    Args:
        update: The incoming update.
        context: The context passed by the telegram.ext module.
    """
    msg = "Command is not recognized"
    await logger.reply_warn(update, msg)


async def handle_error(update: Update, context: CallbackContext):
    """
    Handles errors that occur during the bot's operation.

    Args:
        update: The incoming update.
        context: The context passed by the telegram.ext module.
    """
    logger.error(f"Update {update} caused an error: {context.error}")
