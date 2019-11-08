# -*- coding: utf-8 -*-

import sqlite3
from os.path import isfile
from os import remove

# Specifica il file del database
databaseFile = "Database.db"

# Se esiste il vecchio database
if(isfile(databaseFile)):
    # Lo cancella
    remove(databaseFile)

# Si connette al database, se non esite lo crea
DB = sqlite3.connect(databaseFile)
# Crea un cursore per interagire con il database
Cursor = DB.cursor()

# Esegue la query per creare la tabella LISTINO
# +----------------- SOLDI -----------------+
# | DATA | TIPO | SOLDI | DESCRIZIONE       |
# +-----------------------------------------+
Cursor.execute("CREATE TABLE SOLDI (ID INTEGER PRIMARY KEY, DATA TEXT NOT NULL, TIPO TEXT NOT NULL, PREZZO FLOAT NOT NULL, DESCRIZIONE TEXT NOT NULL)")

# Scrive le modifiche su file
DB.commit()
# Chiude la connessione con il DB
DB.close()

# Stampa questa frase, quindi esce
print("Database creato con successo!")
