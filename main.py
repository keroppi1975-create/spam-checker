from fastapi import FastAPI
import httpx
from bs4 import BeautifulSoup

app = FastAPI()

@app.get("/")
async def root():
    return {"messaggio": "Spam Checker API funziona! ✅"}

@app.get("/check/{numero}")
async def check_numero(numero: str):
    risultato = await cerca_su_tellows(numero)
    return {
        "numero": numero,
        "tipo": risultato["tipo"],
        "score": risultato["score"],
        "commenti": risultato["commenti"],
        "fonte": "tellows.it"
    }

async def cerca_su_tellows(numero: str):
    url = f"https://www.tellows.it/num/{numero}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        score_tag = soup.find("span", {"class": "h1"})
        score = int(score_tag.text.strip()) if score_tag else 5
        commenti_tag = soup.find("span", {"itemprop": "reviewCount"})
        commenti = int(commenti_tag.text.strip()) if commenti_tag else 0
        if score >= 7:
            tipo = "SPAM"
        elif score >= 5:
            tipo = "SOSPETTO"
        elif score <= 3:
            tipo = "SICURO"
        else:
            tipo = "SCONOSCIUTO"
        return {"tipo": tipo, "score": score, "commenti": commenti}
    except Exception as e:
        return {"tipo": "ERRORE", "score": 0, "commenti": 0}