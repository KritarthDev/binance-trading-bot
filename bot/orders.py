import logging
import time
from binance.exceptions import BinanceAPIException

logger = logging.getLogger(__name__)


class OrderService:
    def __init__(self, client):
        self.client = client

    def create_order(self, symbol, side, order_type, quantity, price=None):
        max_retries = 3

        for attempt in range(max_retries):
            try:
                order_params = {
                    "symbol": symbol,
                    "side": side,
                    "type": order_type,
                    "quantity": quantity,
                    "newOrderRespType": "RESULT"
                }

                if order_type == "LIMIT":
                    order_params["price"] = price
                    order_params["timeInForce"] = "GTC"

                logger.info(f"Placing order: {order_params}")

                response = self.client.place_order(**order_params)

                logger.info(f"Order response: {response}")
                return response

            except BinanceAPIException as e:
                self._handle_api_error(e)
                raise

            except Exception:
                logger.warning(f"Network issue. Retry {attempt+1}/{max_retries}")
                time.sleep(2 ** attempt)

        raise Exception("Max retries exceeded.")

    def place_stop_loss(self, symbol, side, quantity, stop_price):
        current_price = self.get_mark_price(symbol)

        if side == "BUY" and stop_price >= current_price:
            raise ValueError("Stop loss must be BELOW current price for LONG.")

        if side == "SELL" and stop_price <= current_price:
            raise ValueError("Stop loss must be ABOVE current price for SHORT.")

        opposite_side = "SELL" if side == "BUY" else "BUY"

        params = {
            "symbol": symbol,
            "side": opposite_side,
            "type": "STOP_MARKET",
            "stopPrice": stop_price,
            "quantity": quantity,
            "reduceOnly": True,
        }

        logger.info(f"Placing Stop Loss: {params}")
        return self.client.place_order(**params)

    def place_take_profit(self, symbol, side, quantity, target_price):
        current_price = self.get_mark_price(symbol)

        if side == "BUY" and target_price <= current_price:
            raise ValueError("Take profit must be ABOVE current price for LONG.")

        if side == "SELL" and target_price >= current_price:
            raise ValueError("Take profit must be BELOW current price for SHORT.")

        opposite_side = "SELL" if side == "BUY" else "BUY"

        params = {
            "symbol": symbol,
            "side": opposite_side,
            "type": "TAKE_PROFIT_MARKET",
            "stopPrice": target_price,
            "quantity": quantity,
            "reduceOnly": True,
        }

        logger.info(f"Placing Take Profit: {params}")
        return self.client.place_order(**params)

    def get_mark_price(self, symbol):
        data = self.client.client.futures_mark_price(symbol=symbol)
        return float(data["markPrice"])

    def _handle_api_error(self, e):
        if e.code == -2015:
            logger.error("Invalid API key.")
        elif e.code == -2019:
            logger.error("Insufficient margin.")
        elif e.code == -4164:
            logger.error("Order notional must be >= 100 USDT.")
        elif e.code == -2021:
            logger.error("Order would immediately trigger.")
        else:
            logger.error(f"Binance API error: {e.message}")











