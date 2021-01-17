from devtools import debug  # výpis premenný do promptu
from config import PORT, HOST
from fastapi import FastAPI, Request
# from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import time
import requests
import modules.netfunctions as netf
import modules.fuctions as fun

moje_meno = netf.get_hostname()
moje_ip = netf.get_ip()
print('It is', moje_meno, 'My IP address:', moje_ip)
url = "http://dealan.sk/test.php"

db = fun.init_db()

app = FastAPI()

app.mount("/static", StaticFiles(directory="./static"), name="static")
templates = Jinja2Templates(directory="./templates")


# Routes:


@app.get("/")
async def root(request: Request):
    """
    Ukáže merania
    """
    localtime = time.asctime(time.localtime(time.time()))
    # debug(meranie)
    print("/; Čas:", localtime)
    return templates.TemplateResponse("home.html", {"request": request, "time": localtime})


@app.get("/zaznam")
async def zaznam(request: Request):
    """
    zapíše nové zázanamy do DB
    """
    localtime = time.asctime(time.localtime(time.time()))
    print("/; Čas:", localtime)
    return templates.TemplateResponse("zaznam.html", {"request": request, "time": localtime})


@app.get("/graf")
async def graf(request: Request):
    """
    Zobrazí graf nameranej charakteristiky (zatiaľ iba text)
    """
    localtime = time.asctime(time.localtime(time.time()))
    data_z_db = fun.citanie_z_db(db)
    print("Graf; Čas:", localtime)
    return templates.TemplateResponse("graf.html", {"request": request, "data_z_db": data_z_db, "time": localtime})


# Code for running app
if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST,
                port=int(PORT), reload=True, debug=True)
