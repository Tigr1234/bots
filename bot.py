import random, asyncio
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, BotCommand, BotCommandScopeDefault
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters, Defaults, ConversationHandler
from telegram.constants import ParseMode, ChatAction
from telegram.ext.filters import BaseFilter

from logger_config import setup_logger, log_error,  log_bot_startup, log_bot_shutdown, log_user_action
from error_handler import handle_errors

logger = setup_logger('tglog')
user_data = {}

EMOJIS = ['😀', '😂', '🤣', '😍', '🥰', '😎', '🤩', '🥳', '🤯', '👻', 
          '💩', '🤖', '👽', '🐶', '🐱', '🦄', '🐉', '🍕', '🍔', '🎮']

COLOR = ['🔴', '🔵', '🟢', '🟡',
         '🟠', '🟣', '⚫', '⚪']

NAME, AGE, BIO = range(3)

@handle_errors(logger)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_name = user.first_name
    user_id = user.id

    welcome_text = f"Привет {user_name},\n"\
                    "\n"\
                    "Я умею генерировать рандомные эмодзи\n"\
                    "\n"\
                    "Выберите действие из меню ниже."
    
    if user_id in user_data and all(key in user_data[user_id] for key in ("name", "age", "bio")):
        reply_markup = get_keyboard()

    else:
        reply_markup = reg_keyboard()

    try:
        with open ('cat.jpg', 'rb') as photo:
            await show_typing(update, context)
            await update.message.reply_photo(photo, caption=welcome_text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)

    except FileNotFoundError:
        await show_typing(update, context)
        await update.message.reply_text(welcome_text, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)

async def show_typing(update: Update, context: ContextTypes.DEFAULT_TYPE, duration: float=0.5):
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
        ],
        [
            InlineKeyboardButton("Color", callback_data='color'),
            InlineKeyboardButton("Emoji", callback_data='emoji')
        ],
        [
            InlineKeyboardButton("Date", callback_data='date'),
            InlineKeyboardButton("Dice", callback_data='dice')
        ]   
    ]
    return InlineKeyboardMarkup(keyboard)       

@handle_errors(logger)
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    info_text = "Это бот, который делает разные вещи"
    await show_typing(update, context)
    message = update.message or update.callback_query.message
    await message.reply_text(info_text)

@handle_errors(logger)
async def random_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    number = random.randint(1, 9)
    await show_typing(update, context)
    message = update.message or update.callback_query.message
    await message.reply_text(text=f"Рандомные числа {number}")

@handle_errors(logger)
async def color(update: Update, context: ContextTypes.DEFAULT_TYPE):
    color = ' '.join(random.choices(COLOR, k=1))
    await show_typing(update, context)
    message = update.message or update.callback_query.message
    await message.reply_text(text=f"Случайный цвет: {color}")

@handle_errors(logger)
async def emoji(update: Update, context: ContextTypes.DEFAULT_TYPE):
    emojis = ' '.join(random.choices(EMOJIS, k=3))
    await show_typing(update, context)
    message = update.message or update.callback_query.message
    await message.reply_text(text=f"Случайные эмодзи: {emojis}")

@handle_errors(logger)
async def date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await show_typing(update, context)
    message = update.message or update.callback_query.message
    await message.reply_text(f"Текущее время: {current_time}")

@handle_errors(logger)
async def dice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_typing(update, context)
    await context.bot.send_dice(
        chat_id=update.effective_chat.id,
        reply_markup=get_keyboard()
    )

@handle_errors(logger)
async def reroll_dice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await context.bot.send_dice(
        chat_id=update.effective_chat.id,
        reply_markup=get_keyboard()
    )

@handle_errors(logger)
async def start_registration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_typing(update, context)
    message = update.message or update.callback_query.message
    await message.reply_text("Привет, как тебя зовут?")
    logger.info(f'regestration started for user: {update.effective_user.id}')
    return NAME

@handle_errors(logger)
async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in user_data:
        user_data[user_id]={}
    print(user_data[user_id])

    user_data[user_id]["name"] = update.message.text
    logger.info(f'user: {user_id} name: {update.message.text}')

    await show_typing(update, context)
    message = update.message or update.callback_query.message
    await message.reply_text(f"Приятно познакомиться, {update.message.text}. Сколько тебе лет?")
    return AGE

@handle_errors(logger)
async def get_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    age = int(update.message.text)
    user_id = update.effective_user.id

    user_data[user_id]["age"] = age
    logger.info(f'user: {user_id} age: {age}')

    await show_typing(update, context)
    message = update.message or update.callback_query.message
    await message.reply_text("Раскажи немного о себе")
    return BIO

@handle_errors(logger)
async def get_bio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_data[user_id]["bio"] = update.message.text

    await show_typing(update, context)
    message = update.message or update.callback_query.message
    await message.reply_text(
        f'Регистрация завершена\n\n'
        f'Имя: {user_data[user_id]["name"]}\n'
        f'Возраст: {user_data[user_id]["age"]}\n'
        f'Био: {user_data[user_id]["bio"]}'
    )
    logger.info(f'regestration completed for user: {user_id}')
    return ConversationHandler.END

@handle_errors(logger)
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'info':
        await show_typing(update, context)
        await info(update,context)

    elif query.data == 'number':
        await show_typing(update, context)
        await random_number(update, context)

    elif query.data == 'color':
        await color(update, context)

    elif query.data == 'emoji':
        await show_typing(update, context)
        await emoji(update, context)

    elif query.data == 'date':
        await show_typing(update, context)
        await date(update, context)

    elif query.data == 'dice':
        await show_typing(update, context)
        await dice(update, context)


def main():
    app = Application.builder().token('8129146567:AAGEHZ002jaeQ2tMUHkdKMpcVUoazb8kmfM').build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("number", random_number))
    app.add_handler(CommandHandler("color", color))
    app.add_handler(CommandHandler("emoji", emoji))
    app.add_handler(CommandHandler("date", date))
    app.add_handler(CommandHandler("dice", dice))

    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(start_registration, pattern='^start_registration')],
        states= {
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_age)],
            BIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_bio)]
        },
        fallbacks=[CallbackQueryHandler(info, pattern='^cancle_reg$')]
    )
    app.add_handler(conv_handler)

    app.add_handler(CallbackQueryHandler(button_callback))

    log_bot_startup(logger, 'startup')

    # app.post_init = setup

    # app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == '__main__':
    main()