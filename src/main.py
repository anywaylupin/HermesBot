from bot import BotInstance
from bot.commands import balance, help
from keys import BOT_TOKEN, BOT_USERNAME

if __name__ == "__main__":
    my_bot = BotInstance(BOT_USERNAME, BOT_TOKEN, 5)
    my_bot.add_handler(balance.BalanceCommand())
    my_bot.add_handler(help.HelpCommand())
    my_bot.start_polling()
