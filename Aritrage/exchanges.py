import asyncio
import httpx

EXCHANGES = {
    "binance":  "https://api.binance.com/api/v3/ticker/bookTicker?symbol=BTCUSDT",
    "okx":      "https://www.okx.com/api/v5/market/books?instId=BTC-USDT",
    "kucoin":   "https://api.kucoin.com/api/v1/market/orderbook/level1?symbol=BTC-USDT",
    "coinbase": "https://api.exchange.coinbase.com/products/BTC-USD/book?level=1",
#    "bybit":    "https://api.bybit.com/v2/public/tickers?symbol=BTCUSDT",
    "bybit":    "https://api.bybit.com/v5/market/tickers?category=spot&symbol=BTCUSDT",
    "bitget":   "https://api.bitget.com/api/spot/v1/market/depth?symbol=BTCUSDT&limit=1",
    "kraken":   "https://api.kraken.com/0/public/Ticker?pair=XBTUSD"
}


async def fetch_price(client: httpx.AsyncClient, name: str, url: str) -> dict:
    # 1) Primer bloque: solicitud y parseo bruto
    try:
        resp = await client.get(url, timeout=10)
        if resp.status_code != 200:
            raise ValueError(f"{name}: HTTP {resp.status_code}")
        if not resp.content:
            raise ValueError(f"{name}: respuesta vacía")
        data = resp.json()
    except Exception as e:
        print(f"[Error fetch {name}]: {e}")
        return {"exchange": name, "bid": 0.0, "ask": 0.0}

    # 2) Segundo bloque: lógica específica de parsing
    try:
        if name == "binance":
            bid = float(data.get("bidPrice", 0.0))
            ask = float(data.get("askPrice", 0.0))

        elif name == "okx":
            d = data.get("data", [{}])[0]
            bids = d.get("bids", [[0,0]])[0]
            asks = d.get("asks", [[0,0]])[0]
            bid, ask = float(bids[0]), float(asks[0])

        elif name == "kucoin":
            d = data.get("data", {})
            bid = float(d.get("bestBid", 0.0))
            ask = float(d.get("bestAsk", 0.0))

        elif name == "coinbase":
            bids = data.get("bids", [[0,0]])[0]
            asks = data.get("asks", [[0,0]])[0]
            bid, ask = float(bids[0]), float(asks[0])

        elif name == "bitget":
            d = data.get("data", {})
            # Si data es lista, tomo el primer elemento
            if isinstance(d, list):
                d = d[0]
            bids = d.get("bids") or d.get("bid") or [[0.0, 0.0]]
            asks = d.get("asks") or d.get("ask") or [[0.0, 0.0]]
            bid, ask = float(bids[0][0]), float(asks[0][0])

        elif name == "bybit":
            r = data.get("result")
            # V2 devuelve lista, V5 puede devolver dict con bid1Price/ask1Price
            if isinstance(r, dict):
                r = [r]
            if not isinstance(r, list) or not r:
                raise ValueError("bybit: result vacío")
            item = r[0]
            bid = float(item.get("bid_price", item.get("bid1Price", 0.0)))
            ask = float(item.get("ask_price", item.get("ask1Price", 0.0)))

        elif name == "kraken":
            res = data.get("result", {})
            key = next(iter(res), None)
            if not key:
                raise ValueError("kraken: clave de par ausente")
            d = res[key]
            bid = float(d.get("b", [0.0])[0])
            ask = float(d.get("a", [0.0])[0])

        else:
            raise ValueError(f"{name}: parsing no definido")

        return {"exchange": name, "bid": bid, "ask": ask}

    except Exception as e:
        print(f"[Error parse {name}]: {e}\nRESPUESTA RAW: {data}")
        return {"exchange": name, "bid": 0.0, "ask": 0.0}


async def fetch_all() -> list[dict]:
    async with httpx.AsyncClient() as client:
        tasks = [fetch_price(client, name, url) for name, url in EXCHANGES.items()]
        return await asyncio.gather(*tasks)

