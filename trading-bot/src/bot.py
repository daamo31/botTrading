import json
import pandas as pd
from .strategies.base_strategy import MovingAverageStrategy
from .data.data_loader import load_data
from .utils.logger import Logger

class TradingBot:
    def __init__(self, config_path):
        self.logger = Logger(__name__)
        self.config = self.load_config(config_path)
        self.strategy = MovingAverageStrategy(
            short_window=self.config['strategy']['parameters']['short_window'],
            long_window=self.config['strategy']['parameters']['long_window']
        )
        self.data = None

    def load_config(self, config_path):
        self.logger.info(f"Cargando configuración desde {config_path}")
        with open(config_path, 'r') as file:
            config = json.load(file)
        return config

    def load_market_data(self, symbol, interval, start_date, end_date):
        self.logger.info(f"Cargando datos de mercado para {symbol}")
        self.data = load_data(symbol, interval, start_date, end_date)
        if self.data is None:
            self.logger.error("No se pudo cargar los datos del mercado.")
            raise ValueError("No se pudo cargar los datos del mercado.")
        self.logger.info("Datos de mercado cargados correctamente.")

    def run(self):
        if self.data is not None:
            self.logger.info("Ejecutando estrategia de trading")
            signals = self.strategy.get_signal(self.data)
            last_signal = signals['positions'].iloc[-1]
            self.strategy.execute_trade(last_signal)
        else:
            self.logger.warning("No hay datos de mercado cargados.")

if __name__ == "__main__":
    bot = TradingBot(config_path='config.json')
    bot.load_market_data(symbol='EURUSD', interval='60', start_date='2023-01-01', end_date='2023-12-31')
    bot.run()