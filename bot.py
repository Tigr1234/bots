import random, asyncio
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, BotCommand, BotCommandScopeDefault
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters, Defaults, ConversationHandler
from telegram.constants import ParseMode, ChatAction
from telegram.ext.filters import BaseFilter

user_data = {}

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
            await update.message.reply_photo(photo, caption=welcome_text, parse_mode=ParseMode.MARKDOWN, reply_markup=get_keyboard())

    except FileNotFoundError:
        await show_typing(update, context)
        await update.message.reply_text(welcome_text, parse_mode=ParseMode.MARKDOWN, reply_markup=get_keyboard())

async def show_typing(update: Update, context: ContextTypes.DEFAULT_TYPE, duration: float=1.0):
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    await asyncio.sleep(duration)

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

def main():
    app = Application.builder().token('8129146567:AAGEHZ002jaeQ2tMUHkdKMpcVUoazb8kmfM').build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("number", random_number))
    app.add_handler(CallbackQueryHandler(button_callback))

    app.run_polling()

if __name__ == '__main__':
    main()