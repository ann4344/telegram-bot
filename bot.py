import telebot
from telebot import types
TOKEN = "8175867277:AAEQ9i6uKEUA0g34yqGE8-qy8_mw4SkiNLk"  # ← ВАШ ТОКЕН!
bot = telebot.TeleBot(TOKEN)
print("🚀 Бот запускается...")
@bot.message_handler(commands=['start'])
def handle_start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_start = types.KeyboardButton('start')
    markup.add(btn_start)
    bot.send_message(message.chat.id, 'Нажмите кнопку start', reply_markup=markup)
@bot.message_handler(func=lambda m: m.text == 'start')
def handle_start_btn(message):
    markup = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, 'Опишите ваш проект или задачу в свободной форме.', reply_markup=markup)
@bot.message_handler(func=lambda m: m.text != 'start' and not m.text.startswith('/'))
def handle_description(message):
    bot.reply_to(message, '''Спасибо!
Менеджер свяжется с вами здесь ближайшее время
(работаем с 10:00 до 19:00 по МСК).''')
print("✅ Бот запущен!")
bot.infinity_polling()
