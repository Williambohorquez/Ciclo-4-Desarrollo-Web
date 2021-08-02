import sqlite3
from sqlite3 import Error
from flask import g

def conectar():

    if 'db' not in g:
        g.db = sqlite3.connect("static/db/pictic.db")
        g.db.row_factory = sqlite3.Row
    return g.db

def desconectar():
    db = g.pop( 'db', None )

    if db is not None:
        db.close()
