import ccxt
import datetime
from typing import List, TypedDict


class BinanceExchange:
    def __init__(self, config: dict):
        self.__exchange = ccxt.binance(config)

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

    async def fetch_ohlcv(
        self,
        symbol: str,
        timeframe="1m",
        since: int | None = None,
        limit: int | None = None,
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
            }
            for data in response
        ]

        return data_set


class OHLCVData(TypedDict):
    timestamp: str
    open: float
    high: float
    low: float
    close: float
    volume: float


OHLCVDataSet = List[OHLCVData]
