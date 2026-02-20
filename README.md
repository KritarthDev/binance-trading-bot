# Binance Futures Testnet Trading Bot

A simplified Python trading bot that places Market and Limit orders on Binance USDT-M Futures Testnet.

This project was built as part of a technical assessment to demonstrate:

- Clean architecture
- Proper CLI handling
- Structured logging
- Error handling
- Exchange API integration


--------------------------------------------------
FEATURES
--------------------------------------------------

✔ Place MARKET orders  
✔ Place LIMIT orders  
✔ Supports BUY and SELL  
✔ CLI-based user input (argparse)  
✔ Input validation  
✔ Structured modular design  
✔ Logging to file  
✔ Proper exception handling  


--------------------------------------------------
PROJECT STRUCTURE
--------------------------------------------------

trading_bot/
│
├── bot/
│   ├── client.py          # Binance client wrapper
│   ├── orders.py          # Order placement logic
│   ├── validators.py      # Input validation
│   └── logging_config.py  # Logging configuration
│
├── cli.py                 # CLI entry point
├── requirements.txt
├── README.md
└── .env (not committed)


--------------------------------------------------
SETUP INSTRUCTIONS
--------------------------------------------------

1. Clone the repository

2. Create virtual environment

python3 -m venv venv
source venv/bin/activate

3. Install dependencies

pip install -r requirements.txt

4. Create a .env file in the project root:

BINANCE_API_KEY=your_testnet_api_key
BINANCE_API_SECRET=your_testnet_secret_key

⚠ Use Binance Futures Testnet keys:
https://testnet.binancefuture.com


--------------------------------------------------
ADD TEST FUNDS
--------------------------------------------------

Before placing orders:

1. Login to Binance Futures Testnet
2. Go to Wallet
3. Use Faucet to add test USDT


--------------------------------------------------
RUN EXAMPLES
--------------------------------------------------

MARKET Order:

./venv/bin/python cli.py \
--symbol BTCUSDT \
--side BUY \
--type MARKET \
--quantity 0.003


LIMIT Order:

./venv/bin/python cli.py \
--symbol BTCUSDT \
--side SELL \
--type LIMIT \
--quantity 0.003 \
--price 80000


--------------------------------------------------
OUTPUT
--------------------------------------------------

The application prints:

- Order request summary
- Order response details (orderId, status, executedQty, avgPrice)
- Success / failure message

Logs are written to:

trading_bot.log


--------------------------------------------------
ASSUMPTIONS
--------------------------------------------------

- Minimum notional value on Futures is 100 USDT
- Test USDT must be added via faucet
- This application interacts only with Binance Futures Testnet
- No real funds are used


--------------------------------------------------
TECHNOLOGIES USED
--------------------------------------------------

- Python 3.x
- python-binance
- argparse
- python-dotenv
- logging


--------------------------------------------------
FUTURE IMPROVEMENTS
--------------------------------------------------

- Add Stop-Limit / Stop-Market order type
- Add position management
- Add automated strategy execution
- Add unit tests
- Add Docker support

