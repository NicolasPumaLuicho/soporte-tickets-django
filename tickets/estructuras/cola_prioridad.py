class MinHeap:
    def __init__(self):
        self.heap = []

    def obtener_padre(self, i):
        return (i - 1) // 2

    def obtener_hijo_izq(self, i):
        return 2 * i + 1

    def obtener_hijo_der(self, i):
        return 2 * i + 2

    def obtener_minimo(self):
        if len(self.heap) == 0:
            return None
        return self.heap[0]

    def insertar(self, elemento):
        self.heap.append(elemento)
        self._flotar(len(self.heap) - 1)

    def _flotar(self, i):
        padre = self.obtener_padre(i)
        while i > 0 and self.heap[i] < self.heap[padre]:
            self.heap[i], self.heap[padre] = self.heap[padre], self.heap[i]
            i = padre
            padre = self.obtener_padre(i)

    def extraer_minimo(self):
        if len(self.heap) == 0:
            return None
        minimo = self.heap[0]
        ultimo = self.heap.pop()
        if len(self.heap) > 0:
            self.heap[0] = ultimo
            self._hundir(0)
        return minimo

    def _hundir(self, i):
        n = len(self.heap)
        while True:
            izq = self.obtener_hijo_izq(i)
            der = self.obtener_hijo_der(i)
            menor = i
            if izq < n and self.heap[izq] < self.heap[menor]:
                menor = izq
            if der < n and self.heap[der] < self.heap[menor]:
                menor = der
            if menor == i:
                break
            self.heap[i], self.heap[menor] = self.heap[menor], self.heap[i]
            i = menor


def cola_urgentes(tickets):
    cola = MinHeap()
    for t in tickets:
        cola.insertar((-t.prioridad(), t.id, t.titulo))
    return cola


def primeros(cola, k):
    salida = []
    while k > 0 and len(cola.heap) > 0:
        clave, id, titulo = cola.extraer_minimo()
        salida.append({"id": id, "titulo": titulo, "prioridad": -clave})
        k -= 1
    return salida
