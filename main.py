import sqlite_my
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.storage import FSMContext
from dotenv import dotenv_values
import requests
import random
from keyboards import choose
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
    await message.answer('Выберите что вы хотите сделать', reply_markup=choose)

##########   УЗНАТЬ КУРС
@dp.callback_query_handler(lambda c: c.data == 'kurs')
async def kurs(message: types.Message, state: FSMContext):
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

##########   УЗНАТЬ ЦЕНУ
@dp.callback_query_handler(lambda c: c.data == 'sale')
async def sale(message: types.Message, state: FSMContext):
    await state.set_state(state='login_sale')
    await message.answer('Введи свой логин')

@dp.message_handler(state='login_sale')
async def LoginSale(message: types.Message, state: FSMContext):
    await state.update_data(data={'LogiNameSale': message.text})
    await state.set_state(state='password_sale')
    await message.answer('Введи свой пароль')

@dp.message_handler(state='password_sale')
async def PasswordSale(message: types.Message, state: FSMContext):
    await state.update_data(data={'PassIntSale': int(message.text)})
    await state.set_state(state='currency_sale')
    await message.answer('Введи криптовалюту')

@dp.message_handler(state='currency_sale')
async def CountSales(message: types.Message, state: FSMContext):
    await state.update_data(data={'CurrNameSale': message.text})
    await state.set_state(state='count_sale')
    await message.answer('Введите сколько вы хотите приобрести валюты')

@dp.message_handler(state='count_sale')
async def Currency(message: types.Message, state: FSMContext):
    await state.update_data(data={'CountSale': int(message.text)})
    await state.set_state(state='count_sales')
    dataSale = await state.get_data()
    url_sale = 'https://api.binance.com/api/v3/ticker/price'
    urlchik_sale = f'{url_sale}?symbol={dataSale["CurrNameSale"]}'
    user_id_sale = random.randint(1000, 100000)
    responce = requests.get(urlchik_sale)
    datas = responce.json()
    prices = round(float(datas['price']), 2)
    sale = float(dataSale["CountSale"] * prices)
    sale2 = sale
    await message.answer(f"Ваш id {user_id_sale}\n"
                         f"Ваш логин {dataSale['LogiNameSale']}\n"
                         f"Ваш пароль {dataSale['PassIntSale']}\n"
                         f"{dataSale['CountSale']} {dataSale['CurrNameSale']} будет стоить: {sale2}$")
    db_user = db.insert_user_sale(user_id_sale, dataSale['LogiNameSale'], dataSale['PassIntSale'], dataSale['CurrNameSale'], dataSale['CountSale'], sale2)
    await state.finish()