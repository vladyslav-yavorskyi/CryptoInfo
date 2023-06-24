import os
import telebot
from dotenv import load_dotenv
from commands import commands
from crypto import get_crypto_data, make_graph

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)



bot.set_my_commands(commands=commands)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    name = message.from_user.first_name
    bot.send_message(chat_id=message.from_user.id, text=f'Hi, <b>{name}</b>! Are you ready for some <b>CryptoInfo</b>?', parse_mode='HTML')
    bot.send_message(chat_id=message.from_user.id, text='<b>Write the coin to check the price </b>', parse_mode='HTML')



@bot.message_handler(func=lambda msg: True)
def send_crypto_data(message):
    try:
        coin = message.text.upper() + 'USDT'
        get_coin_data = get_crypto_data(coin)
        make_graph(coin, 100)
        bot.send_text_messag
        bot.send_photo(chat_id=message.from_user.id, photo=telebot.types.InputFile('testsave.png'))
        bot.send_message(message.from_user.id,
                     f'Average Price for <b>{coin}</b> is <b>{get_coin_data["price"]}$</b> (for the last <i>{get_coin_data["mins"]}</i> minutes)', parse_mode='HTML')
    except:
        bot.send_message(chat_id=message.from_user.id, text='<b>Something went wrong. Try it again..</b>', parse_mode='HTML')
        bot.send_sticker(message.from_user.id, "CAACAgIAAxkBAAEi1C5klXa16caqdsl_8mr2M2wOJfoiIAACagADwZxgDCHf0XJEvU3QLwQ")


bot.infinity_polling()
