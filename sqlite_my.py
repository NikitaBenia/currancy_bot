import random
import requests
import sqlite3
import os

class BaseDate:
    def __init__(self):
        self.database = sqlite3.connect(os.path.join("data", "database.db"))
        self.cursor = self.database.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Users(
                                user_id INTEGER,
                                login TEXT,
                                password INTEGER,
                                currency TEXT,
                                pricet FLOAT
        )''')
        self.database.commit()

    def insert_user(self, user_id, login, password, currency, pricet):
        self.cursor.execute(f"INSERT INTO Users(user_id, login, password, currency, pricet) VALUES (?, ?, ?, ?, ?)",
                            (user_id, login, password, currency, pricet))
        self.database.commit()
        print('Регистрация прошла успешно!')