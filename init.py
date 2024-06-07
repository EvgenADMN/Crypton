from database import Database


def init_bot():
    db = Database()

    bot_token = input('Bot token: ')
    market_api = input('Market API: ')

    db.add_setting('bot_token', bot_token)
    db.add_setting('market_api', market_api)
