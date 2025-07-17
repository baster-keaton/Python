# 📊 Monitor de Arbitraje de Criptomonedas en Tiempo Real
Este proyecto permite escanear múltiples exchanges públicos cada 5 minutos, mostrar cotizaciones BTC/USDT en una web y detectar automáticamente oportunidades de arbitraje entre plataformas. Incluye una alerta opcional por Telegram.

## 🚀 Funcionalidades

- ✅ Escaneo de precios en tiempo real desde Binance, OKX, KuCoin, Coinbase, Bybit, Bitget y Kraken  
- ⏱️ Actualización automática cada 5 minutos  
- 💰 Detección de oportunidades de arbitraje entre exchanges  
- 🔔 Notificación por Telegram con spread positivo  
- 🌐 Visualización web con tabla interactiva y tema oscuro

---

## 🧰 Tecnologías utilizadas

- Python 3.10+
- Flask + APScheduler
- Asyncio + httpx
- Bootstrap + DataTables
- Systemd (ejecución como servicio en Linux)
- Telegram Bot (opcional)

---

## 📁 Estructura de archivos

```bash
crypto-arbitrage/
├── app.py                  # Servidor web con Flask
├── exchanges.py            # Consultas y parseo de precios por exchange
├── scheduler_module.py     # Actualización periódica + detección de arbitraje
├── .env                    # Token y chat ID de Telegram (si se usa)
├── requirements.txt        # Dependencias del proyecto
├── templates/
│   └── dashboard.html      # Frontend HTML (modo oscuro)
└── README.md               # Este archivo
```

---

## Endpoints públicos y normalización
   
Exchange	Endpoint público (ticker)	Formato de símbolo

    Binance	https://api.binance.com/api/v3/ticker/bookTicker?symbol=BTCUSDT	BTCUSDT
    OKX	https://www.okx.com/api/v5/market/books?instId=BTC-USDT	BTC-USDT
    KuCoin	https://api.kucoin.com/api/v1/market/orderbook/level1?symbol=BTC-USDT	BTC-USDT
    Coinbase	https://api.exchange.coinbase.com/products/BTC-USD/book?level=1	BTC-USD
    Bybit	https://api.bybit.com/v2/public/tickers?symbol=BTCUSDT	BTCUSDT
    Bitget	https://api.bitget.com/api/spot/v1/market/depth?symbol=BTCUSDT&limit=5	BTCUSDT
    Kraken	https://api.kraken.com/0/public/Ticker?pair=BTCUSD	XBTUSD (Kraken usa)

## 1. plan detallado y el esqueleto de código para:

Monitorizar Binance, OKX, KuCoin, Coinbase, Bybit, Bitget y Kraken
Consultar solo órdenes públicas cada 5 min
Detectar y notificar automáticamente oportunidades de arbitraje
Almacenar únicamente las últimas cotizaciones
Correr en tu servidor Linux ya configurado

  Estructura del proyecto
  crypto-arbitrage/
  
    ├── app.py                    # Servidor web con Flask
    ├── exchanges.py              # Módulo que consulta precios en APIs de exchanges
    ├── scheduler_module.py       # Scheduler + detección de arbitraje + notificaciones
    ├── .env                      # Variables de entorno (token de Telegram, etc.)
    ├── templates/
    │   └── dashboard.html        # HTML para la visualización de precios
    ├── static/                   # (Opcional) Archivos CSS o JS personalizados
    ├── requirements.txt          # Dependencias del proyecto
    └── README.md                 # Explicación del proyecto y uso



## 2. 🛠️ Instalación: Dependencias y entorno en linux

### Clonar el repo
    git clone https://github.com/<TU_USUARIO>/<TU_REPOSITORIO>.git
    cd crypto-arbitrage

### Crear y activar virtualenv
    python3 -m venv venv
    source venv/bin/activate

### Instalar librerías
    pip install httpx asyncio flask apscheduler python-dotenv

## 3. 🔐 Configuración opcional de Telegram
Crea un bot en BotFather

Copia el token

Obtén tu chat_id con este bot: userinfobot

Crea archivo .env con:

    TELEGRAM_TOKEN=tu_token_aqui
    TELEGRAM_CHAT_ID=tu_chatid_aqui

## 4. 🧪 Ejecución manual para pruebas
Para probar el servidor sin systemd:

    source venv/bin/activate
    python app.py

#### Luego accede vía navegador: http://localhost:8000/ o http://"TU-IP-SERVIDOR":8000/


## 🧩 Ejecución como servicio en Linux
Crear archivo /etc/systemd/system/arbitrage.service con:

    [Unit]
    Description=Servicio de Arbitraje Crypto
    After=network.target

    [Service]
    User=ubuntu
    WorkingDirectory=/home/ubuntu/crypto-arbitrage
    ExecStart=/home/ubuntu/crypto-arbitrage/venv/bin/python app.py
    Restart=always
    Environment="PYTHONUNBUFFERED=1"

    [Install]
    WantedBy=multi-user.target

Activar el servicio

    sudo systemctl daemon-reload
    sudo systemctl enable arbitrage
    sudo systemctl start arbitrage

Verificar estado

    sudo systemctl status arbitrage.service
    sudo systemctl status arbitrage

## 🔍 Visualización web
Una vez activo, accede desde tu navegador:

      http://<TU-IP-EC2>:8000/

Si usas Amazon EC2, asegúrate de abrir el puerto 8000 en el grupo de seguridad.

## 🧪 Tests y validación
Cada exchange tiene manejo de errores propio

En caso de fallos (rate limit, caída de API), los datos se ignoran temporalmente sin romper el flujo

Las respuestas se muestran como 0.0 si no se pudieron obtener correctamente

## 🛡️ Consideraciones de seguridad
No se almacenan API keys ni cotizaciones históricas

Sólo se consultan endpoints públicos

Si deseas integrar trading real, debes añadir autenticación por exchange y validaciones adicionales

## ❤️ Créditos
Desarrollado con pasión por monitorear los mercados descentralizados y buscar oportunidades justas 💰⚡



