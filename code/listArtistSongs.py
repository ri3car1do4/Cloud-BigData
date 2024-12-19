#!/usr/bin/python

from pyspark import SparkConf, SparkContext
from time import time
import sys

start_time = time()

# Configuración de Spark
conf = SparkConf().setAppName('ListArtistSongsRDD')
sc = SparkContext.getOrCreate(conf)

# Leer los parámetros
input_file = sys.argv[1]      # Archivo de entrada
artist = sys.argv[2].lower()  # Convertimos a minúsculas para comparación case-insensitive
output_file = sys.argv[3]     # Carpeta de salida

# Leer el archivo de texto
lines = sc.textFile(input_file)

# Filtrar las líneas que no son encabezado y contienen al artista
songs = (
    lines.filter(lambda line: not line.startswith('title'))
         .map(lambda line: line.split(','))
         .filter(lambda fields: artist in fields[3].lower())  # Buscar al artista en la columna de artistas
         .map(lambda fields: (
             fields[0], 
             next((field for field in fields if field.startswith('http')), '')  # Extraer la primera URL válida
         ))
         .distinct()                                          # Eliminar duplicados
)

# Contar las canciones filtradas
count = songs.count()

# Añadir el contador al resultado
songs_with_count = sc.parallelize([f'Total songs found: {count}']).union(songs.map(lambda x: f'{x[0]} | {x[1]}'))

# Guardar el resultado
songs_with_count.saveAsTextFile(output_file)

print(f"Tiempo total de ejecución: {time() - start_time:.2f} segundos")
