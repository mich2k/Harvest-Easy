import requests
import text
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, ChatMemberHandler, CallbackQueryHandler, InvalidCallbackData
from os import getenv

TOKEN = getenv('TG_TOKEN')
url = getenv('URL')


async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text.welcome_message)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message is not None:
        id_user = update.effective_user.name

        if requests.get(url + f'checkUsername/{id_user}'):
            requests.get(url + f'setelegramSession/{id_user}')
            await update.message.reply_text(f'Sessione salvata, benvenuto: {id_user}')

        else:
            await update.message.reply_text(text.unregistered_user)


async def get_score(update: Update, context: ContextTypes.DEFAULT_TYPE):

    id_user = update.effective_user.name
    
    if requests.get(url + f'getSession/{id_user}').content.decode('UTF-8') == 'True':
        resp = requests.get(
            url + f'getScore/{id_user}').content.decode('UTF-8')
        await update.message.reply_text(resp)
    else:
        await update.message.reply_text(text.init_error_message)


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    # EFFETTUA GET PER RISOLVERE IL PROBLEMA INDICANDO CHI L'HA RISOLTO (report or solved)
    query = update.callback_query
    await query.answer()
    
    resp = query.data 

    
    await query.edit_message_text(text=f"Selected option: {resp}")
    await query.message.reply_text(query)



async def helper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text.help_text)



if __name__ == '__main__':

    application = ApplicationBuilder().token(TOKEN).build()

    # fix
    welcome_handler = ChatMemberHandler(welcome, ChatMemberHandler.ANY_CHAT_MEMBER)

    start_handler = CommandHandler('start', start)
    get_score_handler = CommandHandler('score', get_score)
    help_handler = CommandHandler('help', helper)
    
    
    call_handler = CallbackQueryHandler(status)
    
    application.add_handlers([welcome_handler, start_handler,
                             call_handler, get_score_handler, help_handler])

    application.run_polling()
