# -*- coding: utf-8 -*-
from telebot.types import *

# -- Start Keyboard -- #
Start = ReplyKeyboardMarkup(row_width=2,resize_keyboard=True)
nuovaEntrataBtn = KeyboardButton("➕ Entrata")
nuovaUscitaBtn = KeyboardButton("➖ Uscita")
bilancioBtn = KeyboardButton("💵 Bilancio")
Start.row(nuovaEntrataBtn,nuovaUscitaBtn)
Start.row(bilancioBtn)

# -- Prezzo Keyboard -- #
Prezzo = ReplyKeyboardMarkup(row_width=3,resize_keyboard=True,one_time_keyboard=True)
unoBtn = KeyboardButton("1,00")
cinqueBtn = KeyboardButton("5,00")
dieciBtn = KeyboardButton("10,00")
ventiBtn = KeyboardButton("20,00")
cinquantaBtn = KeyboardButton("50,00")
cancelBtn = KeyboardButton("/cancel")
Prezzo.row(unoBtn,cinqueBtn)
Prezzo.row(dieciBtn,ventiBtn)
Prezzo.row(cinquantaBtn)
Prezzo.row(cancelBtn)

# -- Bilancio Keyboard -- #
Bilancio = InlineKeyboardMarkup(row_width=1)
precBtn = InlineKeyboardButton(text="⬅️ Prec",callback_data="prec")
nextBtn = InlineKeyboardButton(text="Next ➡️",callback_data="next")
Bilancio.row(precBtn,nextBtn)

# -- Cancel Keyboard -- #
Cancel = ReplyKeyboardMarkup(row_width=1,resize_keyboard=True,one_time_keyboard=True)
cancelBtn = KeyboardButton("/cancel")
Cancel.row(cancelBtn)
