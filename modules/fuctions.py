import sqlite3
from devtools import debug
from pydantic import BaseModel


class KryptoData(BaseModel):
    datum: str
    mena: int
    smer: int
    kolko: float
    zaKolko: float
    kto: int
    poznamka: str
    zostatok: float
    rowid: int
    kurz: float


class KryptoOutput(KryptoData):
    pass


def init_db():
    db = sqlite3.connect('sec/krypto.db')
    cursor = db.cursor()
    sql = "CREATE TABLE IF NOT EXISTS evidencia (smer TEXT NOT NULL, kolko REAL, za_kolko REAL, uid INTEGER, mena_id INTEGER, poznamka TEXT, cas_zmeny TEXT NOT NULL, balance)"
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
    sql = "INSERT INTO evidencia VALUES (?,?,?, '1' ,?,?,?,?)"
    print(sql)
    try:
        cursor.execute(sql, (value.smer, value.kolko, value.zaKolko,
                             value.mena, value.poznamka, value.datum, value.zostatok))
        db.commit()
    except sqlite3.Error as e:
        print("Error:", e.args[0])
    return db.total_changes


def uprav_v_db(db, value):
    cursor = db.cursor()
    debug(value.rowid)
    sql = "update evidencia set smer = ?, kolko = ?, za_kolko = ?, uid = 1, mena_id = 1, cas_zmeny = ?, poznamka  = ?, balance  = ? where rowid  = ?"
    print(sql)
    try:
        cursor.execute(sql, (value.smer, value.kolko, value.zaKolko,
                             value.datum, value.poznamka, value.zostatok, value.rowid))
        db.commit()
    except sqlite3.Error as e:
        print("Error:", e.args[0])
    return db.total_changes
    # return "vykonal som"


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
    # debug(vystup)
    return vystup


def citaj_evidencia(db):
    cursor = db.cursor()
    vystup = ""
    try:
        sql = "select smer, kolko, za_kolko, uid, mena.skratka, cas_zmeny, poznamka, round((za_kolko / kolko), 2), balance, evidencia.rowid from evidencia inner join mena on evidencia.mena_id = mena.rowid"
        cursor.execute(sql)
        vystup = cursor.fetchall()
    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])
    return vystup


def citaj_evidencia_zaznam(db, id: int):
    rowid = id
    cursor = db.cursor()
    vystup = ""
    sql = "select smer, kolko, za_kolko, uid, mena.skratka, cas_zmeny, poznamka, (za_kolko / kolko), balance, evidencia.rowid from evidencia inner join mena on evidencia.mena_id = mena.rowid where evidencia.rowid = ?"
    try:
        cursor.execute(sql, (rowid,))
        vystup = cursor.fetchall()
    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])
    return vystup


def zapisKryptoDoDb(krypto):
    datum = krypto.datum
    print(datum)
    zapis_do_db(db, krypto)
    return krypto


def upravKryptoVDb(krypto):
    datum = krypto.datum
    print(datum)
    uprav_v_db(db, krypto)
    return krypto
