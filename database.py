import sqlite3


class Database:
    """
    Класс для работы с базой данных SQLITE3.
    Основные методы:
        help() - для вывода подробной информации
        add_user(username, telegram_id) - добавить пользователя в таблицу Users
    """

    def __init__(self):
        self.connection = sqlite3.connect("crypton.db")
        self.cursor = self.connection.cursor()

        self.cursor.execute('CREATE TABLE IF NOT EXISTS Users '
                            '(ID INTEGER PRIMARY KEY, name VARCHAR(50), tg_id)')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS Settings '
                            '(ID INTEGER PRIMARY KEY, name VARCHAR(50), value VARCHAR(200))')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS BuyCrypto '
                            '(ID INTEGER PRIMARY KEY, user INT, amount FLOAT, price FLOAT,'
                            'FOREIGN KEY (user) REFERENCES Users (ID))')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS LastPrice '
                            '(ID INTEGER PRIMARY KEY, user INT, price FLOAT,'
                            'FOREIGN KEY (user) REFERENCES Users (ID))')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS UserStatus '
                            '(ID INTEGER PRIMARY KEY, user INT, status VARCHAR(50), value BOOL,'
                            'FOREIGN KEY (user) REFERENCES Users (ID))')

        self.connection.commit()

    def about(self):
        print('''
            Database().add_many_users({'Evgen': 437565880, 'Merk': 745579373})
        ''')

    def add_setting(self, name: str, value: str):
        self.cursor.execute(f'INSERT INTO Settings (name, value) VALUES (\'{name}\', \'{value}\')')
        self.connection.commit()

    def get_setting(self, name):
        setting = self.cursor.execute(f'SELECT value FROM Settings WHERE name=\'{name}\'')
        result = setting.fetchall()
        if result:
            return result[0][0]

    def set_status(self, user: int, status: str, value: bool):
        has_record = self.cursor.execute(f'SELECT * FROM UserStatus '
                                        f'WHERE user={user} AND status={status}').fetchall()
        if not has_record:
            self.cursor.execute(f'INSERT INTO UserStatus (user, status, value) '
                                f'VALUES ({user}, {status}, {value})')
        else:
            self.cursor.execute(f'UPDATE UserStatus SET value={value}'
                                f'WHERE user={user} AND status={status}')

    def add_user(self, username: str, telegram_id: int):
        self.cursor.execute(f'INSERT INTO Users (name, tg_id) VALUES (\'{username}\', {telegram_id})')
        self.connection.commit()

    def add_many_users(self, users_dict: dict):
        for username, telegram_id in users_dict.items():
            self.cursor.execute(f"INSERT INTO Users (name, tg_id) VALUES ('{username}', {telegram_id})")
        self.connection.commit()

    def get_users(self):
        users = self.cursor.execute('SELECT name, tg_id FROM Users')
        return dict(users.fetchall())

    def get_whitelist(self):
        users = self.cursor.execute('SELECT tg_id FROM Users')
        return list(tg_id[0] for tg_id in users.fetchall())

    def set_last_price(self, tg_id: int, price: float):
        user_id = self.cursor.execute(f'SELECT ID FROM Users WHERE tg_id={tg_id}').fetchall()[0][0]
        has_record = self.cursor.execute(f'SELECT * FROM LastPrice '
                                        f'WHERE user={user_id}').fetchall()
        if not has_record:
            self.cursor.execute(f'INSERT INTO LastPrice (user, price) VALUES ({user_id}, {price})')
            self.connection.commit()
            return
        self.cursor.execute(f'UPDATE LastPrice SET price={price} WHERE user={user_id}')
        self.connection.commit()

    def get_last_price(self, tg_id):
        user_id = self.cursor.execute(f'SELECT ID FROM Users WHERE tg_id={tg_id}').fetchall()[0][0]
        last_price = self.cursor.execute(f'SELECT price FROM LastPrice WHERE user={user_id}').fetchall()
        if not last_price:
            return False
        return last_price[0][0]



    def buy_coin(self, user: int, amount: float, price: float):
        self.cursor.execute(f'INSERT INTO BuyCrypto (user, amount, price) VALUES ({user}, {amount}, {price})')
        self.connection.commit()
