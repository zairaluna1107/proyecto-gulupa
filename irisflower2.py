#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 17:25:57 2020

@author: zaira
"""

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

import numpy as np
import pandas as pd

#importar dataset
iris= pd.read_csv("iris.csv")
iris=iris.drop('Id',axis=1)#eliminar la columna de "Id"

print('Información del dataset:')
print(iris.info())

print('Descripción del dataset')
print(iris.describe())#datos estadisticos del dataset

print('Distribución de las especies del iris:')
print(iris.groupby('Species').size())

import matplotlib.pyplot as plt

#Grafico Sepal - Longitud vs Ancho 
fig=iris[iris.Species == 'Iris-setosa'].plot(kind='scatter', x='SepalLengthCm', y='SepalWidthCm',color='blue', label='Setosa')
iris[iris.Species == 'Iris-versicolor'].plot(kind='scatter', x='SepalLengthCm', y='SepalWidthCm',color='green',label='Versicolor',ax=fig)
iris[iris.Species == 'Iris-virginica'].plot(kind='scatter', x='SepalLengthCm', y='SepalWidthCm',color='red',label='virginica',ax=fig)

fig.set_xlabel(u"Sépalo - Longitud")
fig.set_ylabel(u"Sépalo - Ancho")
fig.set_title(u"Sépalo - Longitud vs Ancho")
plt.show()

#Grafico Pétalo - Longitud vs Ancho 
fig=iris[iris.Species == 'Iris-setosa'].plot(kind='scatter', x='PetalLengthCm', y='PetalWidthCm',color='blue', label='Setosa')
iris[iris.Species == 'Iris-versicolor'].plot(kind='scatter', x='PetalLengthCm', y='PetalWidthCm',color='green',label='Versicolor',ax=fig)
iris[iris.Species == 'Iris-virginica'].plot(kind='scatter', x='PetalLengthCm', y='PetalWidthCm',color='red',label='virginica',ax=fig)

fig.set_xlabel(u"Pétalo - Longitud")
fig.set_ylabel(u"Pétalo - Ancho")
fig.set_title(u"Pétalo - Longitud vs Ancho")
plt.show()

X=np.array(iris.drop(['Species'],1))
y=np.array(iris['Species'])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

print('Son {} datos para entrenamiento y {} datos para prueba'.format(X_train.shape[0], X_test.shape[0]))

"""
#modelo de regresion logistica
algoritmo =LogisticRegression()
algoritmo.fit(X_train, y_train)
Y_pred = algoritmo.predict(X_test)
print('Precision Regresion Logistica {}'.format(algoritmo.score(X_train, y_train)))
"""
#modelo de maquinas de vectores de soporte
algoritmo = SVC()
algoritmo.fit(X_train, y_train)
Y_pred = algoritmo.predict(X_test)
print('Precisión Máquinas de Vectores de Soporte: {}'.format(algoritmo.score(X_train, y_train)))

#Modelo de Vecinos más Cercanos
algoritmo = KNeighborsClassifier(n_neighbors=5)
algoritmo.fit(X_train, y_train)
Y_pred = algoritmo.predict(X_test)
print('Precisión Vecinos más Cercanos: {}'.format(algoritmo.score(X_train, y_train)))

#Modelo de Árboles de Decisión Clasificación
algoritmo = DecisionTreeClassifier()
algoritmo.fit(X_train, y_train)
Y_pred = algoritmo.predict(X_test)
print('Precisión Árboles de Decisión Clasificación: {}'.format(algoritmo.score(X_train, y_train)))
