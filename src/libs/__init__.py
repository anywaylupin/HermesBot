from keys import API_KEY, SECRET_KEY
from libs.BinanceExchange import BinanceExchange
from libs.LoggerInstance import LoggerInstance
from libs.Plotter import Plotter

config = {"apiKey": API_KEY, "secret": SECRET_KEY}

exchange = BinanceExchange(config)

logger = LoggerInstance()

plotter = Plotter()
