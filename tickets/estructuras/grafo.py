class Grafo:
    def __init__(self, nombres, es_dirigido=False):
        self.nombres = nombres
        self.es_dirigido = es_dirigido
        self.indice = {}
        for i in range(len(nombres)):
            self.indice[nombres[i]] = i
        n = len(nombres)
        self.matriz = [[0] * n for _ in range(n)]

    def agregar_arista(self, a, b, peso=1):
        i = self.indice[a]
        j = self.indice[b]
        self.matriz[i][j] = peso
        if not self.es_dirigido:
            self.matriz[j][i] = peso

    def mostrar(self):
        print("    " + "".join(f"{nombre[:3]:>5}" for nombre in self.nombres))
        for i in range(len(self.nombres)):
            fila = "".join(f"{valor:>5}" for valor in self.matriz[i])
            print(f"{self.nombres[i][:3]:<4}" + fila)

    def vecinos(self, a):
        i = self.indice[a]
        resultado = []
        for j in range(len(self.nombres)):
            if self.matriz[i][j] != 0:
                resultado.append(self.nombres[j])
        return resultado

    def grado(self, a):
        return len(self.vecinos(a))

    def grado_entrada(self, a):
        j = self.indice[a]
        total = 0
        for i in range(len(self.nombres)):
            if self.matriz[i][j] != 0:
                total = total + 1
        return total

    def tiempo_ruta(self, ruta):
        total = 0
        for k in range(len(ruta) - 1):
            i = self.indice[ruta[k]]
            j = self.indice[ruta[k + 1]]
            if self.matriz[i][j] == 0:
                return -1
            total = total + self.matriz[i][j]
        return total

    def mas_conectado(self):
        mejor = None
        mayor = 0
        for nombre in self.nombres:
            if self.grado(nombre) > mayor:
                mayor = self.grado(nombre)
                mejor = nombre
        return mejor

    def mutuos(self, a):
        i = self.indice[a]
        resultado = []
        for j in range(len(self.nombres)):
            if self.matriz[i][j] != 0 and self.matriz[j][i] != 0:
                resultado.append(self.nombres[j])
        return resultado
