import pandas as pd
import numpy as np

class BaseStrategy:
    def __init__(self):
        pass

    def execute_trade(self, signal):
        raise NotImplementedError("Este método debe ser implementado por estrategias específicas.")

    def get_signal(self, market_data):
        raise NotImplementedError("Este método debe ser implementado por estrategias específicas.")

class MovingAverageStrategy(BaseStrategy):
    def __init__(self, short_window=40, long_window=100):
        self.short_window = short_window
        self.long_window = long_window

    def get_signal(self, market_data):
        market_data['short_mavg'] = market_data['close'].rolling(window=self.short_window, min_periods=1).mean()
        market_data['long_mavg'] = market_data['close'].rolling(window=self.long_window, min_periods=1).mean()

        market_data['signal'] = 0
        market_data.iloc[self.short_window:, market_data.columns.get_loc('signal')] = \
            np.where(market_data['short_mavg'].iloc[self.short_window:] > market_data['long_mavg'].iloc[self.short_window:], 1, 0)
        market_data['positions'] = market_data['signal'].diff()

        return market_data

    def execute_trade(self, signal):
        if signal == 1:
            print("Ejecutar compra")
        elif signal == -1:
            print("Ejecutar venta")
        else:
            print("Mantener posición")

# Ejemplo de uso
if __name__ == "__main__":
    # Cargar datos de ejemplo
    data = pd.DataFrame({
        'date': pd.date_range(start='1/1/2024', periods=200),
        'close': np.random.randn(200).cumsum()
    })
    data.set_index('date', inplace=True)

    # Crear una instancia de la estrategia y obtener señales
    strategy = MovingAverageStrategy()
    signals = strategy.get_signal(data)

    # Ejecutar una operación basada en la última señal
    last_signal = signals['positions'].iloc[-1]
    strategy.execute_trade(last_signal)