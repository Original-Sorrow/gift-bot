from misc import *
import handlers.keyboard as kb
from aiogram import types
from aiogram.utils.markdown import quote_html
import random
from config import *
import re
from .functions import *

@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    referal=message.get_args()
    user = message.from_user
    data = await get_rang(message)
    refka = bot_link + str(user.id)
    bal=await get_balance(message)
    allb=await viplata()
    await bot.send_message(message.chat.id,"Привет!",reply_markup=kb.no_inl)
    if data is None:
        cursor.execute(f"INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)",(user.id, 0, 0, 0, 0, 0))
        conn.commit()
        if referal is not None:
            await cheksudb(message, referal)
        else:
            await cheksudb(message)
    elif data[4] == 0:
        if referal is not None:
            await cheksudb(message, referal)
        else:
            await cheksudb(message)
    elif data[4] == 1:
        await bot.send_message(message.chat.id, f"Дарите подарки и зарабатывайте\n"
                                                f"Отправляйте друзьям подарки и зарабатывайте валюту."
                                                f"\nВывод на Qiwi станет доступен при накоплении {all_balance} anicoin на суммарном балансе пользователей."
                                                f"\n\nВаша реферальная ссылка: {refka}"
                                                f"\n\nВаш баланс: <b>{bal}</b> anicoin 💎\n"
                                                f"Цена 1 anicoin равна <b>{coast}₽</b>\n"
                                                f"Общий баланс равен: {allb} {name_wallet}",reply_markup=kb.k1)



@dp.message_handler(commands=['rsl'])
async def cmd_rsl(message: types.Message):
    user = message.from_user
    args = message.get_args()
    data = await get_rang(message)
    if data[1] == 1:
        if not args:
            await message.reply("Укажи аргументы.")
        else:
            chats = cursor.execute("SELECT user_id FROM users").fetchall()
            otp = 0
            notp=0
            for x in chats:
                try:
                    chat = await bot.get_chat(str(x[0]))
                    await bot.send_message(chat.id, args)
                    otp = otp + 1
                except:
                    notp=notp+1
            await message.reply(f"Рассылка успешна!\n\nТекст рассылки:\n{args}\n\nОтправленно {otp} юзерам\nНе отправлено {notp} юзерам")

@dp.message_handler(commands=['botinfo'])
@dp.throttled(rate=5)
async def cmd_botinfo(message: types.Message):
    user = message.from_user
    users = await get_len_users(message)
    await message.reply(f"<b>Информация о базе данных бота:</b>\n\n"
                            f"Зарегистрированных пользователей: <code>{users}</code>\n")

