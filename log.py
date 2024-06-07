import datetime


def log(text):
    now = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    with open('log.txt', 'a')as file:
        file.write(f'{now} -> {text}\n')
