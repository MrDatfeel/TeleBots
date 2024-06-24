import telebot
from telebot import types
import random
import datetime

TOKEN = '7332680265:AAEzyNzZ4m5yC87QoasWk3tXBt1mWynD4XM'  # Замените на ваш токен
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    flip_button = types.InlineKeyboardButton(text="Бросить монету", callback_data='flip')
    markup.add(flip_button)
    bot.send_message(message.chat.id, "Привет! Нажми на кнопку, чтобы подбросить монету.", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == 'flip':
        result = random.choice(['Орел', 'Решка'])
        markup = types.InlineKeyboardMarkup()
        flip_button = types.InlineKeyboardButton(text="Бросить повторно", callback_data='flip')
        markup.add(flip_button)
        # Добавляем время броска для уникальности сообщения
        time_now = datetime.datetime.now().strftime('%H:%M:%S')
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f"Выпало: {result}\nПоследний бросок: {time_now}", reply_markup=markup)


bot.polling(none_stop=True)



