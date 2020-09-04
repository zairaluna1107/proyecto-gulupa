#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 03:28:13 2020

@author: zaira
"""
import numpy as np    
#print('numpy version is:{}'.format(numpy.__version__))    
import seaborn as sns   
#print('seaborn version is{}'.format(seaborn.__version__))    
import sklearn    
#print('sklearn version is:{}'.format(sklearn.__version__)) 
import matplotlib.pyplot as plt
import pandas as pd  
#print('pandas version is: {}'.format(pandas.__version__))   
import statistics as stats

from sklearn import metrics
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from string import ascii_uppercase
from collections import Counter
#load dataset    
 
iris=pd.read_csv('iris.csv')  
iris=iris.drop('Id',axis=1)#eliminar la columna de "Id"
print(iris)
print('Información del dataset:')
print(iris.info())

#preview data    
print(iris.head(15)) 

#Description of Data    
print(iris.describe())  

#Flower distribution    
print(iris.groupby('Species').size())  

#Data Shape    
print(iris.shape) 
#dataset spliting    
 
array = iris.values    
X = array[:,0:4]    
Y = array[:,4]    
validation_size = 0.2    
seed = 7    
#División de los datos en tran y test con 80-20
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=validation_size,     
random_state=seed) 
y_pred=y_test
#evaluate model to determine better algorithm   
results = []    
names = []    
models = []    
#models.append(('LR', LogisticRegression()))    
models.append(('LDA', LinearDiscriminantAnalysis()))    
models.append(('CART', DecisionTreeClassifier()))    
models.append(('NB', GaussianNB()))    
models.append(('SVM', SVC()))  
models.append(('KNC', KNeighborsClassifier()))

for name, model in models:   
    kf = KFold(n_splits=10)
    clf = model
    clf.fit(X_train, y_train)
    score = clf.score(X_train,y_train)
    print("---------Modelo ", model, "----------")
    print("Metrica del modelo", score)
    results.append(score)    
    names.append(name)
    scores = cross_val_score(clf, X_train, y_train, cv=kf, scoring="accuracy")
    print("Metricas cross_validation", scores)
    print("Media de cross_validation", scores.mean())
    preds = clf.predict(X_test)
    score_pred = metrics.accuracy_score(y_test, preds)
    print("Metrica en Test", score_pred) 
    
    
#print(names)

#choose best one model trough graphical representation    
#pretiction    
svn = SVC()    
svn.fit(X_train, y_train)    
predictions = svn.predict(X_test)    
print(accuracy_score(y_test, predictions))    
print(confusion_matrix(y_test, predictions))    
print(classification_report(y_test, predictions)) 

cm= confusion_matrix(y_test, predictions)
columnas=['Clase %s'%(i) for i in list(ascii_uppercase)[0:len(np.unique(y_test))]]
df_cm=pd.DataFrame(cm,index=columnas,columns=columnas)

grafica=sns.heatmap(df_cm,cmap='Pastel1',annot=True)
grafica.set(xlabel='Verdadero',ylabel='Predicciones')
plt.show()

def infoboxplot (especie,hoja):
    df=pd.DataFrame(iris)
    f=df[df['Species']==especie][hoja]
    #print(f)
    vmin=min(f)
    vmax=max(f)
    print("-----------Especie: ",especie,"  Tipo de hoja: ",hoja,"-------------")
    print('valor min: ', vmin)
    print('valor max: ', vmax)
    rango=vmax-vmin
    print('Rango', rango)
    q1=np.percentile(f,[25])
    q2=np.percentile(f,[50])
    q3=np.percentile(f,[75])
    iqr=q3-q1
    print('q1: ', q1)
    print('q2: ', q2)
    print('q3: ', q3)
    print('iqr: ', iqr)
    print('media: ',stats.mean(f)) 
    print('mediana: ', stats.median(f))
    moda=Counter(f).most_common()[0][0]
    print('moda: ',moda)
    return(vmin,vmax,rango,q1,q2,q3,iqr)


#SepalLengthCm
vminsesl,vmaxsesl,rangosesl,q1sesl,q2sesl,q3sesl,iqrsesl = infoboxplot('Iris-setosa','SepalLengthCm')
vminversl,vmaxversl,rangoversl,q1versl,q2versl,q3versl,iqrversl = infoboxplot('Iris-versicolor','SepalLengthCm')
vminvirsl,vmaxvirsl,rangovirsl,q1virsl,q2virsl,q3virsl,iqrvirsl = infoboxplot('Iris-virginica','SepalLengthCm')

#SepalWidthCm
vminsesw,vmaxsesw,rangosesw,q1sesw,q2sesw,q3sesw,iqrsesw = infoboxplot('Iris-setosa','SepalWidthCm')
vminversw,vmaxversw,rangoversw,q1versw,q2versw,q3versw,iqrversw = infoboxplot('Iris-versicolor','SepalWidthCm')
vminvirsw,vmaxvirsw,rangovirsw,q1virsw,q2virsw,q3virsw,iqrvirsw = infoboxplot('Iris-virginica','SepalWidthCm')

#PetalLengthCm
vminsepl,vmaxsepl,rangosepl,q1sepl,q2sepl,q3sepl,iqrsepl = infoboxplot('Iris-setosa','PetalLengthCm')
vminverpl,vmaxverpl,rangoverpl,q1verpl,q2verpl,q3verpl,iqrverpl = infoboxplot('Iris-versicolor','PetalLengthCm')
vminvirpl,vmaxvirpl,rangovirpl,q1virpl,q2virpl,q3virpl,iqrvirpl = infoboxplot('Iris-virginica','PetalLengthCm')

#PetalWidthCm
vminsepw,vmaxsepw,rangosepw,q1sepw,q2sepw,q3sepw,iqrsepw = infoboxplot('Iris-setosa','PetalWidthCm')
vminverpw,vmaxverpw,rangoverpw,q1verpw,q2verpw,q3verpw,iqrverpw = infoboxplot('Iris-versicolor','PetalWidthCm')
vminvirpw,vmaxvirpw,rangovirpw,q1virpw,q2virpw,q3virpw,iqrvirpw = infoboxplot('Iris-virginica','PetalWidthCm')

#separar columnas con solo valores numéricos
arreglo=list(iris.columns)
iris1=iris[arreglo[0:4]]
print(iris1)

#Matriz de correlación
matrizco=iris1.corr('pearson')
print (matrizco)

print('Diagrama')
#Boxplot    
plt.figure(figsize=(15,10))    
plt.subplot(2,2,1)    
sns.boxplot(x='Species',y='SepalLengthCm',data=iris)    
plt.subplot(2,2,2)    
sns.boxplot(x='Species',y='SepalWidthCm',data=iris)    
plt.subplot(2,2,3)    
sns.boxplot(x='Species',y='PetalLengthCm',data=iris)    
plt.subplot(2,2,4)    
sns.boxplot(x='Species',y='PetalWidthCm',data=iris)  

#Pairwise joint plot (scatter matrix)    
sns.pairplot(iris,hue='Species', height=2, diag_kind="kde")    
sns.pairplot(iris,hue='Species')   

#verify new data    
X_new = np.array([[3, 2, 4, 0.2], [  4.7, 3, 1.3, 0.2 ]])    
print("X_new.shape: {}".format(X_new.shape))   

#validate    
prediction = svn.predict(X_new)    
print("Prediction of Species: {}".format(prediction))    
  
    
 
