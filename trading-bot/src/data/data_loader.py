import pandas as pd
import logging

# Configuración de los logs
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def load_and_process_data(file_path, chunksize=100000):
    try:
        logger.info(f"Cargando y procesando datos desde {file_path} en bloques de {chunksize} filas...")

        # DataFrame final para almacenar los resultados procesados
        all_data = pd.DataFrame()
        error_count = 0  # Contador de filas con errores

        # Leer el archivo CSV en bloques
        for chunk in pd.read_csv(
            file_path,
            header=0,  # Asumimos que el archivo CSV tiene encabezados
            names=["DateTime", "Bid", "Ask", "Volume"],
            dtype={"DateTime": str, "Bid": float, "Ask": float, "Volume": int},  # Especificar tipos de datos
            chunksize=chunksize,
            low_memory=False
        ):
            logger.info("Procesando un nuevo bloque...")

            # Convertir la columna 'DateTime' a tipo datetime
            chunk['DateTime'] = pd.to_datetime(chunk['DateTime'], format='%Y%m%d %H:%M:%S.%f', errors='coerce')

            # Filtrar filas con valores inválidos o NaN
            chunk = chunk.dropna()

            # Concatenar el bloque procesado al DataFrame final
            all_data = pd.concat([all_data, chunk], ignore_index=True)

        # Configurar la columna 'DateTime' como índice
        all_data.set_index('DateTime', inplace=True)

        logger.info("Datos cargados y procesados correctamente.")
        logger.info(f"Total de filas con errores: {error_count}")
        return all_data

    except Exception as e:
        logger.error(f"Error al procesar los datos: {e}")
        return None


# Ruta al archivo CSV
file_path = '/Users/daniel/Desktop/bot/trading-bot/src/data/data.csv'

# Procesar el archivo
processed_data = load_and_process_data(file_path, chunksize=100000)

if processed_data is not None:
    logger.info(processed_data.info())
    print(processed_data.head())
else:
    logger.error("No se generó ningún DataFrame procesado.")