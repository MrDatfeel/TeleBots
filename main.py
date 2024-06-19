
import telebot
import requests
import json




TOKEN = "7332221211:AAFwB3ZNuDMU6x9YLFrmGRaF0oJN1Ibsy_8"        #ТОКЕН


bot = telebot.TeleBot(TOKEN)


keys = {                                                         #СЛОВАРЬ, ГДЕ ХРАНЯТСЯ ВАЛЮТЫ
    "евро": "EUR",
    "доллар": "USD",
    "рубль": "RUB",
}


class APIException(Exception):
    pass

class APIConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException(f"Невозможно перевести одинаковые валюты {base}.")

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f"Не удалось обработать валюту {quote}.")

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f"Не удалось обработать валюту {base}.")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Не удалось обработать количество {amount}.")

        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}")
        total_base = json.loads(r.content)[keys[base]]

        return total_base


@bot.message_handler(commands=["start", "help"])
def help(message: telebot.types.Message):
    text = "Чтобы начать работу с данным ботом введите команду в следующем формате:\n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\nУвидеть список всех доступных валют: /values"
    bot.reply_to(message, text)


@bot.message_handler(commands=["values"])                #ОБРАБОТЧИК, ВАЛЮТА
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = "\n".join((text,key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=["text", ])           #ОБРАБОТЧИК, ОСНОВНОЙ
def convert(message: telebot.types.Message):
    values = message.text.split(" ")

    if len(values) != 3:
        raise APIException("Не верные параметры.")

    quote, base, amount = values
    total_base = APIConverter.convert(quote, base, amount)

    text = f"цена {amount} {quote} в {base} - {total_base}"
    bot.send_message(message.chat.id, text)


bot.polling()