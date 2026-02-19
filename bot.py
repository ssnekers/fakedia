import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

users = {}

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.effective_user.username
    chat_id = update.effective_chat.id

    if username:
        users[username.lower()] = chat_id
        await update.message.reply_text("✅ Ти зареєстрований!")
    else:
        await update.message.reply_text("❌ Встанови username в Telegram.")

# /send_file username android|ios
async def send_file(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) != 2:
        await update.message.reply_text(
            "❌ Використання: /send_file username android|ios"
        )
        return

    username = context.args[0].replace("@", "").lower()
    platform = context.args[1].lower()

    if username not in users:
        await update.message.reply_text("❌ Користувач не натискав /start")
        return

    chat_id = users[username]

    # ANDROID → надсилаємо файл
    if platform == "android":
        try:
            with open("files/android.apk", "rb") as file:
                await context.bot.send_document(chat_id=chat_id, document=file)

            await update.message.reply_text("✅ Android файл надіслано!")
        except Exception as e:
            await update.message.reply_text(f"❌ Помилка: {e}")

    # IOS → надсилаємо username бота
    elif platform == "ios":
        try:
            await context.bot.send_message(
                chat_id=chat_id,
                text="🍎 Для iPhone переходь сюди:\n👉 @funpapers_bot"
            )

            await update.message.reply_text("✅ iOS версію надіслано!")
        except Exception as e:
            await update.message.reply_text(f"❌ Помилка: {e}")

    else:
        await update.message.reply_text("❌ Платформа має бути android або ios")


app = ApplicationBuild
