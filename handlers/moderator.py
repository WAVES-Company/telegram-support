import telebot
from config import GROUP_ID
from database import get_user_by_group_message, get_user_lang
from handlers.user import t

def register(bot: telebot.TeleBot):

    @bot.message_handler(func=lambda message: message.chat.id == GROUP_ID and message.reply_to_message is not None)
    def reply_to_user(message):
        replied_msg_id = message.reply_to_message.message_id
        user_id = get_user_by_group_message(replied_msg_id)

        if user_id:
            lang = get_user_lang(user_id)
            try:
                bot.send_message(user_id, t(lang, 'reply', text=message.text))
                bot.send_message(message.chat.id, t('ru', 'delivered'))
            except Exception as e:
                bot.send_message(message.chat.id, t('ru', 'error', error=e))
        else:
            bot.send_message(message.chat.id, t('ru', 'not_found'))