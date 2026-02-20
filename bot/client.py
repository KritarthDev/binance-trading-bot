import os
from pathlib import Path
from binance.client import Client
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv


# Explicitly load .env from project root
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


class BinanceFuturesClient:
    def __init__(self):
        api_key = os.getenv("BINANCE_API_KEY")
        api_secret = os.getenv("BINANCE_API_SECRET")

        if not api_key or not api_secret:
            raise ValueError("API credentials not found in environment variables")

        self.client = Client(api_key, api_secret, testnet=True)

    def place_order(self, **params):
        return self.client.futures_create_order(**params)

    def validate_connection(self):
        try:
            self.client.futures_account()
            return True
        except BinanceAPIException:
            return False
        except Exception:
            return False

