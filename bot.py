from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

import os
TOKEN = os.getenv("BOT_TOKEN")

CORRECT = "ответ"

async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (update.message.text or "").strip().lower()

    if text == CORRECT:
        await update.message.reply_text("верный")
    else:
        await update.message.reply_text("неверный")

app = Application.builder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handler))

app.run_polling()