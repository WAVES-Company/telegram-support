from telebot import TeleBot
from config import BOT_TOKEN
from database import init_db
from handlers import user, moderator

bot = TeleBot(BOT_TOKEN)

init_db()
user.register(bot)
moderator.register(bot)

bot.remove_webhook()
bot.polling(non_stop=True)