import random, asyncio
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, BotCommand, BotCommandScopeDefault
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters, Defaults, ConversationHandler
from telegram.constants import ParseMode, ChatAction
from telegram.ext.filters import BaseFilter

EMOJIS = ['😀', '😂', '🤣', '😍', '🥰', '😎', '🤩', '🥳', '🤯', '👻', 
          '💩', '🤖', '👽', '🐶', '🐱', '🦄', '🐉', '🍕', '🍔', '🎮']

COLOR = ['🔴', '🔵', '🟢', '🟡',
         '🟠', '🟣', '⚫', '⚪']

NAME, AGE, BIO = range(3)

user_data = {}

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

def get_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("Info", callback_data='info'),
            InlineKeyboardButton("Help", callback_data='help')
        ],

        [
            InlineKeyboardButton("Color", callback_data='color'),
            InlineKeyboardButton("Emoji", callback_data='emoji')
        ], 

        [
            InlineKeyboardButton("Clear", callback_data='clear'),
            InlineKeyboardButton("Фото", callback_data='photo')
        ],       
    ]
    return InlineKeyboardMarkup(keyboard)

def get_dice_keyboard():
    dice_keyboard = [
        [
            InlineKeyboardButton("Перекрутить", callback_data='reroll_dice')
        ]
    ]
    return InlineKeyboardMarkup(dice_keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await welcome(update, context)
    # reply_markup = InlineKeyboardMarkup(keyboard)

    # custom_keyboard = [
    #     [
    #         KeyboardButton("Дата и время"),
    #         KeyboardButton("Статистика")
    #     ],

    #     [
    #         KeyboardButton("Фото"),
    #         KeyboardButton("Бросить кости")
    #     ]
    # ]
    # custom_reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)

    # await update.message.reply_text("Привет", reply_markup=reply_markup)
    # await update.message.reply_text("Кнопки", reply_markup=custom_reply_markup)

async def show_typing(update: Update, context: ContextTypes.DEFAULT_TYPE, duration: float=1.0):
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    await asyncio.sleep(duration) 

async def setup(app: Application):
    commands = [
        BotCommand("start", "Начнём работу!"),
        BotCommand("register", "Начать регистрацию"),
        BotCommand("info", "Инфотрмация о боте"),
        BotCommand("help", "Все комманды"),
        BotCommand("photo", "Красивое фото"),
        BotCommand("color", "Рандомный цвет"),
        BotCommand("emoji", "Рандомные 3 эмодзи"),
        BotCommand("clear", "Очистить чат"),
        BotCommand("dice", "Крутить кости")
    ]
    await app.bot.set_my_commands(commands, scope=BotCommandScopeDefault())

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
    Доступные команды:
/start - Начать работу
/register - Начать регистрацию
/help - Помощь
/info - Информация
/color - Случайный цвет
/emoji - Случайные эмодзи
/clear - Очистить чат """
    await show_typing(update, context)
    await update.message.reply_text(help_text)

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    info_text = "Это бот, который делает разные вещи"
    await show_typing(update, context)
    await update.message.reply_text(info_text)

async def color(update: Update, context: ContextTypes.DEFAULT_TYPE):
    color = ' '.join(random.choices(COLOR, k=1))
    await show_typing(update, context)
    await update.message.reply_text(text=f"Случайный цвет: {color}")

async def emoji(update: Update, context: ContextTypes.DEFAULT_TYPE):
    emojis = ' '.join(random.choices(EMOJIS, k=3))
    await show_typing(update, context)
    await update.message.reply_text(text=f"Случайные эмодзи: {emojis}")

async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    last_message_id = update.effective_message.message_id

    try:
        for i in range(5):
            try:
                await context.bot.delete_message(chat_id, last_message_id - i)
            except Exception:
                continue
            #await asyncio.sleep(0.1)

        await show_typing(update, context)
        await context.bot.send_message(chat_id, "Чат очищен! 🧹")
    except Exception as e:
        await show_typing(update, context)
        await context.bot.send_message(chat_id, f"Ошибка при очистке: {e}")

async def date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await show_typing(update, context)
    await update.message.reply_text(f"Текущее время: {current_time}")

async def send_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "Кот Василий"
    try:
        with open('image.png', 'rb') as photo:
            await show_typing(update, context)
            await update.message.reply_photo(photo, text)
    
    except FileNotFoundError:
        await show_typing(update, context)
        await update.message.reply_text("Ошибка")

async def dice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_typing(update, context)
    await context.bot.send_dice(
        chat_id=update.effective_chat.id,
        reply_markup=get_dice_keyboard()
    )

async def reroll_dice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await context.bot.send_dice(
        chat_id=update.effective_chat.id,
        reply_markup=get_dice_keyboard()
    )

async def start_registration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_typing(update, context)
    await update.message.reply_text("Привет, как тебя зовут?", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Отмена', callback_data='cancle_reg')]]))
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in user_data:
        user_data[user_id]={}
    print(user_data[user_id])

    user_data[user_id]["name"] = update.message.text

    await show_typing(update, context)
    await update.message.reply_text("Приятно познакомиться, {update.message.text}. Сколько тебе лет?", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Отмена', callback_data='cancle_reg')]]))
    return AGE

async def get_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    age = int(update.message.text)
    user_id = update.effective_user.id

    user_data[user_id]["age"] = age
    await show_typing(update, context)
    await update.message.reply_text("Раскажи немного о себе", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Отмена', callback_data='cancle_reg')]]))
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

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "Все комманды":
        await help(update, context)

    elif text == "Фото":
        await send_photo(update, context)

    elif text == "Бросить кости":
        await dice(update, context)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'info':
        await query.edit_message_text(text="Это бот, который делает разные вещи")

    elif query.data == 'help':
        await query.edit_message_text(text="""Доступные команды:
/start - Начать работу
/help - Помощь
/info - Информация
/color - Случайный цвет
/emoji - Случайные эмодзи
/clear - Очистить чат """)

    elif query.data == 'color':
        await color(update, context)

    elif query.data == 'emoji':
        emojis = ' '.join(random.choices(EMOJIS, k=3))
        await query.edit_message_text(text=f"Случайные эмодзи: {emojis}")

    elif query.data == 'photo':
        try:
            with open('image.png', 'rb') as photo:
                await query.message.reply_photo(photo)

        except FileNotFoundError:
            await query.message.reply_text()

    elif query.data == 'reroll_dice':
        await reroll_dice(update, context)
        
    elif query.data == 'clear':
        chat_id = update.effective_chat.id
        last_message_id = update.effective_message.message_id

        try:
            for i in range(20):
                try:
                    await context.bot.delete_message(chat_id, last_message_id - i)
                except Exception:
                    continue
                await asyncio.sleep(0.1)
            
            await context.bot.send_message(chat_id, "Чат очищен! 🧹")
        except Exception as e:
            await context.bot.send_message(chat_id, f"Ошибка при очистке: {e}")
        

def main():
    app = Application.builder().token('8129146567:AAGEHZ002jaeQ2tMUHkdKMpcVUoazb8kmfM').build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("color", color))
    app.add_handler(CommandHandler("emoji", emoji))
    app.add_handler(CommandHandler("clear", clear))
    app.add_handler(CommandHandler("date", date))
    app.add_handler(CommandHandler("photo", send_photo))
    app.add_handler(CommandHandler("dice", dice))
    app.add_handler(CallbackQueryHandler(button_callback))
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('register', start_registration)],
        states= {
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_age)],
            BIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_bio)]
        },
        fallbacks=[CallbackQueryHandler(dice, pattern='^cancle_reg$')]
    )
    app.add_handler(conv_handler)

    app.post_init = setup

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == '__main__':
    main()