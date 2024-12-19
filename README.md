![image](https://github.com/user-attachments/assets/1884711d-89e9-4a63-ad09-e87699dc4acb)
# Descripción del problema.
En el marco del proyecto para la asignatura de Cloud Computing y Big Data, hemos seleccionado una base de datos que contiene información sobre canciones de Spotify recopiladas entre 2017 y 2021. 
El objetivo principal del proyecto es diseñar, implementar y evaluar una solución que aborde un problema típico de Big Data en la nube. Específicamente, nos enfocamos en el procesamiento y análisis eficiente de grandes volúmenes de datos relacionados con música, aprovechando técnicas de computación distribuida, almacenamiento escalable y consultas optimizadas. La solución propuesta debe ser capaz de gestionar datos a gran escala, realizar cálculos complejos y responder rápidamente a consultas específicas.
En el contexto de esta base de datos, buscamos abordar las siguientes necesidades analíticas relacionadas con las canciones de Spotify:

Identificación de canciones populares por región y tiempo: Obtener el top 50 de canciones para un país específico en una fecha dada. Esto requiere el uso de técnicas de filtrado eficiente (Filtering) para identificar los registros más relevantes.
Consulta de todas las canciones de un artista: Recuperar todas las canciones disponibles de un artista específico en la base de datos. Este proceso involucra la combinación de filtrado y resúmenes numéricos, como el conteo de registros por artista.
Detección de las canciones más escuchadas en un año: Identificar la canción más y la menos popular en un año específico, utilizando técnicas de resumen numérico, como cálculos de máximos y conteos.
Listado alfabético de artistas: Proveer un listado de todos los artistas disponibles en la base de datos, ordenados alfabéticamente, empleando técnicas de clasificación y búsqueda.
Clasificación de canciones por escuchas: Categorizar las canciones en rangos de escucha específicos (menos de 1000, entre 1000 y 5000, entre 5000 y 10000, etc) utilizando un índice invertido para mejorar la eficiencia de las consultas relacionadas con las escuchas.

Este proyecto aborda desafíos reales relacionados con el análisis de grandes volúmenes de datos musicales, como el manejo eficiente de información estructurada, el filtrado rápido de datos y la generación de insights relevantes. Los resultados obtenidos tienen aplicaciones en la industria musical, como análisis de tendencias, personalización de experiencias de usuario y estrategias de marketing basadas en datos.

# Necesidad de Big Data y Cloud.
El proyecto maneja grandes volúmenes de datos musicales (3,64 Gb) que superan la capacidad de sistemas tradicionales. Big Data es esencial para procesar estas consultas de manera eficiente, gracias a su capacidad de manejar altos volúmenes, velocidad y variedad de datos.
La nube complementa esto ofreciendo escalabilidad, elasticidad y costo-eficiencia. Permite ajustar recursos según las necesidades del proyecto, evitando inversiones iniciales altas y facilitando el acceso global y la colaboración en tiempo real. 
En conjunto, Big Data y la nube garantizan un procesamiento óptimo, almacenamiento flexible y análisis avanzado para resolver los desafíos del proyecto.

# Descripción de los datos
La identificación y adquisición de los datos para nuestro proyecto se llevó a cabo mediante una búsqueda exhaustiva entre diversas fuentes de datos proporcionadas en el material de referencia de la asignatura y otras de Internet. Tras una evaluación de diversas opciones, concluimos que kaggle.com era la plataforma que albergaba los conjuntos de datos más relevantes para nuestra idea de proyecto, una base de datos relacionada con Spotify, lo que nos permitió acceder a la información necesaria para llevar a cabo nuestra investigación. 

La estructura de los datos se compone de múltiples campos, que incluyen información crucial para nuestro análisis. Estos campos son los siguientes: título de la canción, posición del ranking, fecha del ranking, artista o artistas principales, url de la canción en spotify, región del ranking, ranking al que pertenece (top 200 o viral 50), tendencia (hacia arriba, hacia abajo o estable) y número de reproducciones(ese día en dicho país).
title: Nombre de la canción.
rank: Posición en el ranking de la región y fecha proporcionadas.
date: Fecha del ranking.
artist: Artistas de la canción, separados por comas si hay varios.
linkurl: Enlace a la canción en Spotify.
region: Región geográfica de la clasificación.
chart: Tipo de lista de clasificación (por ejemplo, "top200").
trend: Tendencia de la canción en el ranking ("SAME_POSITION", "UP", "DOWN").
streams: Número de reproducciones (streams) de la canción.

En cuanto al tamaño de los datos, estos ocupan un total de 3.64GB, lo que refleja la magnitud del conjunto de datos y justifica aún más la elección de técnicas de Big Data processing para su procesamiento y análisis.El formato de dicha base de datos es.CVS (Command-Separated Values), lo que facilita su posterior procesamiento.

# Descripción de la aplicación, modelo(s) de programación, plataforma e infraestructura.
## Descripción de la Aplicación
La aplicación desarrollada es una solución de análisis y consulta de datos musicales basada en la nube. Está diseñada para procesar información masiva proveniente de una base de datos de Spotify (2017-2021), permitiendo obtener insights clave sobre canciones, artistas y tendencias. La funcionalidad de la aplicación incluye:
- Consultas específicas:
    - Top 50 canciones por país y fecha.
    - Canciones más populares por año.
    - Canciones de un artista específico.
- Listados ordenados y categorizados:
    - Artistas ordenados alfabéticamente.
    - Canciones agrupadas por rangos de duración.
- Análisis avanzado:
    - Identificación de patrones y tendencias en la popularidad de canciones.
## Modelos de Programación
Se ha utilizado el framework de Apache Spark con Resilient Distributed Datasets (RDDs), se ha implementado el procesamiento paralelo para filtrar, ordenar y realizar cálculos sobre grandes volúmenes de datos, distribuyendo las tareas entre múltiples nodos.
## Plataforma
La aplicación está diseñada para ejecutarse en Apache Spark, aprovechando sus características clave: 
Compatibilidad con múltiples lenguajes: Python.
Distribución automática de datos y tareas: PySpark distribuye de forma eficiente entre los nodos del clúster, mejorando rapidez y eficiencia. 
## Infraestructura 
Hardware: Hacemos uso de un clúster de Dataproc en Google Cloud con múltiples nodos (Master Node que coordina el cluster y Worker Nodes que ejecutan las diferentes tareas). 
Software: Apache Spark, instalado en el clúster, y Python (PySpark), lenguaje principal de implementación. 
Almacenamiento: Usamos un Bucket de Google Cloud para subir la base de datos(en .csv) y almacenar las salidas (los resultados del análisis).

# Diseño del software
## Artistas ordenados alfabéticamente
```python
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
```
## Canciones agrupadas por rangos de duración
```python
#!/usr/bin/python

from pyspark import SparkConf, SparkContext
from time import time
import sys

start_time = time()

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

print(f"Tiempo total de ejecución: {time() - start_time:.2f} segundos"}
```
## Top 50 canciones por país y fecha
```python
#!/usr/bin/python

from pyspark import SparkConf, SparkContext
from time import time
import sys
import csv
from io import StringIO

start_time = time()

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

print(f"Tiempo total de ejecución: {time() - start_time:.2f} segundos")
```
## Canciones más populares por año.
```python
#!/usr/bin/python

from pyspark import SparkConf, SparkContext
from time import time
import sys
import csv
from io import StringIO

start_time = time()

# Configuración de Spark
conf = SparkConf().setAppName('SongAnalysisByYear')
sc = SparkContext.getOrCreate(conf)

# Parámetro de entrada: Año
input_file = sys.argv[1]
year = sys.argv[2]
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

print(f"Tiempo total de ejecución: {time() - start_time:.2f} segundos")
```
## Canciones de un artista específico
```python
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
```
## 
# Uso
En este apartado vamos a explicar el procedimiento que hemos seguido para obtener los resultados a partir de los códigos y la base de datos, y realizar las pruebas de las mismas.

Advertencia: en caso de no tener instalado PySpark, es crucial realizar su instalación en el Cloud Shell antes de continuar con los siguientes pasos.

En primer lugar, para poder trabajar con una base de datos tan grande, vamos a crear un cluster de la siguiente manera: 

![image](https://github.com/user-attachments/assets/61e5687c-e04b-4223-a2cd-81ecd7c16c97)

A continuación, hemos subido los documentos .py a nuestro Cloud Shell.

Para la obtención de los outputs, vamos a enviar el siguiente trabajo al cluster:
Para la obtención de outputs de llamadas no paramétricas, ejecutaremos el siguiente comando, sustituyendo “artistsSummary.py” por el documento en cuestión, y “outputArtistsSummary” por el nombre que le queramos adjudicar al documento de los resultados. Este sería el caso de: listeningRanges.py y artistsSummary.py.

![image](https://github.com/user-attachments/assets/f53220cf-0f2c-42a6-a82e-a05878fedbd2)

Output: 

Output (listeningRanges.py):

En cuanto a las trabajos con parámetros, diferenciamos los siguientes casos:
top50.py (archivo de entrada, pais, año, archivo de salida)

![image](https://github.com/user-attachments/assets/9f547f8e-b5d5-4e4e-9355-adbcc8f95ae1)

Output:

listArtistSongs.py (archivo de entrada, artista, archivo de salida)

![image](https://github.com/user-attachments/assets/29c271cb-0702-44a5-a786-2e136ea2e6dd)

Output:

mostLeastHeard.py (archivo de entrada, año, archivo de salida)

![image](https://github.com/user-attachments/assets/2546787d-82a8-480f-a213-2b4ae712b762)

Output:

Por último, para  mostrar los outputs vamos a ejecutar lo siguiente, sustituyendo “outputTop50Argentina2017” por el output que queramos consultar:

![image](https://github.com/user-attachments/assets/0475a697-9506-4ca6-aac7-4fa186f979a0)

# Evaluación del rendimiento
Para evaluar el rendimiento del sistema, se llevaron a cabo pruebas con configuraciones de 2 y 4 nodos. En cada caso, se registraron los tiempos de ejecución correspondientes del código de mostLeastHeard.py.

Con estos datos, se calculó el Speed Up utilizando la fórmula:
Speed Up = TiempoSecuencial / TiempoParalelo

Donde:
- TiempoSecuencial corresponde al tiempo de ejecución en un solo nodo (modo secuencial).
- TiempoParalelo es el tiempo de ejecución al usar múltiples nodos.

Este análisis ayuda a medir el aumento en la eficiencia del sistema al incrementar el número de nodos empleados. El tiempo de ejecución secuencial (en un solo nodo) es el siguiente:

![image](https://github.com/user-attachments/assets/2eef6457-9546-4062-9645-1d8e7485799a)

Resultado con 2 Nodos: 

![image](https://github.com/user-attachments/assets/1ea8035f-ba43-4f8f-ac98-154afa3cd50a)

Speed up = 

Resultado con 4 nodos: 

![image](https://github.com/user-attachments/assets/183fd192-2c23-450c-8b7f-ee2d52eb71f5)


Speed up = 

Se ha utilizado las siguientes instrucciones para conseguir los tiempos de ejecución:
```
from time import time
...
start_time = time()
...
print(f"Tiempo de ejecución: {time() - start_time:.2f} segundos")
```

# Características avanzadas

En el punto anterior podemos apreciar una de las funciones avanzadas que hemos utilizado en este proyecto que no habías utilizado en previos proyectos. 

En este proyecto nos hemos encontrado con varios desafíos. Es por esto, que además de emplear estas funciones para realizar análisis de códigos, también las hemos tenido que utilizar para hacer frente a las dificultades con las que nos topábamos. Entre estas, se encuentra la correcta lectura del fichero en todos los casos.

Durante el curso nos acostumbramos a separar documentos en formato .csv con el .split(‘,’), pero en este proyecto no nos era suficiente. Debido a ciertos inputs donde si ,por ejemplo, hay varios artistas, el apartado de artista se presenta de la manera “… ,“artista1, artista2, artista3”, …” en vez de “…,artista,...”; esto no nos permitía procesar los datos de forma correcta, lo que propiciaba outputs erróneos. Gracias a este problema comenzamos a utilizar la instrucción “reader = csv.reader(StringIO(line)”, la cual respeta el formato .csv, facilitando de esta manera el posterior análisis de los datos.

# Conclusiones
En este proyecto, hemos logrado abordar con éxito varios desafíos asociados al procesamiento y análisis de grandes volúmenes de datos, en este caso, provenientes de Spotify. A través de técnicas de computación distribuida y almacenamiento en la nube, hemos diseñado e implementado una solución escalable y eficiente capaz de gestionar datos masivos y realizar consultas complejas en tiempo real.

Aunque hemos logrado implementar una solución escalable, siempre hay espacio para mejorar la eficiencia de las consultas. Se podrían incorporar técnicas de sharding (fragmentación de datos) y particionamiento de tablas para mejorar aún más la velocidad de acceso a grandes volúmenes de datos.

Una lección aprendida que queríamos destacar , es que en proyectos de Big Data, el diseño de los esquemas de datos y la estructuración adecuada de las tablas es crucial para asegurar una alta eficiencia en el procesamiento y las consultas. La creación de índices invertidos y el uso de particiones ayudaron a mejorar significativamente la velocidad de acceso.

Como trabajo futuro, se sugiere la incorporación de análisis de redes sociales. Esto serviría para enriquecer los datos musicales de Spotify y obtener una visión más completa sobre la popularidad y el impacto de las canciones y los artistas.

En conclusión, este proyecto no solo ha proporcionado soluciones técnicas eficientes, sino que también ha ofrecido una base sólida para explorar nuevas oportunidades en el análisis de datos musicales a gran escala.

# Referencias
Kaggle (Para la obtención del dataset): [https://www.kaggle.com/datasets/sunnykakar/spotify-audio-features?resource=download&select=charts.csv](https://www.kaggle.com/datasets/sunnykakar/spotify-audio-features?resource=download&select=charts.csv)

Apuntes del Google Classroom de la Asignatura (Para la implementación del código): [https://classroom.google.com/u/5/w/Njk3NzgxMTk4MjM4/t/all](https://classroom.google.com/u/5/w/Njk3NzgxMTk4MjM4/t/all)

Documentación de Spark (Para la implementación del código): [https://spark.apache.org/docs/latest/sql-data-sources.html](https://spark.apache.org/docs/latest/sql-data-sources.html)

