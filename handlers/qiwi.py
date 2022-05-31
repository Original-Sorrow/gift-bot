from aiogram.dispatcher import FSMContext
from misc import *
import handlers.keyboard as kb
from aiogram import types
from aiogram.utils.markdown import quote_html
from config import *
import re
from .functions import *
import pyqiwi
from aiogram.dispatcher.filters.state import State, StatesGroup




class st(StatesGroup):
	number = State()



wallet = pyqiwi.Wallet(token=qiwi_token, number=qiwi_number)


@dp.message_handler(text=['Вывести средства'])
async def vivod(message: types.Message):
    user= message.from_user
    refka = bot_link + str(user.id)
    alb=await viplata()
    data= await get_rang(message)
    if alb<all_balance:
        await bot.send_message(message.chat.id,f"Вы не можете вывести средства в данный момент так как общий баланс пользователей бота не достиг {all_balance} anicoin.\n"
                                               f"В данный момент он равен {alb} {name_wallet}.\n"
                                               f"Вы можете позвать друзей!Так быстрее наберётся общий баланс!\n"
                                               f"Ваша реферальнаяя ссылка: \n{refka}")
    elif alb>=all_balance:
        balance=float(data[3])*coast
        if balance < 1:
            await bot.send_message(message.chat.id, "Вывод доступен только от одного рубля!!!")
        elif balance >= 1:
            await bot.send_message(message.chat.id,"Введите номер телефона киви(без + ):")
            await st.number.set()


@dp.message_handler(state=st.number)
async def proc(message: types.Message, state: FSMContext):
    user = message.from_user
    number=message.text
    cursor.execute(f'UPDATE users SET number=? WHERE id=?', (number, user.id,))
    conn.commit()
    get = cursor.execute("SELECT balance FROM users WHERE id=?", (user.id,)).fetchone()
    amount = float(get[0])
    get = cursor.execute("SELECT number FROM users WHERE id=?", (user.id,)).fetchone()
    number = int(get[0])
    try:
        wallet.send(pid=99, recipient=number, amount=amount, comment=coment)
        await bot.send_message(message.chat.id,"Средства были успешны зачисленны на ваш номер киви",reply_markup=kb.menu)
    except:
        await bot.send_message(message.chat.id, f"Произошла ошибка проверьте правильность написания номера телефона, если всё верно напишите в поддержку: @{helpme}",reply_markup=kb.menu)
    await state.finish()



