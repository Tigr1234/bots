import os, logging
from datetime import datetime
from logging.handlers import RotatingFileHandler

def setup_logger(name = "bot_logs", log_level = logging.INFO):
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    logger.handlers.clear()
    formater = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formater)
    logger.addHandler(console_handler)
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, f'{name}.log'),
        maxBytes=5*1024*1024,
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formater)
    logger.addHandler(file_handler)
    error_handler = RotatingFileHandler(os.path.join(log_dir, f'{name}_errors.log'), maxBytes=5*1024*1024, backupCount=5, encoding='utf-8')
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formater)
    logger.addHandler(error_handler)
    return logger 

def log_user_action(logger, user_id, user_name, action, details = None):
    message = f'user: {user_name}, id: {user_id}-{action}'
    if details:
        message += f'{details}'
    logger.info(message)

def log_error(logger, error, context = None):
    message = f"error: {type(error).__name__}: {str(error)}"
    if context: 
        message += f" -context:{context}"

    logger.error(message, exe_info = True)

def log_bot_startup(logger, bot_info):
    logger.info(f"bot_started: {bot_info}")

def log_bot_shutdown(logger):
    logger.info("bot_shutdown")