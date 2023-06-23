import os
import telebot
from dotenv import load_dotenv
from crypto import get_crypto_data

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)
base_url = 'https://api.binance.com'


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, 'Hi! Are you ready for some CryptoInfo?')
    bot.send_message(chat_id=message.from_user.id, text='<b>Write the coin to check the price </b>', parse_mode='HTML')


@bot.message_handler(func=lambda msg: True)
def send_crypto_data(message):
    try:
        coin = message.text.upper() + 'USDT'
        get_coin_data = get_crypto_data(coin)
        bot.reply_to(message,
                     f'Average Price for <b>{coin}</b> is <b>{round(float(get_coin_data["price"]),2)}$</b> (for the last <i>{get_coin_data["mins"]}</i> minutes)', parse_mode='HTML')
    except:
        bot.send_message(chat_id=message.from_user.id, text='<b>Something went wrong. Try it again..</b>', parse_mode='HTML')
        bot.send_sticker(message.from_user.id, "CAACAgIAAxkBAAEi1C5klXa16caqdsl_8mr2M2wOJfoiIAACagADwZxgDCHf0XJEvU3QLwQ")


bot.infinity_polling()
