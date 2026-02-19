import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

# /send_file android|ios (через reply)
async def send_file(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Перевірка чи це reply
    if not update.message.reply_to_message:
        await update.message.reply_text(
            "❌ Використання: відповідай на повідомлення користувача та пиши:\n/send_file android або /send_file ios"
        )
        return

    if len(context.args) != 1:
        await update.message.reply_text("❌ Вкажи платформу: android або ios")
        return

    platform = context.args[0].lower()
    target_chat_id = update.message.reply_to_message.chat.id

    # ANDROID → файл
    if platform == "android":
        try:
            with open("files/android.apk", "rb") as file:
                await context.bot.send_document(
                    chat_id=target_chat_id,
                    document=file
                )

            await update.message.reply_text("✅ Android файл надіслано!")
        except Exception as e:
            await update.message.reply_text(f"❌ Помилка: {e}")

    # IOS → просто бот
    elif platform == "ios":
        try:
            await context.bot.send_message(
                chat_id=target_chat_id,
                text="🍎 Для iPhone переходь сюди:\n👉 @funpapers_bot"
            )

            await update.message.reply_text("✅ iOS версію надіслано!")
        except Exception as e:
            await update.message.reply_text(f"❌ Помилка: {e}")

    else:
        await update.message.reply_text("❌ Платформа має бути android або ios")


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("send_file", send_file))

app.run_polling()
