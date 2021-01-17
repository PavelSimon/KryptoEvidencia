import sqlite3


def init_db():
    db = sqlite3.connect('sec/krypto.db')
    cursor = db.cursor()
    sql = "CREATE TABLE IF NOT EXISTS evidencia (smer TEXT NOT NULL, kolko REAL, za_kolko REAL, uid INTEGER, mena_id INTEGER, poznamka TEXT, cas_zmeny TEXT NOT NULL)"
    try:
        cursor.execute(sql)
    except sqlite3.Error as e:
        print("Error:", e.args[0])
    sql = "CREATE TABLE IF NOT EXISTS mena (skratka TEXT NOT NULL, nazov TEXT NOT NULL)"
    try:
        cursor.execute(sql)
    except sqlite3.Error as e:
        print("Error:", e.args[0])
    sql = "CREATE TABLE IF NOT EXISTS user (username TEXT NOT NULL, meno TEXT, priezvisko TEXT, mail TEXT NOT NULL)"
    try:
        cursor.execute(sql)
    except sqlite3.Error as e:
        print("Error:", e.args[0])

    return db


def zapis_do_db(db, value):
    cursor = db.cursor()
    """sql = "INSERT INTO meranie VALUES (?,'poznámka', datetime('now', 'localtime'))"
    try:
        cursor.execute(sql, (value0.value))
        db.commit()
    except sqlite3.Error as e:
        print("Error:", e.args[0])
    return db.total_changes"""


def citanie_z_db(db):
    cursor = db.cursor()
    vystup = ""
    try:
        sql = "SELECT rowid, * FROM evidencia"
        cursor.execute(sql)
        vystup = cursor.fetchall()
    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])
    return vystup
