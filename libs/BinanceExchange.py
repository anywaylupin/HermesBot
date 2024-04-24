import ccxt
import datetime
from ccxt.base.types import OrderSide
from typing import List, Literal, TypedDict


type OHLCVDataSet = List[OHLCVData]
type FairValueGap = Literal["bullish", "bearish"]


class OHLCVData(TypedDict):
    timestamp: str
    open: float
    high: float
    low: float
    close: float
    volume: float
    trend: FairValueGap | None


class BinanceExchange:
    def __init__(self, config: dict):
        self.__exchange = ccxt.binance(config)

    def set_sandbox_mode(self, enable: bool):
        self.__exchange.set_sandbox_mode(enable)

    def fetch_balance(self, symbol: str):
        """
        Fetches the balance for the specified cryptocurrency symbol.

        Args:
            symbol: The cryptocurrency symbol.

        Returns:
            The balance information.
        """
        balance = self.__exchange.fetch_balance()
        return balance.get(symbol)

    def fetch_currencies(self):
        """
        Fetches the list of available cryptocurrencies in the user's account.

        Returns:
            A list of available cryptocurrency symbols.
        """
        info = self.fetch_balance("info")
        balances = info.get("balances")  # type: ignore
        return [balance["asset"] for balance in balances]  # type: ignore

    def fetch_ohlcv(
        self,
        symbol: str,
        timeframe="1m",
        since: int | None = None,
        limit: int = 5,
        params={},
    ):
        response = self.__exchange.fetch_ohlcv(symbol, timeframe, since, limit, params)

        data_set: OHLCVDataSet = [
            {
                "timestamp": datetime.datetime.now().isoformat(),
                "open": data[0],
                "high": data[1],
                "low": data[2],
                "close": data[3],
                "volume": data[4],
                "trend": get_trend(data[0], data[3]),
            }
            for data in response
        ]

        return data_set

    def create_market_order(
        self,
        symbol: str,
        side: OrderSide,
        amount: float,
        price: int | None = None,
        params={},
    ):
        response = self.__exchange.create_market_order(
            symbol, side, amount, price, params
        )

        return response


def get_trend(o: float, c: float) -> FairValueGap | None:
    if o > c:
        return "bearish"
    elif o < c:
        return "bullish"
    else:
        return None
