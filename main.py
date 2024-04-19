from bot import create_bot
from keys import BOT_TOKEN, BOT_USERNAME


def main():
    chat_bot = create_bot(BOT_USERNAME, BOT_TOKEN, 5)
    chat_bot.start_polling()


if __name__ == "__main__":
    main()
