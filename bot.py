import random, asyncio
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, BotCommand, BotCommandScopeDefault
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters, Defaults, ConversationHandler
from telegram.constants import ParseMode, ChatAction
from telegram.ext.filters import BaseFilter

user_data = {}

NAME, AGE, BIO = range(3)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_name = user.first_name

    welcome_text = f"Привет {user_name},\n"\
                    "\n"\
                    "Я умею генерировать рандомные эмодзи\n"\
                    "\n"\
                    "Выберите действие из меню ниже."
    try:
        with open ('cat.jpg', 'rb') as photo:
            await show_typing(update, context)
            await update.message.reply_photo(photo, caption=welcome_text, parse_mode=ParseMode.MARKDOWN, reply_markup=reg_keyboard())

    except FileNotFoundError:
        await show_typing(update, context)
        await update.message.reply_text(welcome_text, parse_mode=ParseMode.MARKDOWN, reply_markup=reg_keyboard())

async def show_typing(update: Update, context: ContextTypes.DEFAULT_TYPE, duration: float=1.0):
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    await asyncio.sleep(duration)

def reg_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("Start registration", callback_data='start_registration')
        ]    
    ]
    return InlineKeyboardMarkup(keyboard)  

def get_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("Info", callback_data='info'),
            InlineKeyboardButton("Number", callback_data='number')
        ]    
    ]
    return InlineKeyboardMarkup(keyboard)       

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    info_text = "Это бот, который делает разные вещи"
    await show_typing(update, context)
    await update.message.reply_text(info_text)

async def random_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    number = random.randint(1, 9)
    await show_typing(update, context)
    await update.message.reply_text(text=f"Рандомные числа {number}")

async def start_registration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_typing(update, context)
    await update.message.reply_text("Привет, как тебя зовут?")
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in user_data:
        user_data[user_id]={}
    print(user_data[user_id])

    user_data[user_id]["name"] = update.message.text

    await show_typing(update, context)
    await update.message.reply_text("Приятно познакомиться, {update.message.text}. Сколько тебе лет?")
    return AGE

async def get_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    age = int(update.message.text)
    user_id = update.effective_user.id

    user_data[user_id]["age"] = age
    await show_typing(update, context)
    await update.message.reply_text("Раскажи немного о себе")
    return BIO

async def get_bio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data[user_id]["bio"] = update.message.text
    await show_typing(update, context)
    await update.message.reply_text(
        f'Регистрация завершена\n\n'
        f'Имя: {user_data[user_id]["name"]}\n'
        f'Возраст: {user_data[user_id]["age"]}\n'
        f'Био: {user_data[user_id]["bio"]}'
    )
    return ConversationHandler.END

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'info':
        info_text = "Это бот, который делает разные вещи"
        await show_typing(update, context)
        await query.message.reply_text(info_text)

    elif query.data == 'number':
        number = random.randint(1, 9)
        await show_typing(update, context)
        await query.message.reply_text(text=f"Рандомные числа {number}")

    elif query.data == 'start_registration':
        await show_typing(update, context)
        await start_registration(update, context)

def main():
    app = Application.builder().token('8129146567:AAGEHZ002jaeQ2tMUHkdKMpcVUoazb8kmfM').build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("number", random_number))
    app.add_handler(CallbackQueryHandler(button_callback))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('register', start_registration)],
        states= {
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_age)],
            BIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_bio)]
        },
        fallbacks=[CallbackQueryHandler(info, pattern='^cancle_reg$')]
    )
    app.add_handler(conv_handler)

    # app.post_init = setup

    # app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == '__main__':
    main()