import numpy as np
import cv2
import colorgram
import PIL
import os
import math
import requests
import random
import urllib.request
import tweepy
import logging
import os
from functions import obtain_palette, url_to_image

#Ruta de la API del museo metropolitano
api_route="https://collectionapi.metmuseum.org/public/collection/v1/objects/"
#Ruta donde guardarás la imagen
folder_route=""
#Revisamos que solo nos devuelva obras con imagen pública
image=''
while image == '':
  #Obtenemos una obra de arte al azar
  object_id=random.randint(0,475947)
  request = requests.get(api_route+str(object_id))
  #Solo la publicamos si es una pintura
  try:
    if request.json()['objectName'] == "Painting":
      image=request.json()['primaryImage']
  except:
    pass
print("imagen recibida")
new_im=url_to_image(image)
#Obtenemos su paleta y la añadimos
cv2.imwrite(folder_route, new_im)
palette_im, dominant_color, color_palette =obtain_palette(folder_route)
cv2.imwrite(folder_route, palette_im)
print("Imagen procesada")
#Twitter tiene un tamaño límite de 3072 Kb. Si nuestra imagen excede el tamaño, le hace resize al tamaño que borda el límite de tamaño.
size = os.path.getsize(folder_route) 
if(size//1024 > 3000):
  scale_percent = math.sqrt(1/(size/1024/3000)) # percent of original size
  width = int(palette_im.shape[1] * scale_percent )
  height = int(palette_im.shape[0] * scale_percent )
  dim = (width, height)
  # resize image
  palette_im = cv2.resize(palette_im, dim, interpolation = cv2.INTER_AREA)
  cv2.imwrite(folder_route, palette_im)
print("Imagen modificada de tamaño")
#Credenciales de twitter
logger = logging.getLogger()
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

#Creamos nuestra API con twitter
def create_api():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, 
        wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api
#Publicamos el tweet!
api = create_api()
#Loggeado en twitter
author=request.json()["artistDisplayName"]
painting_name=request.json()["title"]
message=f"Paleta de colores para {painting_name} - {author} \n Publicado por un bot 🤖 \n Color Principal: {dominant_color}"
api.update_with_media(folder_route, status=message)
print(Tweet publicado!)