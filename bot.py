import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# ===== НАЛАШТУВАННЯ =====
BOT_TOKEN = os.getenv("BOT_TOKEN")
CARD_NUMBER = "4874070052298484"

# Шляхи до файлів (тепер через папку files)
ANDROID_FILE = "files/android_app.apk"
IPHONE_FILE = "files/iphone_app.ipa"

PRICES = {
    "android": 140,
    "iphone": 170,
}

# ===== ЛОГУВАННЯ =====
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# ===== /start =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("🤖 Android — 140 грн", callback_data="buy_android"),
            InlineKeyboardButton("🍎 iPhone — 170 грн", callback_data="buy_iphone"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "👋 Вітаємо!\n\nОберіть версію додатку для покупки:",
        reply_markup=reply_markup,
    )


# ===== ОБРОБКА КНОПОК =====
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "buy_android":
        platform = "Android"
        price = PRICES["android"]
        context.user_data["platform"] = "android"

    elif query.data == "buy_iphone":
        platform = "iPhone"
        price = PRICES["iphone"]
        context.user_data["platform"] = "iphone"

    elif query.data == "confirm_payment":
        await send_file(query, context)
        return

    elif query.data == "back":
        await back_to_menu(query)
        return

    else:
        return

    keyboard = [
        [InlineKeyboardButton("✅ Я оплатив(ла)", callback_data="confirm_payment")],
        [InlineKeyboardButton("⬅️ Назад", callback_data="back")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        f"💳 Для оплати версії *{platform}* ({price} грн) переказуйте на картку:\n\n"
        f"`{CARD_NUMBER}`\n\n"
        f"Сума: *{price} грн*\n\n"
        f"Після оплати натисніть кнопку нижче 👇",
        parse_mode="Markdown",
        reply_markup=reply_markup,
    )


# ===== НАДСИЛАННЯ ФАЙЛУ =====
async def send_file(query, context: ContextTypes.DEFAULT_TYPE):
    platform = context.user_data.get("platform")

    await query.edit_message_text("⏳ Перевіряємо оплату... Надсилаємо файл!")

    try:
        if platform == "android":
            if not os.path.exists(ANDROID_FILE):
                raise FileNotFoundError(ANDROID_FILE)

            with open(ANDROID_FILE, "rb") as f:
                await query.message.reply_document(
                    document=f,
                    filename="app_android.apk",
                    caption="✅ Дякуємо за покупку!\n\nВстановіть APK вручну (дозвольте невідомі джерела).",
                )

        elif platform == "iphone":
            if not os.path.exists(IPHONE_FILE):
                raise FileNotFoundError(IPHONE_FILE)

            with open(IPHONE_FILE, "rb") as f:
                await query.message.reply_document(
                    document=f,
                    filename="app_iphone.ipa",
                    caption="✅ Дякуємо за покупку!\n\nДля встановлення використовуйте AltStore або інший IPA-інсталятор.",
                )

        else:
            await query.message.reply_text(
                "❌ Помилка. Почніть заново командою /start"
            )

    except FileNotFoundError as e:
        logger.error(f"Файл не знайдено: {e}")
        await query.message.reply_text(
            "⚠️ Файл тимчасово недоступний. Зверніться до адміністратора."
        )


# ===== НАЗАД =====
async def back_to_menu(query):
    keyboard = [
        [
            InlineKeyboardButton("🤖 Android — 140 грн", callback_data="buy_android"),
            InlineKeyboardButton("🍎 iPhone — 170 грн", callback_data="buy_iphone"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        "Оберіть версію додатку для покупки:",
        reply_markup=reply_markup,
    )


# ===== ЗАПУСК =====
def main():
    if not BOT_TOKEN:
        raise ValueError("❌ BOT_TOKEN не знайдено в Environment Variables")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    logger.info("Бот запущено!")
    app.run_polling()


if __name__ == "__main__":
    main()
