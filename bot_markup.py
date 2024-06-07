import telebot


def markup_buttons():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    buttons = ['💲 Узнать стоимость Notcoin',
               '💵 Покупка NotCoin',
               '🔔 Оповещение при достижении цены']

    for button in buttons:
        markup.add(button)

    return markup
