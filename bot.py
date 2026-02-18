from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    CallbackContext,
)

# -------------------------
TOKEN = "Твій_BOT_TOKEN"  # Твій токен бота

# Файли для роздачі
ANDROID_FILE = "files/app_android.apk"
IOS_FILE = "files/app_ios.ipa"

# Банківська карта для оплати
BANK_CARD = "4874 0700 5229 8484"

# Допустимі користувачі, які можуть надсилати файл
ALLOWED_USERS = ["x_getaway_x", "arielend"]
# -------------------------

# /start
async def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("📱 Android – 140₴", callback_data="choose_android")],
        [InlineKeyboardButton("🍎 iOS – 170₴", callback_data="choose_ios")],
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 Ласкаво просимо! Виберіть платформу, яку хочете придбати:", 
        reply_markup=markup
    )

# Обробка вибору платформи
async def choose_platform(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if query.data == "choose_android":
        context.user_data["file"] = ANDROID_FILE
        platform = "Android"
        price = "140₴"
    else:
        context.user_data["file"] = IOS_FILE
        platform = "iOS"
        price = "170₴"

    keyboard = [
        [InlineKeyboardButton("✅ Я оплатив", callback_data="paid")],
        [InlineKeyboardButton("❌ Відмінити", callback_data="cancel")],
    ]
    markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text=(
            f"💳 Ви обрали *{platform}*.\n\n"
            f"Будь ласка, перекажіть оплату на картку:\n"
            f"*{BANK_CARD}*\n\n"
            f"Сума: *{price}*\n\n"
            "Після оплати натисніть кнопку ✅ 'Я оплатив', "
            "або ❌ 'Відмінити', якщо передумали."
        ),
        reply_markup=markup,
        parse_mode="Markdown"
    )

# Обробка кнопок "Я оплатив" / "Відмінити"
async def payment_buttons(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if query.data == "paid":
        await query.edit_message_text(
            "⏳ Очікуйте, йде перевірка оплати...\n"
            "Наш менеджер перевірить вашу оплату і надішле файл найближчим часом."
        )
    elif query.data == "cancel":
        await query.edit_message_text("❌ Оплата скасована. Ви можете зробити спробу пізніше.")

# Команда для клієнта: надіслати файл після перевірки
async def send_file(update: Update, context: CallbackContext):
    user_name = update.message.from_user.username
    if user_name not in ALLOWED_USERS:
        await update.message.reply_text("⛔ Ви не маєте прав для цієї команди!")
        return

    try:
        target_username = context.args[0]  # username користувача
        file_type = context.args[1]       # android / ios

        if file_type.lower() == "android":
            file_path = ANDROID_FILE
        elif file_type.lower() == "ios":
            file_path = IOS_FILE
        else:
            await update.message.reply_text("❌ Використання: /send_file @username android|ios")
            return

        await context.bot.send_document(chat_id=target_username, document=open(file_path, "rb"))
        await update.message.reply_text(f"✅ Файл успішно надіслано користувачу {target_username}")
    except:
        await update.message.reply_text("❌ Помилка. Використання: /send_file @username android|ios")

# -------------------------
# Налаштування бота
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(choose_platform, pattern="choose_"))
app.add_handler(CallbackQueryHandler(payment_buttons, pattern="^(paid|cancel)$"))
app.add_handler(CommandHandler("send_file", send_file))

# Запуск бота
app.run_polling()
