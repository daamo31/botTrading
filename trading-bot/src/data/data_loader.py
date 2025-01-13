def load_data(file_path):
    import pandas as pd

    try:
        # Cargar datos históricos desde un archivo CSV
        data = pd.read_csv(file_path)

        # Procesar los datos (por ejemplo, convertir fechas, eliminar columnas innecesarias)
        data['date'] = pd.to_datetime(data['date'])
        data.set_index('date', inplace=True)

        # Validar que los datos contengan las columnas necesarias
        required_columns = ['open', 'high', 'low', 'close', 'volume']
        for column in required_columns:
            if column not in data.columns:
                raise ValueError(f"Missing required column: {column}")

        return data

    except FileNotFoundError:
        print(f"Error: El archivo {file_path} no se encontró.")
        return None
    except pd.errors.EmptyDataError:
        print("Error: El archivo está vacío.")
        return None
    except pd.errors.ParserError:
        print("Error: Hubo un problema al analizar el archivo.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None