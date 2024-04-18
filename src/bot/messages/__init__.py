from helpers import logger
from telegram import Update
from telegram.ext import ContextTypes


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.warn("Command is not recognized")
    await update.message.reply_text("I do not understand what you wrote...")


def handle_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Update {update} caused an error: {context.error}")
