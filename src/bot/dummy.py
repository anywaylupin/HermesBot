from typing import Final
from telegram import Update
from telegram.constants import ChatType
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN: Final = '6925504632:AAHMC9E0D-uV8bgFisL9Yy9SeKZKSwnRd-4'
BOT_USERNAME: Final = '@SMCHermesBot'
POLL_INTERVAL_SECONDS: Final = 5

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello, this is Hermès talking')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello, this is Hermès helping. Please type something so I can respond')

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello, this is Hermès custom command.')
    
def handle_response(text: str) -> str:
    processed: str = text.lower()
    
    if 'hello' in processed:
        return 'Hey there'
    if 'how are you' in processed:
        return 'I am good!'
    if 'i love python' in processed:
        return 'Really!'
    
    return 'I do not understand what you wrote...'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: ChatType = update.message.chat.type
    message_text: str = update.message.text
    
    print(f'User {update.message.chat.id} in {message_type}: "{message_text}"')
    
    if message_type == ChatType.GROUP:
        if BOT_USERNAME in message_text:
            new_text: str = message_text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(message_text)
        
    print(f'Bot: {response}')
    
    await update.message.reply_text(response)
    
async def handle_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused an error: {context.error}')

def create_bot():
    print('Starting bot...')
    
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))
    
    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    # Errors
    app.add_error_handler(handle_error)
    
    # Polls
    print('Polling...')
    app.run_polling(poll_interval=POLL_INTERVAL_SECONDS)