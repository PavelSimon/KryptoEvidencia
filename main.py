from devtools import debug  # výpis premenný do promptu
from config import PORT, HOST
from fastapi import FastAPI, Request, Form
from typing import Optional
# from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import time
#import requests
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
    # debug(krypto)
    localtime = time.asctime(time.localtime(time.time()))
    # debug(meranie)
    print("/; Čas:", localtime)
    return templates.TemplateResponse("home.html", {"request": request, "time": localtime, "krypto": krypto})


@app.get("/zaznam")
async def zaznam(request: Request):
    """
    zobrazí zápis nového zázanamu do DB
    """
    meny = fun.citaj_pouzite_meny(fun.db)
    localtime = time.asctime(time.localtime(time.time()))
    print("/zaznam; Čas:", localtime)
    result: fun.KryptoData = fun.KryptoData
    return templates.TemplateResponse("zaznam.html", {"request": request, "time": localtime, "meny": meny, 'result': result})


@app.post("/zaznam")
async def zaznamPost(request: Request, datum: str = Form(...), mena: int = Form(...), smer: str = Form(...), kolko: float = Form(...), zaKolko: float = Form(...), poznamka: Optional[str] = Form(...)):
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
    fun.zapisKryptoDoDb(result)
    return templates.TemplateResponse('zaznam.html', context={'request': request, "time": localtime,  "meny": meny, 'result': result})


@app.get("/zaznam/{param}")
async def zaznam(request: Request, param: str, q: Optional[str] = None):
    """
    zapíše nové zázanamy do DB
    """
    parametre = {"param": param}
    debug(q)
    if q:
        debug(q)
        parametre.update({"q": q})
    debug(parametre)
    query_str = request['query_string']
    debug(query_str)
    meny = fun.citaj_pouzite_meny(fun.db)
    localtime = time.asctime(time.localtime(time.time()))
    print("/zaznam/{param}; Čas:", localtime)
    return templates.TemplateResponse("zaznam.html", {"request": request, "time": localtime, "meny": meny})


@app.get("/graf")
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
