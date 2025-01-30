import json
import pandas as pd
import os
from .strategies.base_strategy import ThresholdStrategy
from .data.data_loader import load_and_process_data
from .utils.logger import Logger

class TradingBot:
    def __init__(self, config_path):
        self.logger = Logger(__name__)
        self.config = self.load_config(config_path)
        self.strategy = ThresholdStrategy(
            buy_threshold=self.config['strategy']['parameters']['buy_threshold'],
            sell_threshold=self.config['strategy']['parameters']['sell_threshold']
        )
        self.data = None
        self.balance = 1000  # Balance inicial en euros
        self.position = 0  # Posición actual (cantidad de activos)
        self.entry_price = 0  # Precio de entrada de la última operación

    def load_config(self, config_path):
        self.logger.info(f"Cargando configuración desde {config_path}")
        with open(config_path, 'r') as file:
            config = json.load(file)
        return config

    def load_market_data(self, symbol, interval, start_date, end_date):
        self.logger.info(f"Cargando datos de mercado para {symbol}")
        file_path = f"data/{symbol}_{interval}_{start_date}_{end_date}.csv"  # Ajusta la ruta del archivo según sea necesario
        processed_file_path = file_path.replace('.csv', '_data_processed.csv')
        
        # Verificar si el archivo original existe
        if not os.path.exists(file_path):
            self.logger.error(f"El archivo original {file_path} no existe.")
            raise ValueError(f"El archivo original {file_path} no existe.")
        
        # Procesar y guardar los datos si el archivo procesado no existe
        if not os.path.exists(processed_file_path):
            self.logger.info(f"El archivo procesado {processed_file_path} no existe. Procesando datos...")
            data = load_and_process_data(file_path)
            if data is not None:
                data.to_csv(processed_file_path)
                self.logger.info(f"Datos procesados guardados en {processed_file_path}")
            else:
                self.logger.error("No se pudo procesar los datos del mercado.")
                raise ValueError("No se pudo procesar los datos del mercado.")
        
        # Cargar el archivo procesado
        self.logger.info(f"Cargando datos procesados desde {processed_file_path}")
        self.data = pd.read_csv(processed_file_path, parse_dates=['DateTime'], index_col='DateTime')
        if self.data is None or self.data.empty:
            self.logger.error("No se pudo cargar los datos del mercado.")
            raise ValueError("No se pudo cargar los datos del mercado.")
        
        # Agregar la columna 'close' si no existe
        if 'close' not in self.data.columns:
            self.logger.info("Agregando columna 'close' como el promedio de 'Bid' y 'Ask'")
            self.data['close'] = (self.data['Bid'] + self.data['Ask']) / 2
        
        self.logger.info("Datos de mercado cargados correctamente.")

    def run(self):
        if self.data is not None:
            self.logger.info("Ejecutando estrategia de trading")
            signals = self.strategy.get_signal(self.data)
            for index, row in signals.iterrows():
                if row['buy_signal'] == 1 and self.position == 0:
                    self.position = self.balance / row['close']
                    self.entry_price = row['close']
                    self.balance = 0
                    self.logger.info(f"Ejecutar compra a {row['close']}, posición: {self.position}")
                elif row['sell_signal'] == 1 and self.position > 0:
                    self.balance = self.position * row['close']
                    self.position = 0
                    self.logger.info(f"Ejecutar venta a {row['close']}, balance: {self.balance}")

                # Verificar si la pérdida supera los 100 euros
                if self.position > 0 and (self.entry_price - row['close']) * self.position > 100:
                    self.balance = self.position * row['close']
                    self.position = 0
                    self.logger.info(f"Venta forzada a {row['close']} para evitar pérdidas mayores a 100 euros, balance: {self.balance}")
        else:
            self.logger.warning("No hay datos de mercado cargados.")