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
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Sales(
                                user_id_sale INTEGER,
                                login_sale TEXT,
                                password_sale INTEGER,
                                currency_sale TEXT,
                                count_sale INTEGER,
                                salet FLOAT
        )''')
        self.database.commit()

    def insert_user(self, user_id, login, password, currency, pricet):
        self.cursor.execute(f"INSERT INTO Users(user_id, login, password, currency, pricet) VALUES (?, ?, ?, ?, ?)",
                            (user_id, login, password, currency, pricet))
        self.database.commit()

    def insert_user_sale(self, user_id_sale, login_sale, password_sale, currency_sale, count_sale, salet):
        self.cursor.execute(f"INSERT INTO Sales(user_id_sale, login_sale, password_sale, currency_sale, count_sale, salet) VALUES (?, ?, ?, ?, ?, ?)",
                            (user_id_sale, login_sale, password_sale, currency_sale, count_sale, salet))
        self.database.commit()