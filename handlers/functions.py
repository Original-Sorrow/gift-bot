import random
from misc import *
from aiogram.types import Message
from aiogram import types
from config import *
import handlers.keyboard as kb


async def get_rang(message: types.Message):
    user = message.from_user
    cursor.execute("SELECT * FROM users WHERE id=?", (user.id,))
    data = cursor.fetchone()
    return data
#занесение в бд    

#получение баланса             
async def get_balance(message: types.Message):
    try:
        user = message.from_user
        get = cursor.execute("SELECT balance FROM users WHERE id=?", (user.id,)).fetchall()
        balance = f"{str(get[0][0])}"
        return balance
    except: pass


async def inline_get_balance(callback_query: types.CallbackQuery):
    try:
        user = callback_query.from_user
        get = cursor.execute("SELECT balance FROM users WHERE id=?", (user.id,)).fetchall()
        balance = f"{str(get[0][0])}"
        return balance
    except: pass

async def get_len_users(message: types.Message):

    users = cursor.execute("SELECT id FROM users").fetchall()

    allusers = len(users)

    return allusers

async def get_bonus(message: types.Message,referal):
    user = message.from_user
    data = await get_rang(message)
    if data[4] == 0:
        balance=random.random()*0.01
        bal=round(balance,5)
        cursor.execute(f'UPDATE users SET balance=? WHERE id=?', (bal, user.id,))
        cursor.execute(f'UPDATE users SET reg=? WHERE id=?', (1, user.id,))
        get = cursor.execute("SELECT balance FROM users WHERE id=?", (referal,)).fetchone()
        oldbalance = float(get[0])
        newbalance=oldbalance+bal
        cursor.execute(f'UPDATE users SET balance=? WHERE id=?', (newbalance, referal,))
        conn.commit()
        await bot.send_message(message.chat.id, f"Вы получили бонус {bal} {name_wallet}",reply_markup=kb.menu)
        await bot.send_message(referal, f"Вы получили {bal} {name_wallet} за вашего реферала.", reply_markup=kb.menu)

async def cheksudb(message: types.Message,referal):
    user = message.from_user
    user_channel_status = await bot.get_chat_member(chat_id=channel_id, user_id=user.id)
    if user_channel_status["status"] != 'left':
        return await get_bonus(message,referal)
    else:
        return await bot.send_message(message.chat.id, 'Для работы с ботом необходимо подписаться на канал!',reply_markup=kb.podpisochka)


async def inline_get_rang(callback_query: types.CallbackQuery):
    user = callback_query.from_user
    cursor.execute("SELECT * FROM users WHERE id=?", (user.id,))
    data = cursor.fetchone()
    return data




async def inline_get_bonus(callback_query: types.CallbackQuery,referal):
    user = callback_query.from_user
    data = await inline_get_rang(callback_query)
    if data[4] == 0:
        balance=random.random()*0.01
        bal=round(balance,5)
        cursor.execute(f'UPDATE users SET balance=? WHERE id=?', (bal, user.id,))
        cursor.execute(f'UPDATE users SET reg=? WHERE id=?', (1, user.id,))
        get = cursor.execute("SELECT balance FROM users WHERE id=?", (referal,)).fetchone()
        oldbalance = float(get[0])
        newbalance = oldbalance + bal
        cursor.execute(f'UPDATE users SET balance=? WHERE id=?', (newbalance, referal,))
        conn.commit()
        await bot.send_message(callback_query.message.chat.id, f"Вы получили бонус {bal} {name_wallet}.", reply_markup=kb.menu)
        await bot.send_message(referal, f"Вы получили {bal} {name_wallet} за вашего реферала.", reply_markup=kb.menu)




async def inline_cheksudb(callback_query: types.CallbackQuery,referal):
    user = callback_query.from_user
    user_channel_status = await bot.get_chat_member(chat_id=channel_id, user_id=user.id)
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    if user_channel_status["status"] != 'left':
        return await inline_get_bonus(callback_query,referal)
    else:
        return await bot.send_message(callback_query.message.chat.id, 'Для работы с ботом необходимо подписаться на канал!',
                                      reply_markup=kb.podpisochka)

async def viplata():
    get = cursor.execute("SELECT balance FROM users").fetchall()
    all_balanc=0
    for x in get:
        all_balanc=float(x[0])+all_balanc
    return round(all_balanc,5)



