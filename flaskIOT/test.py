from telegram.ext import ApplicationBuilder, CommandHandler
from telegram import Update


class botTG:
    async def start(update: Update, context):
        await update.message.reply_text("Ciao")


    async def status(update: Update, context):
        input = update.message.text
        print('Ciao'+input)

    async def notify(update: Update, text: str):
        await update.message.reply.text("Alert:\n" + text)


#Inizializzazione bot telegram
application = ApplicationBuilder().token('5887797061:AAEvYrnkdgFwS5nKmfoSJXNck-kzefUFEC0').build()
application.add_handler(CommandHandler("start", botTG.start))
application.add_handler(CommandHandler("status", botTG.status))

print('bot listening...')
application.run_polling()