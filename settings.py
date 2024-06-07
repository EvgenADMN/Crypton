from database import Database

BOT_TOKEN = Database().get_setting('bot_token')
USERS = Database().get_users()
WHITELIST = Database().get_whitelist()
URL = Database().get_setting('market_api')