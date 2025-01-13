from tradingview_ta import TA_Handler, Interval, Exchange
import pandas as pd
import datetime

def load_data(symbol, exchange, interval, start_date, end_date):
    try:
        # Configurar el manejador de TradingView
        handler = TA_Handler(
            symbol=symbol,
            screener="forex",  # Cambia esto según el tipo de mercado (e.g., "crypto", "stock")
            exchange=exchange,
            interval=interval
        )

        # Obtener datos históricos
        analysis = handler.get_analysis()
        data = analysis.indicators

        # Convertir los datos a un DataFrame de pandas
        df = pd.DataFrame([data])

        # Procesar los datos (por ejemplo, convertir fechas, eliminar columnas innecesarias)
        df['date'] = pd.to_datetime('now')  # Añadir una columna de fecha con la fecha actual
        df.set_index('date', inplace=True)

        # Filtrar por rango de fechas
        df = df[(df.index >= start_date) & (df.index <= end_date)]

        # Validar que los datos contengan las columnas necesarias
        required_columns = ['open', 'high', 'low', 'close', 'volume']
        for column in required_columns:
            if column not in df.columns:
                raise ValueError(f"Missing required column: {column}")

        print("Datos cargados correctamente:")
        print(df.head())

        return df

    except Exception as e:
        print(f"Error: {e}")
        return None