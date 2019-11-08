# -*- coding: utf-8 -*-
import telebot, logging, urllib, os, sqlite3, string
import keyboard, statements
from os.path import isfile
from re import search

# Imposto un logger di eventi
logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

# Token del bot
API_TOKEN = ''
# Creo l'oggetto bot inizializzato con il token
bot = telebot.TeleBot(API_TOKEN)

currentMoneyData = {
	'tipo' : '',
	'soldi' : '',
	'descrizione' : ''
}

# File del database
databaseFile = "Database.db"

if not isfile(databaseFile):
	print("Missing database!")
	exit(-1)

# Handler per il comando start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id,statements.IT.Start.replace("{}",message.from_user.first_name),reply_markup=keyboard.Start,parse_mode='markdown')

# Handler per il comando cancel
# 	: rimuove i dati in memoria e ricomincia da zero
@bot.message_handler(commands=['cancel'])
def cancel(message):
	for key in currentMoneyData:
		currentMoneyData[key] = ''

# Handler per il tasto 'Entrata'
@bot.message_handler(func=lambda message: message.text == '➕ Entrata')
def entrata(message):
	currentMoneyData['tipo'] = 'Entrata'
	msg = bot.send_message(message.from_user.id,statements.IT.SoldiNuovaEntrata,reply_markup=keyboard.Prezzo,parse_mode='markdown')
	bot.register_next_step_handler(msg, soldiNuovaEntrata)

def soldiNuovaEntrata(message):
	if message.text == '/cancel':
		bot.send_message(message.from_user.id,statements.IT.OperazioneAnnullata,reply_markup=keyboard.Start,parse_mode='markdown')
		return
	if search(r"^[0-9]{1,9}(\,|.|$)[0-9]{0,2}(€){0,1}$", message.text):
		currentMoneyData['soldi'] = message.text
		msg = bot.send_message(message.from_user.id,statements.IT.DescrizioneNuovaEntrata,reply_markup=keyboard.Cancel,parse_mode='markdown')
		bot.register_next_step_handler(msg, descrizioneNuovaEntrata)
	else:
		msg = bot.send_message(message.from_user.id,"Formato errato.")
		bot.register_next_step_handler(msg,soldiNuovaEntrata)

def descrizioneNuovaEntrata(message):
	if message.text == '/cancel':
		bot.send_message(message.from_user.id,statements.IT.OperazioneAnnullata,reply_markup=keyboard.Start,parse_mode='markdown')
		return
	currentMoneyData['descrizione'] = message.text
	DB = sqlite3.connect(databaseFile)
	c = DB.cursor()
	c.execute("INSERT INTO SOLDI(DATA,TIPO,PREZZO,DESCRIZIONE) VALUES(CURRENT_TIMESTAMP,?,?,?)",[currentMoneyData['tipo'],currentMoneyData['soldi'],currentMoneyData['descrizione']])
	DB.commit()
	DB.close()
	for key in currentMoneyData:
		currentMoneyData[key] = ''
	bot.send_message(message.from_user.id,statements.IT.NuovaEntrataSalvata,reply_markup=keyboard.Start,parse_mode='markdown')

# Handler per il tasto 'Uscita'
@bot.message_handler(func=lambda message: message.text == '➖ Uscita')
def uscita(message):
	currentMoneyData['tipo'] = 'Uscita'
	msg = bot.send_message(message.from_user.id,statements.IT.SoldiNuovaUscita,reply_markup=keyboard.Prezzo,parse_mode='markdown')
	bot.register_next_step_handler(msg, soldiNuovaUscita)

def soldiNuovaUscita(message):
	if message.text == '/cancel':
		bot.send_message(message.from_user.id,statements.IT.OperazioneAnnullata,reply_markup=keyboard.Start,parse_mode='markdown')
		return
	currentMoneyData['soldi'] = message.text
	msg = bot.send_message(message.from_user.id,statements.IT.DescrizioneNuovaUscita,reply_markup=keyboard.Cancel,parse_mode='markdown')
	bot.register_next_step_handler(msg, descrizioneNuovaUscita)

def descrizioneNuovaUscita(message):
	if message.text == '/cancel':
		bot.send_message(message.from_user.id,statements.IT.OperazioneAnnullata,reply_markup=keyboard.Start,parse_mode='markdown')
		return
	currentMoneyData['descrizione'] = message.text
	DB = sqlite3.connect(databaseFile)
	c = DB.cursor()
	c.execute("INSERT INTO SOLDI(DATA,TIPO,PREZZO,DESCRIZIONE) VALUES(CURRENT_TIMESTAMP,?,?,?)",[currentMoneyData['tipo'],currentMoneyData['soldi'],currentMoneyData['descrizione']])
	DB.commit()
	DB.close()
	for key in currentMoneyData:
		currentMoneyData[key] = ''
	bot.send_message(message.from_user.id,statements.IT.NuovaUscitaSalvata,reply_markup=keyboard.Start,parse_mode='markdown')

# Handler per il tasto 'Bilancio'
@bot.message_handler(func=lambda message: message.text == '💵 Bilancio')
def bilancioHandler(message):
	pagina = bilancio(0)
	if pagina:
		bot.send_message(message.from_user.id,pagina,reply_markup=keyboard.Bilancio,parse_mode='markdown')
	else:
		bot.send_message(message.from_user.id,statements.IT.NessunaTransazione,parse_mode='markdown')

def bilancio(pagina):
    DB = sqlite3.connect("Database.db")
    c = DB.cursor()
    inf = pagina * 3
    # LIMIT INT_1,INT_2
    #   INT_1 = INDICE DA DOVE PARTIRE
    #   INT_2 = QUANTE RIGHE SELEZIONARE
    c.execute("SELECT * FROM SOLDI ORDER BY DATA DESC LIMIT ?, 3 ",[inf])
    result = c.fetchall()
    if len(result) == 0:
        return None
    message = "🔖 Pagina: *" + str(pagina) + "*\n\n"    
    for row in result:
        message += "⏳ Data: *" + str(row[1]) + "*\n"
        if str(row[2]) == 'Entrata':
            message += "➕ Tipo: *" + str(row[2]) + "*\n"
        else:
            message += "➖ Tipo: *" + str(row[2]) + "*\n"            
        message += "💵 Soldi: *" + str(row[3]) + "€*\n"
        message += "📌 Nome: *" + str(row[4]) + "*\n"
        message += "\n\n"
    return message

@bot.callback_query_handler(func=lambda call: call.data == 'prec')
def prec(message):
	text = message.message.text.split("\n")
	row = text[0].split(":")
	numeroPagina = int(row[1][1:]) - 1
	if numeroPagina < 0:
		bot.answer_callback_query(message.id,statements.IT.NoRecordPrecedenti)
	else:
		nuovaPagina = bilancio(int(numeroPagina))
		if nuovaPagina:
			bot.edit_message_text(nuovaPagina,message.from_user.id,message.message.message_id,reply_markup=keyboard.Bilancio,parse_mode='markdown')
		else:
			bot.answer_callback_query(message.id,statements.IT.NoRecordSuccessivi)		
			

@bot.callback_query_handler(func=lambda call: call.data == 'next')
def next(message):
	text = message.message.text.split("\n")
	row = text[0].split(":")
	numeroPagina = int(row[1][1:]) + 1
	nuovaPagina = bilancio(int(numeroPagina))
	if nuovaPagina:
		bot.edit_message_text(nuovaPagina,message.from_user.id,message.message.message_id,reply_markup=keyboard.Bilancio,parse_mode='markdown')
	else:
		bot.answer_callback_query(message.id,statements.IT.NoRecordSuccessivi)		

bot.polling()