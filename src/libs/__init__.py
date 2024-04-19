from keys import API_KEY, SECRET_KEY
from .BinanceExchange import BinanceExchange
from .LoggerInstance import LoggerInstance
from .PlotterInstance import PlotterInstance

exchange = BinanceExchange({"apiKey": API_KEY, "secret": SECRET_KEY})

logger = LoggerInstance()

plotter = PlotterInstance()
