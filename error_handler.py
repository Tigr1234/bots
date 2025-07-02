import asyncio, functools
from telegram import Update
from telegram.ext import ContextTypes
from logger_config import log_user_action, log_error

def handle_errors(logger):
    def decorator(func):
        @functools.wraps(func)
        async def wraper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
            try:
                if update and update.effective_user:
                    user = update.effective_user
                    log_user_action(logger, user.id, user.username or user.first_name, f"Команда {func.__name__}")
                return await func(update, context, *args, **kwargs)
            
            except Exception as e:
                context_info = f"Команда {func.__name__}"
                if update and update.effective_user:
                    context_info += f", user: {update.effective_user.id}"
                log_error(logger, e, context_info)

        return wraper
    return decorator

# def handle_network_errors(logger):
#     def decorator(func):
#         @functools.wraps(func)
#         async def wraper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
#             try:
#                 if update and update.effective_user:
#                     user = update.effective_user
                    