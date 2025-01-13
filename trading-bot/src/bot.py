import json
import pandas as pd
from strategies.base_strategy import MovingAverageStrategy
from data.data_loader import load_data

class TradingBot:
    def __init__(self, config_path):
        self.config = self.load_config(config_path)
        self.strategy = MovingAverageStrategy(
            short_window=self.config['short_window'],
            long_window=self.config['long_window']
        )
        self.data = None

    def load_config(self, config_path):
        with open(config_path, 'r') as file:
            config = json.load(file)
        return config

    def load_market_data(self, file_path):
        self.data = load_data(file_path)
        if self.data is None:
            raise ValueError("No se pudo cargar los datos del mercado.")

    def run(self):
        if self.data is not None:
            signals = self.strategy.get_signal(self.data)
            last_signal = signals['positions'].iloc[-1]
            self.strategy.execute_trade(last_signal)
        else:
            print("No hay datos de mercado cargados.")

if __name__ == "__main__":
    bot = TradingBot(config_path='config.json')
    bot.load_market_data(file_path='path/to/your/market_data.csv')
    bot.run()