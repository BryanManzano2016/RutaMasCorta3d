import random as rd

'''
    Crear arreglo tridimensional que contenga nodos, cuya utima dimension tiene nodos
    El formato de posiciones es asi ---> matriz[z][y][x]
'''
def generarEspacio(distanciaSeparacion, limite):
    espacio = []
    for altura in range(0, limite, distanciaSeparacion):
        plano = []
        for largo in range(0, limite, distanciaSeparacion):
            recta = []
            for ancho in range(0, limite, distanciaSeparacion):
                recta.append( Nodo(ancho, largo, altura) )
            plano.append(recta)
        espacio.append(plano)
    return espacio

'''
    Crea elementos None en la matriz que es pasada por referencia, ademas de una lista
    de no ingresar el nodo de partida y de llegada. Por otra parte una lista pasada
    por referencia para tener posiciones que representan obstaculos 
'''
def anularEnMatriz(matriz, nro, porcentajeObstaculos, nodoInicio, nodoFin, matrizNula):
    for x in range( int((nro ** 3) * porcentajeObstaculos)):
        anchoAleatorio = rd.randrange(0, nro)
        largoAleatorio = rd.randrange(0, nro)
        altoAleatorio = rd.randrange(0, nro)
        if matriz[altoAleatorio][largoAleatorio][anchoAleatorio] != nodoInicio and \
            matriz[altoAleatorio][largoAleatorio][anchoAleatorio] != nodoFin:
            matriz[altoAleatorio][largoAleatorio][anchoAleatorio] = None
            matrizNula.append([anchoAleatorio, largoAleatorio, altoAleatorio])
            '''
            matrizNula.append( "x=" + str(anchoAleatorio) + ", y=" + str(largoAleatorio) +
                               ", z=" + str(altoAleatorio))
            '''
'''
    Crea una lista con los nodos vecinos que aun no son visitados, esto solo
    considerando posiciones no diagonales en el espacio
'''
def nodosVecinos(nodo, matriz):
    listaVecinos = []
    x = nodo.cx
    y = nodo.cy
    z = nodo.cz
    if not nodo is None:
        if x+1 < len(matriz):
            if not matriz[z][y][x+1] is None and not matriz[z][y][x+1].visitado:
                nodo = Nodo(matriz[z][y][x+1].cx, matriz[z][y][x+1].cy, matriz[z][y][x+1].cz)
                nodo.reempDistancia(matriz[z][y][x+1].distanciaAcumulada)
                listaVecinos.append( nodo )
        if x-1 >= 0:
            if not matriz[z][y][x-1] is None and not matriz[z][y][x-1].visitado:
                nodo = Nodo(matriz[z][y][x-1].cx, matriz[z][y][x-1].cy, matriz[z][y][x-1].cz)
                nodo.reempDistancia(matriz[z][y][x-1].distanciaAcumulada)
                listaVecinos.append(nodo)
        if y+1 < len(matriz):
            if not matriz[z][y+1][x] is None and not matriz[z][y+1][x].visitado:
                nodo = Nodo(matriz[z][y+1][x].cx, matriz[z][y+1][x].cy, matriz[z][y+1][x].cz)
                nodo.reempDistancia(matriz[z][y+1][x].distanciaAcumulada)
                listaVecinos.append(nodo)
        if y-1 >= 0:
            if not matriz[z][y-1][x] is None and not matriz[z][y-1][x].visitado:
                nodo = Nodo(matriz[z][y-1][x].cx, matriz[z][y-1][x].cy, matriz[z][y-1][x].cz)
                nodo.reempDistancia(matriz[z][y-1][x].distanciaAcumulada)
                listaVecinos.append(nodo)
        if z+1 < len(matriz):
            if not matriz[z+1][y][x] is None and not matriz[z+1][y][x].visitado:
                nodo = Nodo(matriz[z+1][y][x].cx, matriz[z+1][y][x].cy, matriz[z+1][y][x].cz)
                nodo.reempDistancia(matriz[z+1][y][x].distanciaAcumulada)
                listaVecinos.append(nodo)
        if z-1 >= 0:
            if not matriz[z-1][y][x] is None and not matriz[z-1][y][x].visitado:
                nodo = Nodo(matriz[z-1][y][x].cx, matriz[z-1][y][x].cy, matriz[z-1][y][x].cz)
                nodo.reempDistancia(matriz[z-1][y][x].distanciaAcumulada)
                listaVecinos.append(nodo)
    return listaVecinos


def dijkstra(nodoInicio, matriz):
    listaVisitados = []
    listaVisitados.append(nodoInicio)

    nodoTmp = None

    while len(listaVisitados) > 0:
        '''nodoTmp Solo se utiliza para la posicion'''
        nodoTmp = listaVisitados.pop(0)
        nodoEnMatriz = matriz[nodoTmp.cz][nodoTmp.cy][nodoTmp.cx]

        if not nodoEnMatriz is None and not nodoEnMatriz.visitado:

            matriz[nodoTmp.cz][nodoTmp.cy][nodoTmp.cx].visitar()

            for nodoVecino in nodosVecinos(nodoTmp, matriz):
                suma = nodoEnMatriz.distanciaAcumulada + nodoVecino.peso

                nodoEnMatriz2 = matriz[nodoVecino.cz][nodoVecino.cy][nodoVecino.cx]

                if nodoEnMatriz2.distanciaAcumulada >= suma:
                    matriz[nodoVecino.cz][nodoVecino.cy][nodoVecino.cx].reempDistancia(suma)
                    matriz[nodoVecino.cz][nodoVecino.cy][nodoVecino.cx]. \
                        darReferencia(matriz[nodoTmp.cz][nodoTmp.cy][nodoTmp.cx])

                listaVisitados.append(matriz[nodoVecino.cz][nodoVecino.cy][nodoVecino.cx])


'''
    Nodo que tiene atributos que representan puntos 3D, tambien se
    considera una referencia para ir guardando de donde viene la ruta mas optima
'''
class Nodo:
    def __init__(self, x, y, z):
        self.cx = x
        self.cy = y
        self.cz = z
        self.distanciaAcumulada = float('inf')
        self.visitado = False
        self.referencia = None
        self.peso = 1
    def darReferencia(self, nodo):
        self.referencia = nodo
    def reempDistancia(self, nro):
        self.distanciaAcumulada = nro
    def visitar(self):
        self.visitado = True
    def __str__(self) -> str:
        return "x=" + str(self.cx) + ", y=" + str(self.cy) \
               + ", z=" + str(self.cz)
    def __eq__(self, o: object) -> bool:
        return super().__eq__(o)

