# encoding: utf-8
#Descargar de la API de clubrural precios, número habitaciones y coordenas géográficas 
#de casas rurales y generar gráficas para compararlas. 
import json
import requests
import numpy as np
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import parse
import matplotlib.pyplot as plt
import itertools
from math import sin, cos, sqrt, atan2, radians

def calcularMedia(lista):
	longitud = len(lista)
	total = 0
	for i in range(longitud):
		total = total + lista[i]
	media = total / longitud
	return media

if __name__ == '__main__':

	url='https://api.clubrural.com/api.php?claveapi=9d757c33e4ac1c2d35fc7272e0709cd1&type=gmaps&lat=42.881457&lng=-8.545113&limitkm=100' #Url con clave API
	args = {'tipo':'Apartamento Rural', 'provincia':'A Coruña'} #Header
	response = requests.get(url, params=args) #GET

	print(response.url) 

	if response.status_code == 200: #Si response correcto
		data = response.text
		root = ET.fromstring(data) #Leer XML con los datos
		alojamientos = root.findall('alojamiento')

		R = 6373.0 #Radio aproximado de la tierra
		latSantiago = radians(42.881457) #Latitud catedral Santiago en radianes
		lonSantiago = radians(-8.545113) #Longitud catedral Santiago en radianes

		cont = 0 
		#Listas vacias
		precios = []
		plazas = []
		latitudes = []
		longitudes = []
		distancias = []

		for child in alojamientos:
			precios.append(int(alojamientos[cont][9].text))
			plazas.append(int(alojamientos[cont][10].text))
			latitudes.append(float(alojamientos[cont][15].text))
			longitudes.append(float(alojamientos[cont][16].text))
			cont = cont + 1
		#Elimino elementos fuera de rango
		precios.pop(8)
		plazas.pop(8)
		latitudes.pop(8)
		longitudes.pop(8)

		plazasOrd, preciosOrd = zip(*sorted(zip(plazas, precios))) #Plazas y precios ordenadas por pares
		latOrder, longOrder = zip(*sorted(zip(latitudes,longitudes))) #Latitudes y longitudes ordenadas por pares


		x = 0 

		#Bucle para convertir coordenadas a km 
		for i in range (len(latOrder)):
			latRad = radians(latOrder[x])
			lonRad = radians(longOrder[x])
			dlat = latRad - latSantiago 
			dlong = lonRad - lonSantiago 
			a = sin(dlat/2)**2 + cos(latSantiago) * cos(latRad) * sin(dlong/2) **2 #Formula Haversine para convertir a km
			c = 2*atan2(sqrt(a), sqrt(1 - a))
			d = R * c
			distancias.append(d)
			x = x + 1
		

		#Generar gráficas
		plt.scatter(plazasOrd,preciosOrd, s=10, color='red') #Gráfico de puntos con plazas y precios
		plt.xticks(np.arange(0,150,step=10)) 
		plt.yticks(np.arange(0,100,step=5)) 

		plt.xlabel("Número de plazas")
		plt.ylabel("Precio (Euros)")
		plt.show() #Mostrar label del plot

		plt.scatter(distancias,preciosOrd)
		plt.xlabel("Distancia del centro de Santiago (km)")
		plt.ylabel("Precio (Euros)")
		plt.show()
		#Imprimir datos
		print(distancias)
		print(plazasOrd)
		print(preciosOrd) 
		#Calcular medias
		mediaPrecios = calcularMedia(preciosOrd)
		mediaPlazas = calcularMedia(plazasOrd)
		print("Media precios:")
		print(mediaPrecios)
		print("Media plazas:")
		print(mediaPlazas)
		print(len(alojamientos) )