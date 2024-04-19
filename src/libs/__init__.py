from keys import API_KEY, SECRET_KEY
from libs.BinanceExchange import BinanceExchange
from libs.LoggerInstance import LoggerInstance
from libs.PlotterInstance import PlotterInstance

exchange = BinanceExchange({"apiKey": API_KEY, "secret": SECRET_KEY})

logger = LoggerInstance()

plotter = PlotterInstance()
