from .BotInstance import BotInstance
from .commands import command_set
from .messages import handle_message
from telegram.ext import filters


def create_bot(name: str, bot_token: str, poll_interval_seconds: int):
    """
    Create and configure a bot instance.

    Args:
        name: The name of the bot.
        bot_token: The token required to authenticate the bot.
        poll_interval_seconds: The interval, in seconds, at which the bot should poll for updates.

    Returns:
        BotInstance: The configured bot instance.
    """
    bot = BotInstance(name, bot_token, poll_interval_seconds)

    for command in command_set:
        bot.add_command(command)

    bot.add_handler(filters.TEXT, handle_message)

    return bot
