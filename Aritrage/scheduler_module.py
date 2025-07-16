import os
import asyncio
from apscheduler.schedulers.background import BackgroundScheduler
from exchanges import fetch_all
import httpx
from dotenv import load_dotenv

load_dotenv()  # Carga TELEGRAM_TOKEN, TELEGRAM_CHAT_ID de .env

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

latest_prices: list[dict] = []
_last_alert = None

async def notify_telegram(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    async with httpx.AsyncClient() as client:
        await client.post(url, json=payload)

def detect_and_notify(prices: list[dict]):
    global _last_alert
    # Determina mejor bid y mejor ask
    best_bid = max(prices, key=lambda x: x["bid"])
    best_ask = min(prices, key=lambda x: x["ask"])
    spread = best_bid["bid"] - best_ask["ask"]

    # Umbral mínimo
    if spread > 10 and _last_alert != (best_ask["exchange"], best_bid["exchange"]):
        msg = (
            f"Arbitraje:\n"
            f"Comprar en {best_ask['exchange']}: {best_ask['ask']}\n"
            f"Vender en {best_bid['exchange']}: {best_bid['bid']}\n"
            f"Spread: {spread:.2f} USD"
        )
        asyncio.run(notify_telegram(msg))
        _last_alert = (best_ask["exchange"], best_bid["exchange"])

def update_cycle():
    global latest_prices
    prices = asyncio.run(fetch_all())
    latest_prices = prices
    detect_and_notify(prices)

# Inicializa y programa cada 5 minutos
update_cycle()
scheduler = BackgroundScheduler()
scheduler.add_job(update_cycle, "interval", minutes=5)
scheduler.start()

