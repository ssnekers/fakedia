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
BOT_TOKEN = os.getenv"8368024318:AAEK6Bk7xZojVPXzvmevNM475EUBoZfLXMU"
CARD_NUMBER = "4874070052298484"

# Вкажи реальну назву свого APK-файлу
ANDROID_FILE = "Дія.apk"

PRICE = 140

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
            InlineKeyboardButton(
                f"🤖 Android — {PRICE} грн",
                callback_data="buy_android"
            ),
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
        context.user_data["platform"] = "android"

        keyboard = [
            [InlineKeyboardButton("✅ Я оплатив(ла)", callback_data="confirm_payment")],
            [InlineKeyboardButton("⬅️ Назад", callback_data="back")],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            f"💳 Для оплати версії Android ({PRICE} грн) переказуйте на картку:\n\n"
            f"`{CARD_NUMBER}`\n\n"
            f"Сума: *{PRICE} грн*\n\n"
            f"Після оплати натисніть кнопку нижче 👇",
            parse_mode="Markdown",
            reply_markup=reply_markup,
        )

    elif query.data == "confirm_payment":
        await send_file(query, context)

    elif query.data == "back":
        await back_to_menu(query)


# ===== НАДСИЛАННЯ ФАЙЛУ =====
async def send_file(query, context: ContextTypes.DEFAULT_TYPE):
    await query.edit_message_text("⏳ Перевіряємо оплату... Надсилаємо файл!")

    try:
        if not os.path.exists(ANDROID_FILE):
            raise FileNotFoundError(ANDROID_FILE)

        with open(ANDROID_FILE, "rb") as f:
            await query.message.reply_document(
                document=f,
                filename="app_android.apk",
                caption="✅ Дякуємо за покупку!\n\n"
                        "Для встановлення дозвольте інсталяцію з невідомих джерел.",
            )

    except FileNotFoundError:
        logger.error("APK файл не знайдено")
        await query.message.reply_text(
            "⚠️ Файл тимчасово недоступний. Зверніться до адміністратора."
        )


# ===== НАЗАД =====
async def back_to_menu(query):
    keyboard = [
        [
            InlineKeyboardButton(
                f"🤖 Android — {PRICE} грн",
                callback_data="buy_android"
            ),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        "👋 Оберіть версію додатку для покупки:",
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
