from builtins import list

import auxiliar as aux
import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

''' 
    Nodos separados por la variable distanciaSeparacion y 
    la variable limite es la longitud de las aristas del teorico cubo 
    de espacio tridimencional 
'''
distanciaSeparacion = 1
limite = distanciaSeparacion * 5
porcentajeObstaculos = 0.5

''' [x, y, z] '''
puntoPartida = [0, 0, 0]
puntoLlegada = [limite -1, limite -1, limite -1]
matriz = aux.generarEspacio(distanciaSeparacion, limite)

''' Desde el puntoPartida se considera la partida y puntoLlegada el de llegada '''
matriz[ puntoPartida[2] ][ puntoPartida[1] ][ puntoPartida[0] ].reempDistancia(0)
nodoInicio = matriz[ puntoPartida[2] ][ puntoPartida[1] ][ puntoPartida[0] ]
nodoFin = matriz[ puntoLlegada[2] ][ puntoLlegada[1] ][ puntoLlegada[0] ]

matrizNula = []
aux.anularEnMatriz(matriz, limite, porcentajeObstaculos, nodoInicio, nodoFin, matrizNula)

# Se van guardando los nodos vecinos que pueden continuar con la ruta
listaVisitados = []
listaVisitados.append(nodoInicio)

nodoTmp = None
contador=0
while len(listaVisitados) > 0:
    '''nodoTmp Solo se utiliza para la posicion'''
    contador+=1
    nodoTmp = listaVisitados.pop(0)
    nodoEnMatriz = matriz[nodoTmp.cz][nodoTmp.cy][nodoTmp.cx]

    if not nodoEnMatriz is None and not nodoEnMatriz.visitado:

        matriz[nodoTmp.cz][nodoTmp.cy][nodoTmp.cx].visitar()

        for nodoVecino in aux.nodosVecinos(nodoTmp, matriz):
            suma = nodoEnMatriz.distanciaAcumulada + nodoVecino.peso

            nodoEnMatriz2 = matriz[nodoVecino.cz][nodoVecino.cy][nodoVecino.cx]

            if nodoEnMatriz2.distanciaAcumulada >= suma:
                matriz[nodoVecino.cz][nodoVecino.cy][nodoVecino.cx].reempDistancia(suma)
                matriz[nodoVecino.cz][nodoVecino.cy][nodoVecino.cx].\
                    darReferencia( matriz[nodoTmp.cz][nodoTmp.cy][nodoTmp.cx] )

            listaVisitados.append(matriz[nodoVecino.cz][nodoVecino.cy][nodoVecino.cx])
print("El contador es "+str(contador))
''' 
    El nodo de llegada tiene una referencia que tambien tiene otra, asi hasta
    llegar al nodo de origen
'''



nodoMatriz = matriz[ puntoLlegada[2] ][ puntoLlegada[1] ][ puntoLlegada[0] ]
z_points = [ puntoLlegada[2] ]
y_points = [ puntoLlegada[1] ]
x_points = [ puntoLlegada[0] ]
nodo = nodoMatriz.referencia

if nodo is None:
    print("Los puntos de partida o llegada estan obstaculizados,\n"
          "!Ejecutar otra vez¡")
elif not nodo is None:
    print("Siendo una matriz %dx%dx%d" % (limite, limite, limite))
    print("Pasos dados:", nodo.distanciaAcumulada + 1)

    while nodo != None:
        z_points.append(nodo.cz)
        y_points.append(nodo.cy)
        x_points.append(nodo.cx)
        nodo = nodo.referencia

    z_obs_points = []
    y_obs_points = []
    x_obs_points = []
    for x in matrizNula:
        z_obs_points.append(x[2])
        y_obs_points.append(x[1])
        x_obs_points.append(x[0])

    fig = plt.figure()
    ax = plt.axes(projection="3d")
    plt.axis([0, limite, 0, limite])

    if len(x_obs_points) > 0:
        for k in range(len(x_obs_points) ):
            ax.scatter(x_obs_points[k], y_obs_points[k], z_obs_points[k],
                       s=(np.pi*(0.5)**2)*100, c='blue', alpha=0.75)

    ax.scatter(0, 0, 0, s=(np.pi*(0.5)**2)*100, c='y', alpha=0.75) # origen

    for k in range(len(z_points)):
        if(k==0 or k==(len(z_points)-1)):
            ax.scatter(x_points[k], y_points[k], z_points[k],
                   s=(np.pi*(0.5)**2)*100, c='g', alpha=0.75)
        else:
            ax.scatter(x_points[k], y_points[k], z_points[k],
                   s=(np.pi*(0.5)**2)*100, c='black', alpha=0.75)
        plt.pause(0.01)



    plt.show()

