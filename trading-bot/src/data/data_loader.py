from tradingview_ta import TA_Handler, Interval, Exchange
import finnhub
import pandas as pd
import datetime

# Configurar el cliente de Finnhub
api_key = "cu3a1p9r01qure9c8cbgcu3a1p9r01qure9c8cc0"
api_secret = "cu3a1p9r01qure9c8cd0"
finnhub_client = finnhub.Client(api_key=api_key)

def load_data(symbol, exchange, interval, start_date, end_date, source="tradingview"):
    try:
        if source == "tradingview":
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

        elif source == "finnhub":
            # Convertir fechas a timestamps
            start_timestamp = int(pd.Timestamp(start_date).timestamp())
            end_timestamp = int(pd.Timestamp(end_date).timestamp())

            # Obtener datos históricos de Finnhub con el encabezado de autenticación
            headers = {
                'X-Finnhub-Secret': api_secret
            }
            res = finnhub_client.stock_candles(symbol, '60', start_timestamp, end_timestamp, headers=headers)

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

    except finnhub.FinnhubAPIException as e:
        print(f"Error de Finnhub: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None