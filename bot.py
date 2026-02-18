from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    CallbackContext,
)

# -------------------------
TOKEN = "8368024318:AAEoV01O8LSQy4_IvTfQ6AmaqgUz19dA3cY"

# Файли для роздачі
ANDROID_FILE = "files/app_android.apk"
IOS_FILE = "files/app_ios.ipa"

# Банківська карта для оплати
BANK_CARD = "UA1234 5678 9012 3456"

# Допустимі користувачі, які можуть надсилати файл
ALLOWED_USERS = ["x_getaway_x", "arielend"]
# -------------------------

# Команда /start
async def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Android", callback_data="choose_android")],
        [InlineKeyboardButton("iOS", callback_data="choose_ios")],
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Виберіть платформу:", reply_markup=markup)

# Обробка вибору платформи
async def choose_platform(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if query.data == "choose_android":
        context.user_data["file"] = ANDROID_FILE
        platform = "Android"
    else:
        context.user_data["file"] = IOS_FILE
        platform = "iOS"

    keyboard = [
        [InlineKeyboardButton("Я оплатив", callback_data="paid")],
        [InlineKeyboardButton("Відмінити", callback_data="cancel")],
    ]
    markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text=f"Ви обрали {platform}.\n\nОплата на картку:\n{BANK_CARD}",
        reply_markup=markup
    )

# Обробка кнопок "Я оплатив" / "Відмінити"
async def payment_buttons(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if query.data == "paid":
        await query.edit_message_text("Очікуйте, перевірка оплати...")
    elif query.data == "cancel":
        await query.edit_message_text("Оплата скасована.")

# Команда для клієнта: надіслати файл після перевірки
async def send_file(update: Update, context: CallbackContext):
    user_name = update.message.from_user.username
    if user_name not in ALLOWED_USERS:
        await update.message.reply_text("Ви не маєте прав для цієї команди!")
        return

    try:
        target_username = context.args[0]  # username користувача
        file_type = context.args[1]       # android / ios

        if file_type.lower() == "android":
            file_path = ANDROID_FILE
        elif file_type.lower() == "ios":
            file_path = IOS_FILE
        else:
            await update.message.reply_text("Використання: /send_file @username android|ios")
            return

        await context.bot.send_document(chat_id=target_username, document=open(file_path, "rb"))
        await update.message.reply_text(f"Файл надіслано користувачу {target_username}")
    except:
        await update.message.reply_text("Помилка. Використання: /send_file @username android|ios")

# -------------------------
# Налаштування бота
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(choose_platform, pattern="choose_"))
app.add_handler(CallbackQueryHandler(payment_buttons, pattern="^(paid|cancel)$"))
app.add_handler(CommandHandler("send_file", send_file))

# Запуск бота
app.run_polling()
