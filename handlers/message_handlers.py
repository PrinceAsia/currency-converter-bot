from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from config import currencies, CBU_URL


message_router = Router()


# When user send only sum (digits) bot will convert this sum to USD, EUR, RUBLE
@message_router.message(F.text.isdigit())
async def exchange_handler(message: Message):
    # print(message.text, message.from_user.username, message.from_user.first_name)
    x = int(message.text)
    s = f"{x} sums: \n"
    s += f"\t- {x / currencies['USD']['rate']: .2f} US dollars\n"
    s += f"\t- {x / currencies['EUR']['rate']: .2f} Euros\n"
    s += f"\t- {x / currencies['RUB']['rate']: .2f} Russian rubles\n\n"
    s += f"Currency rates fetched from <a href='{CBU_URL}'>CBU API</a>"
    await message.reply(
        text=s,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text='Source',
                        url=CBU_URL
                    )
                ]
            ]
        )
    )
