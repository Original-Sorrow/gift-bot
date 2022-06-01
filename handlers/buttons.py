from misc import *
from aiogram import types
import handlers.keyboard as kb
from .functions import *
from config import *








@dp.callback_query_handler(lambda c: c.data == "check_sub")
async def kyp(callback_query: types.CallbackQuery):
    await inline_cheksudb(callback_query)


@dp.callback_query_handler(lambda c: c.data == "menu")
async def kyp(callback_query: types.CallbackQuery):
    user = callback_query.from_user
    refka = bot_link + str(user.id)
    bal=await inline_get_balance(callback_query)
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.send_message(callback_query.message.chat.id,f"Дарите подарки и зарабатывайте\n"
                                                    f"Отправляйте друзьям подарки и зарабатывайте овалюту."
                                                    f"\nВывод на Qiwi станет доступен при накоплении {all_balance} anicoin на суммарном балансе пользователей."
                                                    f"\n\nВаша реферальная ссылка: {refka}"
                                                    f"\n\nВаш баланс: <b>{bal}</b> anicoin 💎\n"
                                                    f"Цена 1 anicoin равна <b>{coast}₽</b>",reply_markup=kb.k1)
