
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
from functions import obtain_palette, url_to_image, obtain_image

palette_im, dominant_color, color_palette, request = obtain_image()
#Twitter tiene un tamaño límite de 3072 Kb. Si nuestra imagen excede el tamaño, le hace resize al tamaño que borda el límite de tamaño.
size = os.path.getsize("prueba.jpg") 
if(size//1024 > 3000):
  scale_percent = math.sqrt(1/(size/1024/3000)) # percent of original size
  width = int(palette_im.shape[1] * scale_percent )
  height = int(palette_im.shape[0] * scale_percent )
  dim = (width, height)
  # resize image
  palette_im = cv2.resize(palette_im, dim, interpolation = cv2.INTER_AREA)
  cv2.imwrite("prueba.jpg", palette_im)
print("Imagen modificada de tamaño")
#Credenciales de twitter
logger = logging.getLogger()
consumer_key = "d99GIAomdJYkhISI1c6KYZyfD"
consumer_secret = "T10zOaYPdfwXpy0Y7O8NuY8PyJcZ5qexD4UiidjUb8seB2pmX5"
access_token = "3427737434-e2Ho4byvTKikAN1rpIbw8Dl7XHCe0hLBDykQMF8"
access_token_secret = "KHwiB4H0sucDEjMIvsALzRtBIBuQHnEGBKTKg904Plzo8"

#Creamos nuestra API con twitter
def create_api():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
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
author=request["artistDisplayName"]
painting_name=request["title"]
try:
  message=f"{painting_name} - {author} \n Publicado por un bot 🤖\n Color Principal: {dominant_color}"
  api.update_with_media("prueba.jpg", status=message)
except:
  message=f"{painting_name} - {author} \n Publicado por un bot 🤖\n Color Principal: {dominant_color}\n Colores secundarios: {color_palette[0], color_palette[1], color_palette[2], color_palette[3], color_palette[4], color_palette[5]}"
  api.update_with_media("prueba.jpg", status=message)
print("Tweet publicado!")
