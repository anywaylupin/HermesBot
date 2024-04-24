from .BinanceExchange import get_trend, OHLCVData


class Candle:
    def __init__(self, ohlcv: OHLCVData):
        if ohlcv is not None:
            self.__O = ohlcv["open"]
            self.__H = ohlcv["high"]
            self.__L = ohlcv["low"]
            self.__C = ohlcv["close"]
            self.__timestamp = ohlcv["timestamp"]

            try:
                self.__trend = ohlcv["trend"]
            except Exception as e:
                self.__trend = None
                print(str(e))

            self.trend()

        else:
            self.__O = None
            self.__H = None
            self.__L = None
            self.__C = None
            self.__timestamp = None
            self.__trend = None

    def get_average(self):
        return 1

    def __repr__(self):
        a = [self.__O, self.__H, self.__L, self.__C, self.__timestamp, self.__trend]
        b = str(a)
        return b

    def trend(self):
        return (
            self.__trend
            if self.__O is None or self.__C is None
            else get_trend(self.__O, self.__C)
        )
