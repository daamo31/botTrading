import pandas as pd

def process_large_csv(file_path, chunksize=100000):
    try:
        print(f"Cargando y procesando datos desde {file_path} en bloques de {chunksize} filas...")
        
        # Crear un DataFrame vacío para almacenar los resultados procesados
        all_data = pd.DataFrame()

        # Leer el archivo CSV en bloques (chunks)
        for chunk in pd.read_csv(
            file_path,
            header=None,
            names=["DateTime", "Details"],
            dtype={0: str, 1: str},  # Forzar lectura como texto
            chunksize=chunksize,  # Tamaño del bloque
            low_memory=False  # Evitar advertencias de memoria
        ):
            # Separar la columna 'Details' en 'Time', 'Bid', 'Ask', y 'Volume'
            chunk[['Time', 'Bid', 'Ask', 'Volume']] = chunk['Details'].str.split(',', expand=True)

            # Combinar la fecha y la hora en una sola columna 'DateTime'
            chunk['DateTime'] = pd.to_datetime(
                chunk['DateTime'] + " " + chunk['Time'],
                format='%Y%m%d %H:%M:%S.%f',
                errors='coerce'
            )

            # Convertir 'Bid', 'Ask', y 'Volume' a tipo numérico
            chunk['Bid'] = pd.to_numeric(chunk['Bid'], errors='coerce')
            chunk['Ask'] = pd.to_numeric(chunk['Ask'], errors='coerce')
            chunk['Volume'] = pd.to_numeric(chunk['Volume'], errors='coerce')

            # Eliminar columnas no necesarias y filas con valores NaN
            chunk = chunk[['DateTime', 'Bid', 'Ask', 'Volume']].dropna()

            # Agregar el bloque procesado al DataFrame final
            all_data = pd.concat([all_data, chunk], ignore_index=True)

        # Configurar 'DateTime' como índice
        all_data.set_index('DateTime', inplace=True)

        print("Datos cargados y procesados correctamente:")
        print(all_data.head())

        return all_data

    except Exception as e:
        print(f"Error: {e}")
        return None

# Ruta al archivo CSV
file_path = '/Users/daniel/Desktop/bot/trading-bot/src/data/data.csv'

# Procesar el archivo en bloques
processed_data = process_large_csv(file_path, chunksize=500)  # Bloques de 500,000 filas

# Verificar los resultados
if processed_data is not None:
    print(processed_data.info())
