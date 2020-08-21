import numpy as np
from matplotlib import pyplot as plt
import cv2
import sys
import argparse
import glob
from math import sqrt 
import imutils
import os 

imagesPath = "/home/zaira/Documentos/mejora/mejora2/imagenes"
imagesPathList = os.listdir(imagesPath)
print('imagesPathList',imagesPathList)


for imageName in imagesPathList:
	datos=[]
	print('imageName',imageName)
	image = cv2.imread(imagesPath + '/' + imageName)
	#cv2.imshow('image',image)
	cv2.waitKey(0)
	width, height = 1080, 720
	imagen=cv2.resize(image,(width,height), interpolation=cv2.INTER_LINEAR)
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


	datos.append(blancosho)


	cannyho = cv2.Canny(closingho, 100, 150,)
	#cv2.imshow("cannyclo", cannyho)

	_,contoursho,_ = cv2.findContours(cannyho.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	areaho = []
	perimeterho = []

	areareal,perimeterreal =imutils.area(perimeterho,areaho,contoursho)

	print ('el area de la hoja en pixeles es:  {0:.2f}'.format(areareal))
	print ('el perimetro de la hoja en pixeles es:  {0:.2f}'.format(perimeterreal))

	datos.append(areareal)
        datos.append(perimeterreal)

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

	

	datos.append(largoho)


	# Ancho de la hoja en pixeles
	anchoho=sqrt(((izquierdoho[0]-derechoho[0])**2)+((izquierdoho[1]-derechoho[1])**2))
	anchoho=round(anchoho)
	print ('el ancho de la hoja en pixeles es: ', anchoho)


	datos.append(anchoho)
	

	#segmentacion area afectada
	imaseg=imutils.imseg(fil,col,imabgr)
	#cv2.imshow('imaseg',imaseg)

	blancoshoseg=0;
	blancoshoseg=imutils.pixblancosafec(fil,col,imaseg)
	print('la cantidad de pixeles blancos de la hoja seg son:' + str(int(blancoshoseg)))


	datos.append(anchoho)
        #x=imutils.featurespixcsv(datos)
	#x=imutils.featurespixcsv(blancosho,areareal,perimeterreal,largoho,anchoho,blancoshoseg)
	

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



cv2.destroyAllWindows()

