import sqlite3
from devtools import debug
from pydantic import BaseModel


class KryptoData(BaseModel):
    datum: str
    mena: int
    smer: int
    kolko: float
    zaKolko: float
    poznamka: str


class KryptoOutput(KryptoData):
    pass


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


db = init_db()


def zapis_do_db(db, value):
    cursor = db.cursor()
    debug(value.datum)
    sql = "INSERT INTO evidencia VALUES (?,?,?, '1' ,?,?,?)"
    print(sql)
    try:
        cursor.execute(sql, (value.smer, value.kolko, value.zaKolko,
                             value.mena, value.poznamka, value.datum))
        db.commit()
    except sqlite3.Error as e:
        print("Error:", e.args[0])
    return db.total_changes


def citanie_z_db(db):
    cursor = db.cursor()
    vystup = ""
    try:
        sql = "SELECT rowid, * FROM mena"
        cursor.execute(sql)
        vystup = cursor.fetchall()
    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])
    debug(vystup)
    return vystup


def citaj_pouzite_meny(db):
    cursor = db.cursor()
    vystup = ""
    try:
        sql = "SELECT rowid, * FROM mena"
        cursor.execute(sql)
        vystup = cursor.fetchall()
    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])
    # print(vystup)
    return vystup


def citaj_evidencia(db):
    cursor = db.cursor()
    vystup = ""
    try:
        # sum(case when smer like 'IN' then +kolko else -kolko end)
        sql = "select smer, kolko, za_kolko, uid, mena.skratka, cas_zmeny, poznamka, (za_kolko / kolko), balance  from evidencia inner join mena on evidencia.mena_id = mena.rowid"
        cursor.execute(sql)
        vystup = cursor.fetchall()
    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])
    debug(vystup)
    return vystup


def zapisKryptoDoDb(krypto):
    debug(krypto)
    datum = krypto.datum
    print(datum)
    zapis_do_db(db, krypto)
    return krypto
