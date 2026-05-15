import telebot
from config import GROUP_ID
from database import save_message, get_user_lang, set_user_lang
from locales import ru, en

LOCALES = {'ru': ru.texts, 'en': en.texts}

def t(lang, key, **kwargs):
    text = LOCALES.get(lang, LOCALES['ru']).get(key, LOCALES['ru'][key])
    return text.format(**kwargs) if kwargs else text

def register(bot: telebot.TeleBot):

    @bot.message_handler(commands=['start'])
    def start(message):
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(
            telebot.types.InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
            telebot.types.InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
        )
        bot.send_message(message.chat.id, t('ru', 'choose_lang'), reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
    def set_lang(call):
        lang = call.data.split('_')[1]
        set_user_lang(call.from_user.id, lang)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
        bot.send_message(call.message.chat.id, t(lang, 'welcome', name=call.from_user.first_name))

    @bot.message_handler(func=lambda message: message.chat.type == 'private')
    def forward_to_group(message):
        username = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name
        user_id = message.from_user.id
        lang = get_user_lang(user_id)

        sent = bot.send_message(
            GROUP_ID,
            t('ru', 'new_message', username=username, user_id=user_id, text=message.text)
        )

        save_message(user_id, username, sent.message_id)
        bot.send_message(message.chat.id, t(lang, 'accepted'))