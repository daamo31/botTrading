import pandas as pd

def load_data(file_path):
    try:
        print(f"Cargando datos desde {file_path}")
        
        # Cargar datos desde un archivo CSV
        df = pd.read_csv(file_path, parse_dates=['date'], index_col='date')

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

# Ejemplo de uso
file_path = '../data/data.csv'
df = load_data(file_path)
