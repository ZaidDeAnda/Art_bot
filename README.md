# Art_bot
Un bot de twitter que publica una pintura diario, junto con su paleta de colores!

Solo se usa opencv para python (cv2), colorgram, y tweepy para la comunicación con twitter.

El unico archivo modificable es main.py, donde se necesita añadir la ruta del repositorio y las llaves de la API de twitter.

Para correrlo, simplemente ejecuta main.py. Sin embargo, esto solo te jalará una imagen de la api, le hará el análisis de colores
y la pbliccará. Para realizarlo periódicamente (como un bot), hay que usar un programador de tareas (task scheduler en windows
y cron job en linux)
