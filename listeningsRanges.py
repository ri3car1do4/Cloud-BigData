#!/usr/bin/python

from pyspark import SparkConf, SparkContext
import sys

# Define las categorías de rangos de streams
def determine_range(average):
    if 0 <= average <= 1000:
        return "Rango 1: [0, 1000]"
    elif 1000 < average <= 5000:
        return "Rango 2: (1000, 5000]"
    elif 5000 < average <= 10000:
        return "Rango 3: (5000, 10000]"
    elif 10000 < average <= 30000:
        return "Rango 4: (10000, 30000]"
    elif 30000 < average <= 50000:
        return "Rango 5: (30000, 50000]"
    elif 50000 < average <= 70000:
        return "Rango 6: (50000, 70000]"
    elif 70000 < average <= 90000:
        return "Rango 7: (70000, 90000]"
    elif 90000 < average <= 150000:
        return "Rango 8: (90000, 150000]"
    elif 150000 < average <= 200000:
        return "Rango 9: (150000, 200000]"
    elif average > 200000:
        return "Rango 10: (200000, 1M)"
    else:
        return "Rango Inválido"

# Configuración de Spark
conf = SparkConf().setAppName('SongStreamsRange')
sc = SparkContext.getOrCreate(conf)

# Leer los argumentos de entrada
input_file = sys.argv[1]
output_file = sys.argv[2]

# Leer el archivo de entrada
lines = sc.textFile(input_file)

# Procesar los datos
streams = (
    lines.filter(lambda line: not line.startswith('title'))  # Saltar el encabezado
        .map(lambda line: line.split(','))  # Dividir en columnas
        .filter(lambda fields: fields[8].isdigit())  # Asegurar que la columna de streams sea numérica
        .map(lambda fields: (fields[0], (int(fields[8]), 1)))  # (nombre_canción, (streams, 1))
        .reduceByKey(lambda a, b: (a[0] + b[0], a[1] + b[1]))  # Sumar streams y contar ocurrencias
        .mapValues(lambda x: x[0] / x[1])  # Calcular promedio de streams
        .map(lambda x: (x[0], determine_range(x[1])))  # Asignar rango a cada canción
)

# Guardar el resultado
streams.saveAsTextFile(output_file)

