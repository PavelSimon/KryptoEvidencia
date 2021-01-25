from devtools import debug  # výpis premenný do promptu
from config import PORT, HOST
from fastapi import FastAPI, Request, Form
from typing import Optional
# from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import time
# import requests
import modules.netfunctions as netf
import modules.fuctions as fun

moje_meno = netf.get_hostname()
moje_ip = netf.get_ip()
print('It is', moje_meno, 'My IP address:', moje_ip)

app = FastAPI()

app.mount("/static", StaticFiles(directory="./static"), name="static")
templates = Jinja2Templates(directory="./templates")


# Routes:


@app.get("/")
async def root(request: Request):
    """
    Ukáže zoznam zaevidovaných kryptomien
    """
    krypto = fun.citaj_evidencia(fun.db)
    localtime = time.asctime(time.localtime(time.time()))
    print("/; Čas:", localtime)
    return templates.TemplateResponse("home.html", {"request": request, "time": localtime, "krypto": krypto})


@app.get("/edit/{item_id}")
async def editZaznamGet(item_id: int, request: Request):
    """
    zobrazí edit okno na zmenu zázanamu v DB
    """
    meny = fun.citaj_pouzite_meny(fun.db)
    localtime = time.asctime(time.localtime(time.time()))
    print("/edit/{item_id}; Čas:", localtime)
    # debug(item_id)
    riadky = fun.citaj_evidencia_zaznam(fun.db, item_id)
    # debug(riadky)
    result: fun.KryptoData = fun.KryptoData
    for riadok in riadky:
        result.smer = riadok[0]
        result.kolko = riadok[1]
        result.zaKolko = riadok[2]
        result.kto = 1
        result.mena = 1
        result.datum = riadok[5]
        result.poznamka = riadok[6]
        result.zostatok = riadok[8]
        result.rowid = riadok[9]
    return templates.TemplateResponse('edit.html', context={'request': request, "item_id": item_id, "time": localtime, 'result': result, "meny": meny})
    # return templates.TemplateResponse('edit.html', context={'request': request, "item_id": item_id, "time": localtime, "meny": meny, 'result': result})


@ app.post("/edit/")
async def editZaznamPost(request: Request, datum: str = Form(...), mena: int = Form(...), smer: str = Form(...), kolko: float = Form(...), zaKolko: float = Form(...), zostatok: float = Form(...), poznamka: Optional[str] = Form(...), rowid: int = Form(...)):
    meny = fun.citaj_pouzite_meny(fun.db)
    localtime = time.asctime(time.localtime(time.time()))
    print("POST:/zaznam; Čas:", localtime)
    result: fun.KryptoData = fun.KryptoData
    result.datum = datum
    result.mena = mena
    result.smer = smer
    result.kolko = kolko
    result.zaKolko = zaKolko
    result.poznamka = poznamka
    result.zostatok = zostatok
    result.rowid = rowid
    fun.upravKryptoVDb(result)
    item_id = 1
    # return templates.TemplateResponse('edit.html', context={'request': request, "time": localtime,  "meny": meny, 'result': result})
    return templates.TemplateResponse('edit.html', context={'request': request, "item_id": item_id, "time": localtime, 'result': result, "meny": meny})


@ app.get("/zaznam")
async def zaznam(request: Request):
    """
    zobrazí zápis nového zázanamu do DB
    """
    meny = fun.citaj_pouzite_meny(fun.db)
    localtime = time.asctime(time.localtime(time.time()))
    print("/zaznam; Čas:", localtime)
    result: fun.KryptoData = fun.KryptoData
    return templates.TemplateResponse("zaznam.html", {"request": request, "time": localtime, "meny": meny, 'result': result})


@ app.post("/zaznam")
async def zaznamPost(request: Request, datum: str = Form(...), mena: int = Form(...), smer: str = Form(...), kolko: float = Form(...), zaKolko: float = Form(...), zostatok: float = Form(...), poznamka: Optional[str] = Form(...)):
    meny = fun.citaj_pouzite_meny(fun.db)
    localtime = time.asctime(time.localtime(time.time()))
    print("POST:/zaznam; Čas:", localtime)
    result: fun.KryptoData = fun.KryptoData
    result.datum = datum
    result.mena = mena
    result.smer = smer
    result.kolko = kolko
    result.zaKolko = zaKolko
    result.poznamka = poznamka
    result.zostatok = zostatok
    fun.zapisKryptoDoDb(result)
    return templates.TemplateResponse('zaznam.html', context={'request': request, "time": localtime,  "meny": meny, 'result': result})


@ app.get("/graf")
async def graf(request: Request):
    """
    Zobrazí graf nameranej charakteristiky (zatiaľ iba text)
    """
    localtime = time.asctime(time.localtime(time.time()))
    data_z_db = fun.citaj_evidencia(fun.db)
    print("/Graf; Čas:", localtime)
    return templates.TemplateResponse("graf.html", {"request": request, "data_z_db": data_z_db, "time": localtime})


# Code for running app
if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST,
                port=int(PORT), reload=True, debug=True)
