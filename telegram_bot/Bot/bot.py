import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, ChatMemberHandler
from os import getenv

TOKEN = getenv('TG_TOKEN')
url = getenv('URL')

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = 'Questo è un messaggio di benvenutos'
    await update.message.reply_text(welcome_message)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    id_user = update.effective_user.name
    
    if requests.get(url + f'checkUsername/{id_user}').content.decode('UTF-8') == 'True':
        requests.get(url + f'setSession/{id_user}')
        await update.message.reply_text(f'Sessione salvata, benvenuto: {id_user}')

    else:
        await update.message.reply_text("Utente non registrato, contatti l'amministratore condominiale.")


async def get_score(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    id_user = update.effective_user.name
    
    if requests.get(url + f'getSession/{id_user}').content.decode('UTF-8') == 'True':
        resp = requests.get(url + f'getScore/{id_user}').content.decode('UTF-8')
        await update.message.reply_text(resp)
    else:
        await update.message.reply_text('Inizializzi il bot')


async def helper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = 'Aiutati che lo SmartBIN ti aiuta'
    await update.message.reply_text(help_text)


if __name__ == '__main__':
    
    application = ApplicationBuilder().token(TOKEN).build()

    welcome_handler = ChatMemberHandler(welcome, ChatMemberHandler.CHAT_MEMBER)

    start_handler = CommandHandler('start', start)
    get_score_handler = CommandHandler('score', get_score)
    help_handler = CommandHandler('help', helper)

    application.add_handler(welcome_handler)
    application.add_handler(start_handler)
    application.add_handler(get_score_handler)
    application.add_handler(help_handler)

    application.run_polling()
