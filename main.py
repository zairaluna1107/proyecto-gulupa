# -*- coding: utf-8 -*-
#Realizado por: Santiago Alejandro Trujillo Fandiño
#Fecha: 9 de julio de 2020
#Versión: 1.0
"""Proyecto: IMPLEMENTACI ́ON DE UN SISTEMA CAPAZ DEFACILITAR LA IDENTIFICACI ́ON DEL CAMBIO DECOLOR EN LA HOJA DE GULUPA CONFORME A LAPRESENCIA O AUSENCIA DE NITR ́OGENO MEDIANTEEL PROCESAMIENTO DE IM ́AGENES RGB.

Parameters
----------

imagen1: imagen RGB de la hoja 


Returns
-------
	el valor de la  media  aritmetica de R es: xxxx

	el valor de la  media  aritmetica de G es: xxxx

	el valor de la  media  aritmetica de B es: xxxx

	el valor de la  varianza  de R es: xxxx

	el valor de la  varianza  de G es: xxxx

	el valor de la  varianza  de B es: xxxx

	el valor de la  desviación  estandar  de R es: xxxx

	el valor de la  desviación  estandar  de G es: xxxx

	el valor de la  desviación  estandar  de B es: xxxx

	la cantidad  de  pixeles  blancos  de la hoja  son :xxxx

	el área de la hoja en  pixeles  es:   xxxx

	el perímetro  de la hoja en  pixeles  es:   xxxx

	el largo de la hoja en  pixeles  es:   xxxx

	el ancho de la hoja en  pixeles  es:   xxxx

	la cantidad  de  pixeles  blancos  de la hoja  seg  son :xxxx

	el área  del  cuadro  en  pixeles  es:   xxxx

	el perimetro  del  cuadro  en  pixeles  es:   xxxx

	el largo  del  cuadrado  en  pixeles  es: xxxx

	el ancho  del  cuadrado  en  pixeles  es: xxxx

	el área de la hoja en  centímetros  cuadrados  es: xxxx

	el perímetro  de la hoja en  centímetros  es: xxxx

	el ancho de la hoja en cm es: xxxx

	el largo de la hoja en cm es: xxxx

	El área  afectada  de la hoja en cm  cuadrados  es: xxxx

	El porcentaje  de la hoja  que  presenta  deficiencia  de N es el : xxxx


Ejemplo
-------
   Positivo

     @debian:~/Documentos/mejora$ python main.py 1.JPG

	el valor de la  media  aritmetica de R es: 117.203

	el valor de la  media  aritmetica de G es: 68.274

	el valor de la  media  aritmetica de B es: 212.565

	el valor de la  varianza  de R es: 2080.676

	el valor de la  varianza  de G es: 1248.477

	el valor de la  varianza  de B es: 4528.048

	el valor de la  desviación  estandar  de R es: 45.619

	el valor de la  desviación  estandar  de G es: 35.3310

	el valor de la  desviación  estandar  de B es: 67.2911

	la cantidad  de  pixeles  blancos  de la hoja  son :18079012

	el área de la hoja en  pixeles  es:   180867.0013

	el perímetro  de la hoja en  pixeles  es:   2569.0014

	el largo de la hoja en  pixeles  es:   635.015

	el ancho de la hoja en  pixeles  es:   625.016

	la cantidad  de  pixeles  blancos  de la hoja  seg  son :8546717

	el área  del  cuadro  en  pixeles  es:   24088.0018

	el perimetro  del  cuadro  en  pixeles  es:   627.0019

	el largo  del  cuadrado  en  pixeles  es: 177.020

	el ancho  del  cuadrado  en  pixeles  es:   170.021

	el área de la hoja en  centímetros  cuadrados  es: 18822

	el perímetro  de la hoja en  centímetros  es: 82.0023

	el ancho de la hoja en cm es: 18.024

	el largo de la hoja en cm es: 18.025

	El área  afectada  de la hoja en cm  cuadrados  es: 8926

	El porcentaje  de la hoja  que  presenta  deficiencia  de N es el : 47

Referencias
----------
* https://es.wikipedia.org/wiki/NumPy
* https://unipython.com/matplotlib-funciones-principales/
* https://es.wikipedia.org/wiki/OpenCV
* https://uniwebsidad.com/libros/python/capitulo-10/modulos-de-sistema
* https://docs.python.org/3/library/argparse.html
* http://www.w3big.com/es/python/func-number-sqrt.html

Librerías
----------
import numpy as np
    Agrega mayor soporte para vectores y matrices, constituyendo una biblioteca de funciones matemáticas de alto nivel para operar con esos vectores
    o matrices. 
    
from matplotlib import pyplot as plt
    librería para generar gráficas a partir de datos contenidos en listas, vectores, en el lenguaje de programación Python y en su extensión
    matemática NumPy.

import cv2
    biblioteca usada para visión artificial.

import sys
    Encargado de proveer variables y funcionalidades, directamente relacionadas con el intérprete.

import argparse
    Facilita la escritura de interfaces de línea de comandos fáciles de usar. 

import glob
    El módulo glob encuentra todos los nombres de ruta que coinciden con un patrón específico de acuerdo con las reglas utilizadas por el shell de Unix

from math import sqrt 
    método sqrt () devuelve la raíz cuadrada del número x.

import imutils
    Librería creada que contiene diferentes funciones.


"""

import numpy as np
from matplotlib import pyplot as plt
import cv2
import sys
import argparse
import glob
from math import sqrt 
import imutils


def kill(imagen):
  imabgr=cv2.cvtColor(imagen, cv2.COLOR_RGB2BGR)
  #cv2.imshow('imabgr', imabgr)

  fil , col, ch= imabgr.shape
  r,g,b = cv2.split(imagen)

  meanr,meang,meanb = imutils.calcmedia(r,g,b)

  varianzar,varianzag,varianzab = imutils.calcvarianza(r,g,b)

  desvestr,desvestg,desvestb = imutils.calcdesv(r,g,b)

  mascara = imutils.umbral(imabgr,170,255)

  imasegho = imutils.segmentacion(mascara,fil,col)

  #EROSION hoja 
  kernel = np.ones((3,3),np.uint8)
  erosionho = cv2.erode(imasegho,kernel,iterations = 1)
  #cv2.imshow('erosionho',erosionho)

  #OPENING hoja quita puntos blancos fuera de lo segmentado 
  openingho = cv2.morphologyEx(erosionho, cv2.MORPH_OPEN, kernel)
  #cv2.imshow('openingho',openingho)
  
  #Closing hoja quita puntos negros dentro de lo segmentado 
  kernelclos= np.ones((3,3),np.uint8)
  kernelcloss= np.ones((7,7),np.uint8)
  closingho = cv2.morphologyEx(openingho, cv2.MORPH_CLOSE, kernelclos)
  closingho = cv2.morphologyEx(openingho, cv2.MORPH_CLOSE, kernelcloss)
  #cv2.imshow('closingho',closingho)
  blancosho=0;
  blancosho=imutils.pixelesblancos(blancosho,closingho,fil,col)
  print ('la cantidad de pixeles blancos de la hoja son:' + str(int(blancosho)))

 
  cannyho = cv2.Canny(closingho, 100, 150,)
  #cv2.imshow("cannyclo", cannyho)

  _,contoursho,_ = cv2.findContours(cannyho.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

  areaho = []
  perimeterho = []

  areareal,perimeterreal =imutils.area(perimeterho,areaho,contoursho)

  print ('el area de la hoja en pixeles es:  {0:.2f}'.format(areareal))
  print ('el perimetro de la hoja en pixeles es:  {0:.2f}'.format(perimeterreal))

  superiorho = []
  superiorho = imutils.superior(fil,col,closingho)

  inferiorho = []
  inferiorho = imutils.inferior(fil,col,closingho)
  #print'la posicion inferior es :', inferiorho

  izquierdoho = []
  izquierdoho=imutils.izquierda(fil,col,closingho)
  #print 'la posicion izquierda es :', izquierdoho

  derechoho = []
  derechoho = imutils.derecha(fil,col,closingho)
  #print'la posicion derecha es :', derechoho 

  largoho=sqrt(((inferiorho[0]-superiorho[0])**2)+((inferiorho[1]-superiorho[1])**2))
  largoho=round(largoho)
  print ('el largo de la hoja en pixeles es: ', largoho)

# Ancho de la hoja en pixeles
  anchoho=sqrt(((izquierdoho[0]-derechoho[0])**2)+((izquierdoho[1]-derechoho[1])**2))
  anchoho=round(anchoho)
  print ('el ancho de la hoja en pixeles es: ', anchoho)

  #segmentacion area afectada
  imaseg=imutils.imseg(fil,col,imabgr)
  #cv2.imshow('imaseg',imaseg)

  blancoshoseg=0;
  blancoshoseg=imutils.pixblancosafec(fil,col,imaseg)
  print('la cantidad de pixeles blancos de la hoja seg son:' + str(int(blancoshoseg)))

  x=imutils.featurespixcsv(blancosho,areareal,perimeterreal,largoho,anchoho,blancoshoseg)

  _,mask=cv2.threshold(imaseg,120,240,cv2.THRESH_BINARY)
  #cv2.imshow('mask',mask)

  #Filtros: El filtro de media permite mejorar la calidad de la imagen 
  ####
  median=cv2.medianBlur(mask,3)
  #cv2.imshow('median',median)

  cannyseg = cv2.Canny(median, 50, 150,) #50,150
  #cv2.imshow("cannyseg", cannyseg)

                                                           #CUADRADO

  #Segmentacion solo del cuadrado: Se separa el cuadrado de la imagen debido a que este funciona como referencia en cm de un area, largo
  #y perimetro conocido##
  imasegcua=np.ones([fil,col],np.uint8)
  imasegcua=imutils.segmentacioncua(imasegcua,mascara,fil,col)
  #cv2.imshow('imasegcua',imasegcua)#cuadro binarizado

  #Caracteristicas morfologicas erode-open
  #EROSION cuadrado
  kernelcua = np.ones((7,7),np.uint8)
  erosioncua = cv2.erode(imasegcua,kernelcua,iterations = 1)
  #cv2.imshow('erosioncua',erosioncua)
  ####
  #OPENING cuadrado
  openingcua = cv2.morphologyEx(erosioncua, cv2.MORPH_OPEN, kernel)
  #cv2.imshow('openingcua',openingcua)

  blancoscua=0;
  blancoscua=imutils.pixelesblancos(blancoscua,imasegcua,fil,col)
  print('la cantidad de pixeles blancos del cuadrado son:' + str(int(blancoscua)))

  #Seleccion borde del cuadrado
  cannycua = cv2.Canny(openingcua, 50, 150,)
  #cv2.imshow('cannycua',cannycua)

  #Encontrar Contornos cuadrado
  _,contourscua,_ = cv2.findContours(cannycua, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  print ('numero de formas: {0:2f}'.format(len(contourscua)))

  areacua = []
  perimetercua = []
  superiorcua = []
  inferiorcua = []
  izquierdocua = []
  derechocua = []

  areacua,perimetercua =imutils.area(perimetercua,areacua,contourscua)
  print ('el area del cuadro en pixeles es:  {0:.2f}'.format(areacua))
  print ('el perimetro del cuadro en pixeles es:  {0:.2f}'.format(perimetercua))

# Puntos Extremos
  ####
  #superior

  superiorcua = imutils.superior(fil,col,openingcua)
  print('la posicion superior del cuadrado es :', superiorcua)

  inferiorcua = imutils.inferior(fil,col,openingcua)
  print('la posicion inferior del cuadrado es :', inferiorcua)

  izquierdocua=imutils.izquierda(fil,col,openingcua)
  print ('la posicion izquierda del cuadrado es :', izquierdocua)

  derechocua = imutils.derecha(fil,col,openingcua)
  print('la posicion derecha del cuadrado es :', derechocua) 
  ####
  #Largo del cuadrado en pixeles
  largocua=sqrt(((superiorcua[0]-inferiorcua[0])**2)+((superiorcua[1]-inferiorcua[1])**2))
  largocua=round(largocua)
  print ('el largo del cuadrado en pixeles es:', largocua)
  ####
  # Ancho del cuadrado en pixeles
  anchocua=sqrt(((derechocua[0]-izquierdocua[0])**2)+((derechocua[1]-izquierdocua[1])**2))
  anchocua=round(anchocua)
  print ('el ancho del cuadrado en pixeles es: ', anchocua)

  areacuadrado= 25
  perimetrocuadrado= 20
  anchocuadrado=5
  largocuadrado=5

  #Calculo del area de la hoja en cmsuperiorho:  (400, 669)
  centimetrosho=areareal*areacuadrado
  centimetrosho=round(centimetrosho/areacua)
  if centimetrosho>1000:
    centimetrosho=centimetrosho/10000
  print ('el area de la hoja en centimetros cuadrados es: {0:.0f}'.format(centimetrosho))
  ####
  #Calculo del perimetro de la hoja cm
  perimetroho=perimeterreal*perimetrocuadrado
  perimetroho= round( perimetroho/perimetercua)
  print ('el perimetro de la hoja en centimetros es: {0:.2f}'.format(perimetroho))
  ####
  #Ancho de la hoja en cm
  ancmho=anchoho*anchocuadrado
  ancmho=round(ancmho/anchocua)
  print ('el ancho de la hoja en cm es:', ancmho)
  ####
  #largo de la hoja en cm
  lacmho=largoho*largocuadrado
  lacmho=round(lacmho/largocua)
  print ('el largo de la hoja en cm es:', lacmho)
  ####
  #Area afectada de la hoja
  areainfectada=(blancoshoseg*centimetrosho)
  areainfectada=round(areainfectada/blancosho)
  if areainfectada>1000:
    areainfectada=areainfectada/10000
  print ('El area afectada de la hoja en cm cuadrados es: {0:.0f}'.format(areainfectada))
  ####
  # Porcentaje de area afectada en la hoja
  porcentajem=areainfectada*100
  porcentajem=round(porcentajem/centimetrosho)
  print ('El porcentaje de la hoja que presenta deficiencia de N es el : {0:.0f}'.format(porcentajem))



def main (argv):
#Cargar Imagen
  iimagen=cv2.imread(sys.argv[1])
  width, height = 1080, 720
  iimagen=cv2.resize(iimagen,(width,height), interpolation=cv2.INTER_LINEAR)
  kill(iimagen)

main(sys.argv[1]) 

cv2.waitKey(0)
cv2.destroyAllWindows()
