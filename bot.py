import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("8368024318:AAEoV01O8LSQy4_IvTfQ6AmaqgUz19dA3cY")

async def send_file(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message.reply_to_message:
        await update.message.reply_text(
            "❌ Відповідай на повідомлення та пиши:\n/send_file android або /send_file ios"
        )
        return

    if len(context.args) != 1:
        await update.message.reply_text("❌ Вкажи android або ios")
        return

    platform = context.args[0].lower()
    target_chat_id = update.message.reply_to_message.chat.id

    if platform == "android":
        try:
            with open("files/android.apk", "rb") as file:
                await context.bot.send_document(chat_id=target_chat_id, document=file)
            await update.message.reply_text("✅ Android надіслано!")
        except Exception as e:
            await update.message.reply_text(f"❌ Помилка: {e}")

    elif platform == "ios":
        await context.bot.send_message(
            chat_id=target_chat_id,
            text="🍎 Для iPhone переходь сюди:\n👉 @funpapers_bot"
        )
        await update.message.reply_text("✅ iOS надіслано!")

    else:
        await update.message.reply_text("❌ Платформа має бути android або ios")


async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("send_file", send_file))
    await app.run_polling()


# 🔥 Авто-restart якщо щось впаде
while True:
    try:
        asyncio.run(main())
    except Exception as e:
        print("БОТ ВПАВ:", e)
        print("Перезапуск через 5 секунд...")
        asyncio.sleep(5)
