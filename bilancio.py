# -*- coding: utf-8 -*-

import sqlite3

def bilancio(pagina):
    DB = sqlite3.connect("Database.db")
    c = DB.cursor()
    inf = pagina * 3
    # LIMIT INT_1,INT_2
    #   INT_1 = INDICE DA DOVE PARTIRE
    #   INT_2 = QUANTE RIGHE SELEZIONARE
    c.execute("SELECT * FROM SOLDI LIMIT ?, 3 ",[inf])
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