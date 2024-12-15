#!/usr/bin/python

from pyspark import SparkConf, SparkContext
import sys
import csv
from io import StringIO

# Configuración de Spark
conf = SparkConf().setAppName('Top50Songs')
sc = SparkContext.getOrCreate(conf)

# Parámetros de entrada: archivo, país, año, salida
input_file = sys.argv[1]
country = sys.argv[2]
year = sys.argv[3]
output_file = sys.argv[4]

# Función para procesar líneas CSV correctamente
def parse_line(line):
    try:
        reader = csv.reader(StringIO(line))
        cols = next(reader)
        title = cols[0].strip()
        rank = cols[1].strip()
        date = cols[2].strip()
        artist = cols[3].strip()
        url = cols[4].strip()
        region = cols[5].strip()
        chart = cols[6].strip()
        trend = cols[7].strip()
        streams = int(cols[8].strip())
        return (url, (streams, title, region, date.split('-')[0]))  # Clave: URL
    except Exception:
        return None

# Cargar los datos como RDD
lines = sc.textFile(input_file)

# Filtrar líneas relevantes y mapear a pares (URL, (streams, title))
tracks = (
    lines.filter(lambda line: not line.startswith('title'))  # Omitir encabezado
         .map(parse_line)  # Parsear líneas
         .filter(lambda x: x is not None and x[1][3] == year and x[1][2] == country)  # Filtro por año y país
)

# Reducir por clave (URL) para mantener el máximo número de reproducciones
max_streams_per_track = tracks.reduceByKey(lambda a, b: a if a[0] > b[0] else b)

# Mapear para obtener (streams, title)
top_tracks = max_streams_per_track.map(lambda x: (x[1][0], x[1][1]))

# Ordenar por número de reproducciones y tomar las 50 primeras
top50_tracks = top_tracks.sortBy(lambda x: -x[0]).take(50)

# Formatear salida y guardar los resultados
formatted_output = sc.parallelize(top50_tracks).map(lambda x: f"{x[1]},{x[0]}")

formatted_output.saveAsTextFile(output_file)

# Finalizar el contexto de Spark
sc.stop()

