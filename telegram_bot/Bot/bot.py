import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from os import getenv

TOKEN = getenv('TG_TOKEN')
url = getenv('URL')

# Quando il bot viene startato deve capire se l'ID chat si trova nel database
# Se Admin allora registra i nuovi bidoni nell'appartamento
# Se User deve essere guidato nella comprensione dell'app


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    id_user = update.effective_user.name
    if requests.get(url + 'checkUsername/{}'.format(id_user)).content.decode('UTF-8') == 'True':
        requests.get(url + 'setSession/{}'.format(id_user))
        await update.message.reply_text('Sessione salvata')
    
    else:
        await update.message.reply_text("Utente non registrato, contatti l'amministratore condominiale.")

async def get_score(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass

async def helper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass


if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)
    get_score_handler = CommandHandler('score', get_score)
    help_handler = CommandHandler('help', helper)

    
    application.add_handler(start_handler)
    application.add_handler(get_score_handler)
    application.add_handler(help_handler)

    application.run_polling()
