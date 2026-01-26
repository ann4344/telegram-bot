import telebot
from telebot import types
from flask import Flask
import threading
import time
import os

app = Flask(__name__)

TOKEN = "8175867277:AAEQ9i6uKEUA0g34yqGE8-qy8_mw4SkiNLk"
bot = telebot.TeleBot(TOKEN)

print("🚀 Бот запускается...")

# Flask для Render порта
@app.route('/')
def home():
    return "Telegram Bot работает!"

# Telegram handlers
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

def run_bot():
    print("✅ Бот запущен!")
    bot.infinity_polling()

# Запуск Flask + Bot
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    threading.Thread(target=run_bot, daemon=True).start()
    app.run(host='0.0.0.0', port=port)
