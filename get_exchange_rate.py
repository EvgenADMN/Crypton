import requests


def get_rate():
    url = 'https://www.floatrates.com/daily/usd.json'
    return requests.get(url).json()['rub']['rate']


def get_balance_value():
    rate = get_rate()
