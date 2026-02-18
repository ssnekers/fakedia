import sys
import types

# Фікс для Python 3.13+ (про всяк випадок)
imghdr = types.ModuleType("imghdr")
imghdr.what = lambda *a, **kw: None
sys.modules["imghdr"] = imghdr

import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CARD = "4874070052298484"
ANDROID_FILE = "files/Дія.apk"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
        InlineKeyboardButton("🤖 Android — 140 грн", callback_data="android"),
        InlineKeyboardButton("🍎 iPhone", callback_data="iphone"),
    ]]
    await update.message.reply_text(
        "👋 Вітаємо! Оберіть версію додатку:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # ===== ANDROID =====
    if data == "android":
        context.user_data["platform"] = "android"
        keyboard = [
            [InlineKeyboardButton("✅ Я оплатив(ла)", callback_data="paid")],
            [InlineKeyboardButton("⬅️ Назад", callback_data="back")],
        ]
        await query.edit_message_text(
            f"💳 Оплата версії *Android* — *140 грн*\n\n"
            f"Переказуйте на картку:\n`{CARD}`\n\n"
            f"Після оплати натисніть кнопку нижче 👇",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # ===== IPHONE =====
    elif data == "iphone":
        await query.edit_message_text(
            "📱 Версія для iPhone доступна через бота:\n\n👉 @funpapers_bot"
        )

    # ===== PAID =====
    elif data == "paid":
        await query.edit_message_text("⏳ Надсилаємо файл...")
        try:
            with open(ANDROID_FILE, "rb") as f:
                await query.message.reply_document(
                    document=f,
                    caption="✅ Дякуємо за покупку! Ось ваш файл."
                )
        except FileNotFoundError:
            await query.message.reply_text(
                "⚠️ Файл не знайдено. Зверніться до адміністратора."
            )

    # ===== BACK =====
    elif data == "back":
        keyboard = [[
            InlineKeyboardButton("🤖 Android — 140 грн", callback_data="android"),
            InlineKeyboardButton("🍎 iPhone", callback_data="iphone"),
        ]]
        await query.edit_message_text(
            "👋 Оберіть версію додатку:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN не знайдено!")

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle))

    logging.info("Бот запущено!")
    app.run_polling()


if __name__ == "__main__":
    main()

