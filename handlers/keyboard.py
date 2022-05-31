from aiogram import types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from config import *


link="https://t.me/"+channel
link1="https://t.me/"+channel_info
link2="https://t.me/"+chat



k1 = types.InlineKeyboardMarkup()
obnovit = types.InlineKeyboardButton('Обновить баланс.', callback_data='check_bal')
knopka_info = types.InlineKeyboardButton('Инфо.', url=link1)
knopka_chata = types.InlineKeyboardButton('Чат.', url=link2)
k1 = k1.add(obnovit).row(knopka_info,knopka_chata)

podpiska = types.InlineKeyboardMarkup()
knopka_kanala = types.InlineKeyboardButton('Канал', url=link)
proverka = types.InlineKeyboardButton('Проверить подписку', callback_data='check_sub')
podpisochka = podpiska.add(knopka_kanala).add(proverka)



menu = types.InlineKeyboardMarkup()
gl_menu = types.InlineKeyboardButton('Главное меню.', callback_data='menu')
menu = menu.add(gl_menu)



no_inl = types.ReplyKeyboardMarkup(resize_keyboard=True)
no_inl.add(types.KeyboardButton('Вывести средства'))
