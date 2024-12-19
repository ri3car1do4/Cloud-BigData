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
# Uso
# Evaluación del rendimiento
# Características avanzadas
# Conclusiones
En este proyecto, hemos logrado abordar con éxito varios desafíos asociados al procesamiento y análisis de grandes volúmenes de datos, en este caso, provenientes de Spotify. A través de técnicas de computación distribuida y almacenamiento en la nube, hemos diseñado e implementado una solución escalable y eficiente capaz de gestionar datos masivos y realizar consultas complejas en tiempo real.

Aunque hemos logrado implementar una solución escalable, siempre hay espacio para mejorar la eficiencia de las consultas. Se podrían incorporar técnicas de sharding (fragmentación de datos) y particionamiento de tablas para mejorar aún más la velocidad de acceso a grandes volúmenes de datos.

Una lección aprendida que queríamos destacar , es que en proyectos de Big Data, el diseño de los esquemas de datos y la estructuración adecuada de las tablas es crucial para asegurar una alta eficiencia en el procesamiento y las consultas. La creación de índices invertidos y el uso de particiones ayudaron a mejorar significativamente la velocidad de acceso.

Como trabajo futuro, se sugiere la incorporación de análisis de redes sociales. Esto serviría para enriquecer los datos musicales de Spotify y obtener una visión más completa sobre la popularidad y el impacto de las canciones y los artistas.

En conclusión, este proyecto no solo ha proporcionado soluciones técnicas eficientes, sino que también ha ofrecido una base sólida para explorar nuevas oportunidades en el análisis de datos musicales a gran escala.

# Referencias
Kaggle (Para la obtención del dataset): [https://www.kaggle.com/datasets/sunnykakar/spotify-audio-features?resource=download&select=charts.csv]

Apuntes del Google Classroom de la Asignatura (Para la implementación del código): [https://classroom.google.com/u/5/w/Njk3NzgxMTk4MjM4/t/all]

Documentación de Spark (Para la implementación del código): [https://spark.apache.org/docs/latest/sql-data-sources.html]

