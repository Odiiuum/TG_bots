import logging
from logging.handlers import RotatingFileHandler
from aiogram.types import Message
import os

def setup_logger(log_file: str = 'bot.log', level: str = "INFO", console_handler_bool: bool = True) -> logging.Logger:
    log_level = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }.get(level.upper(), logging.INFO)
    
    logs_directory = "logs/"
    if not os.path.exists(logs_directory):
        os.makedirs(logs_directory)
    
    logs_fullpath_file = os.path.join(logs_directory, log_file)
    
    logger = logging.getLogger()
    logger.setLevel(log_level)

    if not logger.handlers:  
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        file_handler = RotatingFileHandler(logs_fullpath_file, maxBytes=1024*1024, backupCount=5)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        if console_handler_bool:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

    return logger

def log_user_action(message: Message, action: str, logger: logging.Logger = None):
    if logger is None:
        logger = setup_logger()

    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.full_name
    log_message = f"User {username} (ID: {user_id}) performed action: {action}"
    logger.info(log_message)
