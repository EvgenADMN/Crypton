import time
import requests
import telebot
from log import log
from database import Database
from telebot import types
from init import init_bot
from settings import BOT_TOKEN, WHITELIST, USERS, URL
from get_exchange_rate import get_rate
from bot_markup import markup_buttons

def main():
    bot = telebot.TeleBot(BOT_TOKEN)
    markup = markup_buttons()

    @bot.message_handler(commands=['start'])
    def start(message):
        if message.chat.id not in WHITELIST:
            return
        bot.send_message(message.chat.id, "Привет, бро", reply_markup=markup)

    @bot.message_handler(content_types=['text'])
    def message_handler(message):
        user_id = message.chat.id
        if user_id not in WHITELIST:
            return

        database = Database()

        if 'Узнать стоимость' in message.text:
            log(f'{message.chat.first_name} узнал цену')
            price = float(requests.get(URL).json()['result']['list'][0]['lastPrice'])
            last_price = database.get_last_price(user_id)
            if not last_price:
                database.set_last_price(user_id, price)
                bot.send_message(user_id, f'Цена NotCoin: {price} USDT', reply_markup=markup)
                return

            percent = round(abs(last_price - price) / (last_price / 100), 2)
            if price > last_price:
                addict_text = f'▲ {percent}%'
            elif price < last_price:
                addict_text = f'▼ {percent}%'
            else:
                addict_text = '0%'

            database.set_last_price(user_id, price)
            bot.send_message(user_id, f'Цена NotCoin: {price} USDT ({addict_text})', reply_markup=markup)
        elif 'Покупка' in message.text:
            bot.send_message(user_id, 'В разработке', reply_markup=markup)
        elif 'Оповещение при достижении цены' in message.text:
            bot.send_message(user_id, 'В разработке', reply_markup=markup)

    bot.infinity_polling()


if __name__ == '__main__':
    if BOT_TOKEN is None:
        init_bot()
    while True:
        try:
            main()
        except Exception as exc:
            log(exc)
            time.sleep(5)
