import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class BaseStrategy:
    def __init__(self):
        pass

    def execute_trade(self, signal):
        raise NotImplementedError("Este método debe ser implementado por estrategias específicas.")

    def get_signal(self, market_data):
        raise NotImplementedError("Este método debe ser implementado por estrategias específicas.")

class ThresholdStrategy(BaseStrategy):
    def __init__(self, buy_threshold=1.06451, sell_threshold=1.7):
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold

    def get_signal(self, market_data):
        market_data['signal'] = 0
        market_data['buy_signal'] = (market_data['close'] > self.buy_threshold).astype(int)
        market_data['sell_signal'] = (market_data['close'] >= self.sell_threshold).astype(int)
        return market_data

    def execute_trade(self, signal):
        if signal == 1:
            print("Ejecutar compra")
        elif signal == -1:
            print("Ejecutar venta")
        else:
            print("Mantener posición")

def test_strategy():
    # Generar datos de prueba
    dates = pd.date_range(start='2024-01-01', periods=200, freq='D')
    data = pd.DataFrame({
        'date': dates,
        'close': np.random.uniform(1.09, 1.11, size=200)  # Generar datos de cierre entre 1.09 y 1.11
    })
    data.set_index('date', inplace=True)

    # Crear una instancia de la estrategia y obtener señales
    strategy = ThresholdStrategy()
    signals = strategy.get_signal(data)

    # Mostrar todas las veces que se hubiese activado la compra
    buy_signals = signals[signals['buy_signal'] == 1]
    print("Señales de compra activadas:")
    print(buy_signals)

    # Visualizar los datos y las señales
    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data['close'], label='Close Price')
    plt.plot(buy_signals.index, buy_signals['close'], 'g^', markersize=10, label='Buy Signal')
    plt.axhline(y=1.09451, color='blue', linestyle='--', label='Buy Threshold')
    plt.axhline(y=1.10, color='red', linestyle='--', label='Sell Threshold')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    test_strategy()