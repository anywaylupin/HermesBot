from bot import create_bot
from keys import BOT_TOKEN, BOT_USERNAME

if __name__ == "__main__":
    my_bot = create_bot(BOT_USERNAME, BOT_TOKEN, 5)
    my_bot.start_polling()
