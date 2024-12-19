#!/usr/bin/python

from pyspark import SparkConf, SparkContext
import sys
import re
import csv
from io import StringIO

start_time = time()

# Configuración del contexto de Spark
conf = SparkConf().setAppName('ListArtistsRDD')
sc = SparkContext.getOrCreate(conf)

# Archivo de entrada
input_file = sys.argv[1]
output_file = sys.argv[2]

# Leer el archivo
lines = sc.textFile(input_file)

# Procesar las líneas para extraer los artistas
artists = (
    lines.filter(lambda line: not line.startswith('title'))  # Ignorar encabezado
         .map(lambda line: list(csv.reader(StringIO(line)))[0][3])  # Usar csv.reader para extraer la columna de artistas
         .flatMap(lambda artist: artist.split(','))  # Dividir artistas separados por comas
         .map(lambda artist: artist.strip())  # Eliminar espacios en blanco
         .distinct()  # Obtener solo artistas únicos
	 .sortBy(lambda artist: artist.lower()) #Ordenar alfabéticamente sin importar mayúsculas
)

# Guardar los resultados
artists.saveAsTextFile(output_file)

print(f"Tiempo total de ejecución: {time() - start_time:.2f} segundos"}
