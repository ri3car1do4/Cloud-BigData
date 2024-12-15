#!/usr/bin/python

from pyspark import SparkConf, SparkContext
import sys
import csv
from io import StringIO

# Configuración de Spark
conf = SparkConf().setAppName('SongAnalysisByYear')
sc = SparkContext.getOrCreate(conf)

# Parámetro de entrada: Año
year = sys.argv[1]
input_file = sys.argv[2]
output_file = sys.argv[3]

# Función para procesar líneas CSV correctamente
def parse_line(line):
    try:
        reader = csv.reader(StringIO(line))
        cols = next(reader)
        if cols[2].startswith(year):
            title = cols[0].strip()
            url = cols[4].strip()
            streams = int(cols[8].strip())
            return title, url, streams
    except Exception:
        return None

# Leer el archivo de texto
lines = sc.textFile(input_file)

# Filtrar el encabezado y procesar las líneas
songs = lines.filter(lambda line: not line.startswith("title"))\
            .map(parse_line)\
            .filter(lambda x: x is not None)

# Calcular la suma de streams por canción (nombre y URL)
summed_songs = songs.map(lambda x: ((x[0], x[1]), x[2]))\
                    .reduceByKey(lambda a, b: a + b)

# Identificar la canción más escuchada y la menos escuchada
most_listened = summed_songs.takeOrdered(1, key=lambda x: -x[1])
least_listened = summed_songs.takeOrdered(1, key=lambda x: x[1])

# Contar el total de canciones analizadas
total_songs = summed_songs.count()

# Guardar los resultados
results = sc.parallelize([
    f"Year: {year}",
    f"Total de canciones analizadas: {total_songs}",
    f"Canción más escuchada: {most_listened[0][0][0]} ({most_listened[0][0][1]}) con {most_listened[0][1]} reproducciones",
    f"Canción menos escuchada: {least_listened[0][0][0]} ({least_listened[0][0][1]}) con {least_listened[0][1]} reproducciones"
])

results.saveAsTextFile(output_file)

# Finalizar el contexto de Spark
sc.stop()

