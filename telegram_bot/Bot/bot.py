import requests
import text
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, ChatMemberHandler, CallbackQueryHandler, InvalidCallbackData
from os import getenv

TOKEN = getenv('TG_TOKEN')
url_db = getenv('URL_db')
url_get = getenv('URL_get')
url_set = getenv('URL_set')
url_check = getenv('URL_check')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message is not None:
        id_user = update.effective_user.name

        if requests.get(url_check + f'checkUsername/{id_user}').content.decode('UTF-8') == 'True':
            requests.get(url_set + f'set_TelegramSession/{id_user}&{update.message.chat.id}')
            await update.message.reply_text(f'Sessione salvata, benvenuto: {id_user}')

        else:
            await update.message.reply_text(text.unregistered_user)


async def get_score(update: Update, context: ContextTypes.DEFAULT_TYPE):

    id_user = update.effective_user.name

    if requests.get(url_get + f'getSession/{id_user}').content.decode('UTF-8') == 'True':
        resp = requests.get(url_get + f'getScore/{id_user}')
        
        await update.message.reply_text('Punteggio attuale: ' + str(resp.content.decode('UTF-8')))
    else:
        await update.message.reply_text(text.init_error_message)


async def get_leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    id_user = update.effective_user.name

    if requests.get(url_get + f'getSession/{id_user}').content.decode('UTF-8') == 'True':
        resp = requests.get(url_get + f'leaderboard')
        
        await update.message.reply_text('Leaderboard attuale:\n ' + str(resp.content.decode('UTF-8')))
    else:
        await update.message.reply_text(text.init_error_message)

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Attende che il valore presente nel pulsante venga cliccato
    query = update.callback_query
    await query.answer()

    answer = query.data

    # Estraggo l'id_bin dal testo della notifica
    id_bin = re.findall('\[(\d+)\]', query.message.text)[0]

    send_choice = requests.get(url_db + ('solved/' if answer ==
                 'solved' else 'report/') + f'{query.from_user.id}&{int(id_bin)}')

    await query.edit_message_text(text=f"{send_choice.content.decode('utf-8')}")



async def helper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text.help_text)


if __name__ == '__main__':

    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)
    get_score_handler = CommandHandler('score', get_score)
    get_leaderboard_handler = CommandHandler('leaderboard', get_leaderboard)
    help_handler = CommandHandler('help', helper)

    call_handler = CallbackQueryHandler(status)

    application.add_handlers([start_handler,get_leaderboard_handler,
                             call_handler, get_score_handler, help_handler])

    application.run_polling()
