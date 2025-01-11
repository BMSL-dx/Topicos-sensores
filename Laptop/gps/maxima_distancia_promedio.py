import numpy as np
import matplotlib.pyplot as plt
from math import sqrt,pi
import random as rn

def distancia(p1,p2):
    return sqrt((p2[1]-p1[1])**2 + (p2[0]-p1[0])**2)

def graficarPuntos(puntos):
    puntos1=[puntos[i][0] for i in range(len(puntos))]
    puntos2=[puntos[i][1] for i in range(len(puntos))]

    # print(f"puntos1 = {puntos1}\npuntos2 = {puntos2}")
    media=[0,0]
    media[0]=sum(puntos1)/len(puntos1)
    media[1]=sum(puntos2)/len(puntos2)
    
    distancias = [distancia(media, puntos[i])
                  for i in range(len(puntos1))]

    maxima = max(distancias)
    theta=np.linspace(0,2*pi,100)
    x = maxima*np.cos(theta) + media[0]
    y = maxima*np.sin(theta) + media[1]
    plt.plot(puntos1,puntos2,'o',color='blue')
    plt.plot(media[0],media[1],'o',color='orange')
    plt.plot(x,y,color='orange')
    
    plt.show()

if __name__ == "__main__":
    inicio,final,fin=0,10,10
    puntos = [[rn.randrange(inicio,final,1),
                rn.randrange(inicio,final,1)] 
               for _ in range(0,fin)]
    
    # print(f"puntos = {puntos}")
    
    graficarPuntos(puntos)

