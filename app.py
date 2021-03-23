import telebot

from config import TOKEN, keys
from extentions import ConvertionExeption, Exchange


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands = ['start', 'help'])
def start(message):
    text = f"Привет, {message.chat.username}! \nЧтобы воспользоваться ботом, напиши в таком порядке:\n\n<имя валюты цену которой хочешь узнать> <имя валюты, в которую нужно перевести> <количество первой валюты>\n\n Должно получиться примерно так: эфириум доллары 1 \n\nЧтобы посмотреть список всех доступных валют, просто нажми /values"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands = ['values'])
def values(message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = '\n- '.join((text, key))
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types = ['text'])
def convert(message):
    try:
        values = message.text.lower().split(" ")

        if len(values) != 3:
            raise ConvertionExeption("Слишком много параметров")

        quote, base, amount = values
        total_base = Exchange.get_price(quote, base, amount)

    except ConvertionExeption as e:
        bot.send_message(message.chat.id, f"Ошибка пользователя.\n{e}")
    except Exception as e:
        bot.send_message(message.chat.id, f"Не удалось обработать команду.\n{e}")
    else:
        text = f"Цена {amount} {quote} в {base} - {total_base}"
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)

