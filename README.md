# KryptoEvidencia 
Evidencia nákupu a predaja rôznych "virtuálnych mien" pre účely daňovej evidencie

Založené na FastAPI knižnici, beží len na lokálnom počítači (http://localhost:8002). Port je možné nastaviť v [config.py](config.py)
Pohyby jednotlivých kryptomien sú zapísané do sqlite databaze, ktorá je automaticky vytvorí v adresári sec, ktorý sa však neprenáša na github...

Každá transakcia umožní uloženie podkladových súborov k evidencii. Napr. pdf faktúry, screenshot z burzy a pod.

Výroz aplikácie - pohyb je samozrejme fiktívny:
![alt text](https://github.com/PavelSimon/KryptoEvidencia/blob/master/KryptoEvidecia.png)