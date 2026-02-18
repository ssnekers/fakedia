import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CARD = "4874070052298484"
ANDROID_FILE = "files/Дія.apk"
IPHONE_FILE = "files/Дія.ipa"


def start(update: Update, context: CallbackContext):
    keyboard = [
        [
            InlineKeyboardButton("🤖 Android — 140 грн", callback_data="android"),
            InlineKeyboardButton("🍎 iPhone — 170 грн", callback_data="iphone"),
        ]
    ]
    update.message.reply_text(
        "👋 Вітаємо! Оберіть версію додатку:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


def handle(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    data = query.data

    if data == "android":
        context.user_data["platform"] = "android"
        price, name = 140, "Android"
    elif data == "iphone":
        context.user_data["platform"] = "iphone"
        price, name = 170, "iPhone"
    elif data == "paid":
        platform = context.user_data.get("platform")
        query.edit_message_text("⏳ Надсилаємо файл...")
        filepath = ANDROID_FILE if platform == "android" else IPHONE_FILE
        try:
            with open(filepath, "rb") as f:
                query.message.reply_document(
                    document=f,
                    caption="✅ Дякуємо за покупку! Ось ваш файл."
                )
        except FileNotFoundError:
            query.message.reply_text("⚠️ Файл не знайдено. Зверніться до адміністратора.")
        return
    elif data == "back":
        keyboard = [
            [
                InlineKeyboardButton("🤖 Android — 140 грн", callback_data="android"),
                InlineKeyboardButton("🍎 iPhone — 170 грн", callback_data="iphone"),
            ]
        ]
        query.edit_message_text(
            "👋 Оберіть версію додатку:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return
    else:
        return

    keyboard = [
        [InlineKeyboardButton("✅ Я оплатив(ла)", callback_data="paid")],
        [InlineKeyboardButton("⬅️ Назад", callback_data="back")],
    ]
    query.edit_message_text(
        f"💳 Оплата версії *{name}* — *{price} грн*\n\n"
        f"Переказуйте на картку:\n`{CARD}`\n\n"
        f"Після оплати натисніть кнопку нижче 👇",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN не знайдено!")

    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(handle))

    logging.info("Бот запущено!")
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
