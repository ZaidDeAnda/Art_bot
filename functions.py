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

def obtain_palette(img_path):
  original_image=cv2.imread(img_path)
  colors = colorgram.extract(img_path, 7)
  print(colors)
  dominant_color=colors[1].rgb
  palette=colors[0],colors[2],colors[3],colors[4],colors[5],colors[6]
  dominant_color=[x for x in dominant_color]
  palette = [x.rgb for x in palette]
  color_palette=[]
  for i in range(len(palette)):
    color_palette.append([palette[i][0],palette[i][1],palette[i][2]])
  palette_resized=np.array(palette)
  palette_resized.resize([2,3,3])
  #Creamos una franja blanca
  white_space = np.ones([original_image.shape[1]//3, original_image.shape[1],3])*255
  lenght = original_image.shape[1]
  dominant_position_x=lenght//6
  dominant_position_y=white_space[0]
  #Para el color principal
  start_point = (0, 0)
  end_point = (original_image.shape[1]//3,original_image.shape[1]//3)
  color=dominant_color[::-1]
  thickness=-1
  white_space = cv2.rectangle(white_space, start_point, end_point, color, thickness)
  #Para los colores segundarios
  increment_x=(lenght-original_image.shape[1]//3)//3
  start_positions_x=[x*increment_x+original_image.shape[1]//3 for x in np.arange(3)]
  start_positions_x.append(white_space.shape[1])
  increment_y=original_image.shape[1]//3//2
  start_positions_y=[y*increment_y for y in np.arange(2)]
  start_positions_y.append(original_image.shape[1]//3)
  b=0
  for i in range(len(start_positions_x)-1):
    for j in range(len(start_positions_y)-1):
      start_points = (start_positions_x[i],start_positions_y[j])
      end_points = (start_positions_x[i+1],start_positions_y[j+1])
      color=palette[b][::-1]
      b+=1
      thickness=-1
      white_space = cv2.rectangle(white_space, start_points, end_points, color, thickness)
  new_im=np.vstack([original_image, white_space])
  return new_im, dominant_color, palette

def url_to_image(url):
  # hacemos una función para primero descargar una imagen en una url
  resp = urllib.request.urlopen(url)
  # Convertirmos el request a un numpy array
  image = np.asarray(bytearray(resp.read()), dtype="uint8")
  # lo convertimos a imagen
  image = cv2.imdecode(image, cv2.IMREAD_COLOR)
  # regresamos la imagen
  return image

def obtain_image():
  #Ruta de la API del museo metropolitano
  api_route="https://collectionapi.metmuseum.org/public/collection/v1/objects/"
  #Revisamos que solo nos devuelva obras con imagen pública
  image=''
  while image is '':
    #Obtenemos una obra de arte al azar
    object_id=random.randint(0,475947)
    request = requests.get(api_route+str(object_id))
    #Solo la publicamos si es una pintura
    try:
      if request.json()['objectName'] == "Painting":
        image=request.json()['primaryImage']
    except:
      pass
  new_im=url_to_image(image)
  cv2.imwrite("prueba.jpg", new_im)
  while len(colorgram.extract("prueba.jpg", 7)) != 7:
    print("imagen rechazada")
    #Revisamos que solo nos devuelva obras con imagen pública
    image=''
    while image is '':
      #Obtenemos una obra de arte al azar
      object_id=random.randint(0,475947)
      request = requests.get(api_route+str(object_id))
      #Solo la publicamos si es una pintura
      try:
        if request.json()['objectName'] == "Painting":
          image=request.json()['primaryImage']
      except:
        pass
    new_im=url_to_image(image)
    cv2.imwrite("prueba.jpg", new_im)
  #Obtenemos su paleta y la añadimos
  scale_percent = 0.5 # percent of original size
  width = int(new_im.shape[1] * scale_percent )
  height = int(new_im.shape[0] * scale_percent )
  dim = (width, height)
  # resize image
  new_im = cv2.resize(new_im, dim, interpolation = cv2.INTER_AREA)
  cv2.imwrite("prueba.jpg", new_im)
  #Obtenemos su paleta y la añadimos
  print("imagen recibida")
  palette_im, dominant_color, color_palette = obtain_palette("prueba.jpg")
  print("imagen procesada")
  return palette_im, dominant_color, color_palette, request.json()
