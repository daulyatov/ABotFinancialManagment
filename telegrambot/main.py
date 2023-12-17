import logging

import telebot
from telebot import types

from django.conf import settings
from telegrambot.models import TelegramUser

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

bot = telebot.TeleBot(settings.TOKENBOT)

@bot.message_handler(commands=['start'])
def start(message):
    user = message.from_user

    model_user, created = TelegramUser.objects.get_or_create(user_id=user.id)

    if created:
        model_user.user_id = user.id
        model_user.username = user.username
        model_user.first_name = user.first_name
        model_user.last_name = user.last_name
        model_user.language_code = user.language_code
        model_user.is_bot = user.is_bot
        model_user.save()

        logging.info(f"Новый пользователь: {model_user.get_name()}")
        

    bot.send_message(message.chat.id, f"Привет, {model_user.get_name()}!")

def RunBot():
    try:
        logger = logging.getLogger("RunBot")
        logger.info("Запуск бота!")
        bot.polling(none_stop=True, interval=0)
        
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}!")
        raise e
    
    except KeyboardInterrupt:
        logger.info("Бот остановлен принудительно!")
    
    finally:
        logger.info("Завершение работы бота!")
        
