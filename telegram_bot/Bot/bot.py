import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from os import getenv

TOKEN = getenv('TG_TOKEN')
url = getenv('URL')

# Quando il bot viene startato deve capire se l'ID chat si trova nel database
# Se Admin allora registra i nuovi bidoni nell'appartamento
# Se User deve essere guidato nella comprensione dell'app


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    id_chat = update.effective_chat.id
    id_user = update.effective_user.name
    exist = False

    # Verifico l'identità di chi sta cercando di accedere al bot: cerco la chat id e lo user id all'interno del db.

    if requests.get(url + 'checkSession?{}&{}'.format(id_chat, id_user)) != 'False':
        exist = True

    await context.bot.send_message(id_chat, text="{} {}!\nInserisca Username".format('Bentornato' if exist else 'Benvenuto', id_user))
    username = update.message.text

    if requests.get(url + 'checkUsername?{}'.format(username)) != 'False':

        await context.bot.send_message(id_chat, text="Inserisca la password{}".format("" if exist else " assegnata"))
        password = update.message.text

        if requests.get(url + 'accessAdmin?{}&{}'.format(username, password)) != 'False':
            
            if exist:
                # Accesso consentito e si memorizza la sessione
                await context.bot.send_message(id_chat, text='Accesso riuscito, sessione esistente')

            else:
                # Si memorizza la sessione e si passa alla registrazione dei Bidoni e dei Condomini mediante form
                await context.bot.send_message(id_chat, text='Accesso riuscito, sessione non esistente')

    # Se non esiste l'admin
    else:
        await context.bot.send_message(id_chat, text="Si prega di inviare la richiesta di registrazione prima di procedere")


async def helper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass


if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', helper)

    application.add_handler(start_handler)
    application.add_handler(status_handler)
    application.add_handler(help_handler)

    application.run_polling()
