import sqlite_my
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.storage import FSMContext
from dotenv import dotenv_values
import requests
import random
from sqlite_my import *
import asyncio

db = BaseDate()
storage = MemoryStorage()

config = dotenv_values('.env')
bot = Bot(config['key'])
dp = Dispatcher(bot, storage=storage)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, 'Привет! Я бот для получения курса криптовалют.')
    await asyncio.sleep(2)
    await state.set_state(state='login')
    await message.answer('Введи свой логин')

@dp.message_handler(state='login')
async def Login(message: types.Message, state: FSMContext):
    await state.update_data(data={'LogiName': message.text})
    await state.set_state(state='password')
    await message.answer('Введи свой пароль')

@dp.message_handler(state='password')
async def Password(message: types.Message, state: FSMContext):
    await state.update_data(data={'PassInt': int(message.text)})
    await state.set_state(state='currency')
    await message.answer('Введи криптовалюту')

@dp.message_handler(state='currency')
async def Currency(message: types.Message, state: FSMContext):
    await state.update_data(data={'CurrName': message.text})
    await state.set_state(state='currency')
    dataS = await state.get_data()
    url = 'https://api.binance.com/api/v3/ticker/price'
    urlchik = f'{url}?symbol={dataS["CurrName"]}'
    user_id = random.randint(1000, 100000)
    responce = requests.get(urlchik)
    data = responce.json()
    price = float(data["price"])
    price2 = round(price, 2)
    await message.answer(f"Ваш id {user_id}\n"
                         f"Ваш логин {dataS['LogiName']}\n"
                         f"Ваш пароль {dataS['PassInt']}\n"
                         f"Ваша криптовалюта к доллару {dataS['CurrName']}\n"
                         f"Текущий курс {price2}$")
    db_user = db.insert_user(user_id, dataS['LogiName'], dataS['PassInt'], dataS['CurrName'], price2)
    await state.finish()

    # def get_carrancy(symbol):
    #     url = 'https://api.binance.com/api/v3/ticker/price'
    #     urlchik = f'{url}?symbol={symbol}'
    #     responce = requests.get(urlchik)
    #     data = responce.json()
    #     price = float(data["price"])
    #     return round(price, 2)
    #
    # user_id = random.randint(1000, 100000)
    # login = datas['LogiName']
    # password = datas['PassInt']
    # # currency = datas['CurrName']
    #
    # currencyU = get_carrancy('BTCUSDT')
    # Base.BaseDate.insert_user(user_id, login, password, currencyU)