import finnhub
import pandas as pd
import datetime

# Configurar el cliente de Finnhub
api_key = "cu3a1p9r01qure9c8cbgcu3a1p9r01qure9c8cc0"
finnhub_client = finnhub.Client(api_key=api_key)

def load_data(symbol, interval, start_date, end_date):
    try:
        # Convertir fechas a timestamps
        start_timestamp = int(pd.Timestamp(start_date).timestamp())
        end_timestamp = int(pd.Timestamp(end_date).timestamp())

        # Obtener datos históricos de Finnhub
        res = finnhub_client.stock_candles(symbol, interval, start_timestamp, end_timestamp)

        # Convertir los datos a un DataFrame de pandas
        df = pd.DataFrame({
            'date': pd.to_datetime(res['t'], unit='s'),
            'open': res['o'],
            'high': res['h'],
            'low': res['l'],
            'close': res['c'],
            'volume': res['v']
        })
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