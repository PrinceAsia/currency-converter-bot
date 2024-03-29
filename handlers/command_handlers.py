import requests
from aiogram import Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import CommandStart, Command
from aiogram.utils.chat_action import ChatActionSender

from config import currencies, CBU_URL


command_router = Router()


# This handler works when user send command /start
@command_router.message(CommandStart())
async def start_handler(message: Message):
    s = "Welcome to our <b>currency converter bot</b>\n"
    s += "For more information send /help command!"
    await message.answer(text=s, reply_markup=ReplyKeyboardRemove())


# This handler work for /help command & will show all commands and descriptions
@command_router.message(Command('help', prefix='!/#'))
async def help_handler(message: Message):
    s = "For using this bot use these commands:\n\n"
    s += "/courses - for get all courses\n"
    s += "/usd - for get USD course\n"
    s += "/eur - for get EURO course\n"
    s += "/ruble - for get Russian ruble course\n\n"

    s += "If you want to convert any sum, send sum (only digits)"

    await message.reply(text=s)


# When user send /courses command bot will return USD, EUR, RUB courses in UZS
@command_router.message(Command('courses', prefix='!/#'))
async def courses_handler(message: Message):
    async with ChatActionSender.typing(bot=message.bot, chat_id=message.from_user.id):
        response = requests.get(CBU_URL)

        s = "Today's currency rates:\n\n"

        for course in response.json():
            if course['Ccy'] in currencies.keys():
                currencies[course['Ccy']]['rate'] = course['Rate']
                s += f"\t- 1 {course['CcyNm_EN']} is {course['Rate']} sums\n"
        s += '\n\n'
        await message.answer(text=s)


# When user send /usd command bot will return USD course in UZS
@command_router.message(Command('usd', prefix='!/#'))
async def usd_handler(message: Message):
    response = requests.get(f"{CBU_URL}USD/")
    res = response.json()[0]
    s = f"1 {res['CcyNm_EN']} = {res['Rate']} sums"
    await message.reply(s)


# When user send /eur command bot will return EUR course in UZS
@command_router.message(Command('eur', prefix='!/#'))
async def eur_handler(message: Message):
    response = requests.get(f"{CBU_URL}EUR/")
    res = response.json()[0]
    s = f"1 {res['CcyNm_EN']} = {res['Rate']} sums"
    await message.reply(s)


# When user send /rub command bot will return RUBLE course in UZS
@command_router.message(Command('ruble', prefix='!/#'))
async def ruble_handler(message: Message):
    response = requests.get(f"{CBU_URL}RUB/")
    res = response.json()[0]
    s = f"1 {res['CcyNm_EN']} = {res['Rate']} sums"
    await message.reply(s)
