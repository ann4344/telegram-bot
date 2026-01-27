import telebot
from telebot import types
from flask import Flask
import threading
import time
import os

app = Flask(__name__)

TOKEN = "8175867277:AAEQ9i6uKEUA0g34yqGE8-qy8_mw4SkiNLk"
bot = telebot.TeleBot(TOKEN)

# 🛡️ АВТОЗАЩИТА ОТ ДУБЛЕЙ (409 ошибки)
try:
    bot.get_me()
    print("✅ Бот авторизован")
except:
    print("❌ Бот уже запущен где-то ещё")
    exit()

print("🚀 Бот запускается...")

# ХРАНИЛИЩЕ состояний пользователей
user_states = {}

# Flask для Render порта + cron-job.org
@app.route('/')
def home():
    return "Telegram Bot работает! 24/7 с cron-job.org"

# Telegram handlers
@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id
    user_states[chat_id] = "waiting_start_btn"
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_start = types.KeyboardButton('start')
    markup.add(btn_start)
    bot.send_message(chat_id, '👇', reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def handle_all_messages(message):
    chat_id = message.chat.id
    text = message.text
    
    # Новый пользователь → сразу кнопка start
    if chat_id not in user_states:
        handle_start(message)
        user_states[chat_id] = "waiting_start_btn"
        return
    
    # Ждём клик по кнопке "start"
    if user_states[chat_id] == "waiting_start_btn" and text == 'start':
        user_states[chat_id] = "waiting_description"
        
        markup = types.ReplyKeyboardRemove()
        bot.send_message(chat_id, 'Расскажите, с чем вам нужна помощь, или задайте вопрос', reply_markup=markup)
        return
    
    # Ждём описание проекта → "Спасибо!" (ТОЛЬКО 1 РАЗ)
    if user_states[chat_id] == "waiting_description":
        if user_states[chat_id] != "contact_sent":
            bot.send_message(chat_id, '''Спасибо!
Менеджер свяжется с вами здесь ближайшее время
(работаем с 10:00 до 19:00 по МСК).''')
            user_states[chat_id] = "contact_sent"
        return
    
    # После "Спасибо!" → игнорируем ВСЁ
    if user_states.get(chat_id) == "contact_sent":
        return

def run_bot():
    print("✅ Бот запущен! infinity_polling...")
    bot.infinity_polling()

# Запуск Flask + Bot (Render 24/7)
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    threading.Thread(target=run_bot, daemon=True).start()
    app.run(host='0.0.0.0', port=port, debug=False)
