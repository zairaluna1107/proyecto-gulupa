#!/usr/bin/python
# -*- coding: utf-8 -*-
#Realizado por: Santiago Alejandro Trujillo Fandiño
#Fecha: 9 de julio de 2020
#Versión: 1.0
"""
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

"""

import numpy as np
from matplotlib import pyplot as plt
import cv2
import sys
import argparse
import glob
from math import sqrt 

def calcmedia (R,G,B):
  """Calcula y retorna la media aritmética de cada canal de la imagen (R,G,B) 
Parameters
----------
R: componente R de la imagen
G: componente G de la imagen 
B: componente B de la imagen

Returns
-------
meanr: valor medio de la componente R
meang: valor medio de la componente G
meanb: valor medio de la componente B
"""
  meanr=np.mean(R)
  meang=np.mean(G)
  meanb=np.mean(B)
  print ('el valor medio de R es: {0:.2f}'.format(meanr))
  print ('el valor medio de G es: {0:.2f}'.format(meang))
  print ('el valor medio de B es: {0:.2f}'.format(meanb))
  
  return meanr,meang,meanb

def calcvarianza (R,G,B):
  """Calcula y retorna la varianza de cada canal de la imagen (R,G,B) 
Parameters
----------
R: componente R de la imagen
G: componente G de la imagen 
B: componente B de la imagen

Returns
-------
meanr: valor de la varianza de la componente R
meang: valor de la varianza de la componente G
meanb: valor de la varianza de la componente B
"""
  varianzar=np.var(R)
  varianzag=np.var(G)
  varianzab=np.var(B)
  print ('el valor de la varianza de R es: {0:.2f}'.format(varianzar))
  print ('el valor de la varianza de G es: {0:.2f}'.format(varianzag))
  print ('el valor de la varianza de B es: {0:.2f}'.format(varianzab))

  return varianzar,varianzag,varianzab
  
def calcdesv (R,G,B):
  """Calcula y retorna la desviación estándar de cada canal de la imagen (R,G,B) 
Parameters
----------
R: componente R de la imagen
G: componente G de la imagen 
B: componente B de la imagen

Returns
-------
meanr: valor de la desviación estándar de la componente R
meang: valor de la desviación estándar de la componente G
meanb: valor de la desviación estándar de la componente B
"""
  desvestr=np.std(R)
  desvestg=np.std(G)
  desvestb=np.std(B)
  print ('el valor de la desviación estandar de R es: {0:.2f}'.format(desvestr))
  print ('el valor de la desviación estandar de G es: {0:.2f}'.format(desvestg))
  print ('el valor de la desviación estandar de B es: {0:.2f}'.format(desvestb))

  return desvestr,desvestg,desvestb

def umbral (imabgr ,a ,c):
  """Se realiza la umbralización de la imagen BGR, los valores de la umbralización se obtuvieron con la herramienta dethreshold del programa GIMP
Parameters
----------
imabgr: imagen convertida a BGR 
a: 
c: 
Returns
-------
mascara: imagen BGR con umbralización
"""
  _,mascara=cv2.threshold(imabgr ,a ,c , cv2.THRESH_BINARY)
  #cv2.imshow('mascara',mascara)
  return mascara

def segmentacion (mascara,fil,col):
  """Segmentacion solo de la hoja
Parameters
----------
mascara: imagen BGR con umbralización 
fil: número de filas de la imagen
col: número de columnas de la imagen

Returns
-------
imasegho: hoja segmentada
"""
  imasegho=np.ones([fil,col],np.uint8)
  for i in range(fil):
   for j in range (col):
    if mascara[i ,j,0]==0 and mascara[i ,j,1]==0 and mascara[i ,j,2]==0:
     imasegho[i,j]=255;
    else:
     imasegho[i,j]=0;
  cv2.imshow('hoja segmentada',imasegho)

  return imasegho

def pixelesblancos (blancosho,closingho,fil,col):
  """ Permite conocer la cantidad de pixeles blancos que contiene la segmentación de la hoja y de cuadrado de referencia
Parameters
----------
closingho: imagen con aplicación de funciones morfológicas
fil: número de filas de la imagen
col: número de columnas de la imagen

Returns
-------
    blancosho: cantidad de pixeles blancos
"""
  for i in range(fil):
    for j in range (col):
      if closingho[i ,j]==255:
      	blancosho=blancosho+1;
  return blancosho

def area (perimeterho,areaho,contoursho):
  """Calcula y retorna el área y perímetro de la hoja en píxeles
Parameters
----------
contoursho: imagen del contorno de la hoja

Returns
-------
    areareal: area de la hoja en pixeles
    perimeterreal: perimetro de la hoja en pixeles
 """
  for cntho in contoursho:
      perimeterho.append(cv2.arcLength(cntho,True))
      perimetromaxi = max(perimeterho)
      areaho.append(cv2.contourArea(cntho))
      areamaxima = max(areaho)
  areareal=round(areamaxima)
  perimeterreal=round(perimetromaxi)
  return areareal, perimeterreal

def superior (fil,col,closingho):
  """Halla y retorna el punto superior de la hoja y el cuadrado de referencia.
Parameters
----------
closingho: imagen con aplicación de funciones morfológicas
fil: número de filas de la imagen
col: número de columnas de la imagen

Returns
-------
    superiorho: posición del punto superior

"""
  i = 0
  j = 0
  superiorho = []
  romper = 0
  for i in range(fil):
    for j in range (col):
      if closingho[i ,j] == 255:
          superiorho = [i,j]
          romper = 1
          break
    if romper == 1:
      break
  return superiorho

def inferior (fil,col,closingho):
  """Halla y retorna el punto inferior de la hoja y el cuadrado de referencia.
Parameters
----------
closingho: imagen con aplicación de funciones morfológicas
fil: número de filas de la imagen
col: número de columnas de la imagen

Returns
-------
    inferiorho: posición del punto inferior
"""
  i = fil
  j = col
  romper = 0
  for i in range(fil-1,0,-1):
    for j in range (col-1,0,-1):
      if closingho[i,j]==255:
          inferiorho = [i,j]
          romper = 1
          break
    if romper==1:
     break
  return inferiorho

def izquierda (fil,col,closingho):
  """Halla y retorna el punto máximo de la izquierda de la hoja y del cuadrado de referencia.
Parameters
----------
closingho: imagen con aplicación de funciones morfológicas
fil: número de filas de la imagen
col: número de columnas de la imagen

Returns
-------
    izquierdoho: posición del punto izquierdo
"""
  romper = 0
  for j in range(col):
    for i in range (fil):
      if closingho[i,j]==255:
          izquierdoho = [i,j]
          romper = 1
          break
    if romper==1:
     break
  return izquierdoho

def derecha (fil,col,closingho):
  """Halla y retorna el punto máximo de la derecha de la hoja y el cuadrado de referencia.
Parameters
----------
closingho: imagen con aplicación de funciones morfológicas
fil: número de filas de la imagen
col: número de columnas de la imagen

Returns
-------
    derechoho: posición del punto derecho
"""
  i = fil
  j = col
  romper = 0
  for j in range(col-1,0,-1):
    for i in range (fil-1,0,-1):
      if closingho[i,j]==255:
          derechoho = [i,j]
          romper = 1
          break
    if romper==1:
     break
  return derechoho

def imseg(fil,col,imabgr):
  """Realiza la segmentación de la parte afectada de la hoja.
Parameters
----------
fil: número de filas de la imagen
col: número de columnas de la imagen
imabgr: imagen convertida a BGR 

Returns
-------
    imaseg: imagen de la hoja segmentada en el área afectada
"""
  imaseg=np.ones([fil,col],np.uint8)
  for i in range(fil):
    for j in range (col):
        if imabgr[i,j,0]>=90 and imabgr[i,j,0]<=190 and imabgr[i,j,2]>=30 and imabgr[i,j,2]<=80 : #90,190  ima[i,j]>=85 and r[i,j]<=190
           imaseg[i,j]=255
        else:
            imaseg[i,j]=0; 
  return imaseg

def pixblancosafec(fil,col,imaseg):
  """ Encuantra la cantidad de pixeles blancos del área afectada
Parameters
----------
fil: número de filas de la imagen
col: número de columnas de la imagen
imaseg: imagen de la hoja segmentada en el área afectada

Returns
-------
    blancoshoseg: cantidad de pixeles blancos del área afectada
"""
  blancoshoseg=0;
  for i in range(fil):	
    for j in range (col):
      if imaseg[i,j]==255:
       blancoshoseg=blancoshoseg+1;
  return blancoshoseg

def segmentacioncua (imasegcua,mascara,fil,col):
  """  Realiza la segmentación del cuadrado de referencia
Parameters
----------
mascara: imagen BGR con umbralización
fil: número de filas de la imagen
col: número de columnas de la imagen

Returns
-------
    imasegcua: imagen con la segmentación del cuadrado

"""

  for i in range(fil):
    for j in range (col):
      if mascara[i ,j ,0]==0 and mascara[i ,j,1]==0 and mascara[i ,j,2]>=253:
       imasegcua[i,j]=255;
      else:
       imasegcua[i,j]=0;
  return imasegcua

def featurespixcsv (blancosho,areareal,perimeterreal,largoho,anchoho,blancoshoseg):
 
  x=open("featurespix.csv", mode="w")

  for i in [1]:
      a=blancosho
      b=areareal
      c=perimeterreal
      d=largoho
      e=anchoho
      f=blancoshoseg
      featurespix=str(a) +',' + str(b) + ',' + str(c) + ',' + str(d) + ',' + str(e) + ',' + str(f)
      x.write(featurespix+'\n')
      print(featurespix)




