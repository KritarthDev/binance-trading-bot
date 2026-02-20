import argparse
import logging
from bot.client import BinanceFuturesClient
from bot.orders import OrderService
from bot.validators import (
    validate_side,
    validate_order_type,
    validate_quantity,
    validate_price,
)
from bot.logging_config import setup_logging


def main():
    setup_logging()
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser(
        description="Binance Futures Testnet Trading Bot"
    )

    parser.add_argument("--symbol", help="Trading symbol (e.g., BTCUSDT)")
    parser.add_argument("--side", help="BUY or SELL")
    parser.add_argument("--type", help="MARKET or LIMIT")
    parser.add_argument("--quantity", type=float, help="Order quantity")
    parser.add_argument("--stop-loss", type=float, help="Stop loss price")
    parser.add_argument("--take-profit", type=float, help="Take profit price")
 
    parser.add_argument("--price", type=float, help="Price (required for LIMIT)")
    parser.add_argument("--health", action="store_true", help="Check API connectivity")

    args = parser.parse_args()

    try:
        client = BinanceFuturesClient()

        if args.health:
            if client.validate_connection():
                print("✅ API connection healthy.")
            else:
                print("❌ API connection failed.")
            return

        if not all([args.symbol, args.side, args.type, args.quantity]):
            parser.error(
                "For trading mode, --symbol, --side, --type, and --quantity are required."
            )

        side = validate_side(args.side)
        order_type = validate_order_type(args.type)
        quantity = validate_quantity(args.quantity)
        price = validate_price(args.price, order_type)

        print("\nOrder Request Summary:")
        print(f"Symbol: {args.symbol}")
        print(f"Side: {side}")
        print(f"Type: {order_type}")
        print(f"Quantity: {quantity}")
        if order_type == "LIMIT":
            print(f"Price: {price}")

        service = OrderService(client)

        response = service.create_order(
            symbol=args.symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
        )
        response = service.create_order(
            symbol=args.symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
        )

        # Place SL/TP if provided
        if args.stop_loss:
            service.place_stop_loss(
                symbol=args.symbol,
                side=side,
                quantity=quantity,
                stop_price=args.stop_loss,
            )

        if args.take_profit:
            service.place_take_profit(
                symbol=args.symbol,
                side=side,
                quantity=quantity,
                target_price=args.take_profit,
            )


        print("\nOrder Response:")
        print(f"Order ID: {response.get('orderId')}")
        print(f"Status: {response.get('status')}")
        print(f"Executed Quantity: {response.get('executedQty')}")
        print(f"Avg Price: {response.get('avgPrice', 'N/A')}")

        print("\n✅ Order placed successfully!")

    except Exception as e:
        logger.error(str(e))
        print(f"\n❌ Error: {str(e)}")


if __name__ == "__main__":
    main()

