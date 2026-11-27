class MaxHeap:
    def __init__(self):
        self.heap = []

    def _hundir(self, i):
        n = len(self.heap)
        while True:
            izq = 2 * i + 1
            der = 2 * i + 2
            mayor = i
            if izq < n and self.heap[izq] > self.heap[mayor]:
                mayor = izq
            if der < n and self.heap[der] > self.heap[mayor]:
                mayor = der
            if mayor == i:
                break
            self.heap[i], self.heap[mayor] = self.heap[mayor], self.heap[i]
            i = mayor

    def extraer_maximo(self):
        if len(self.heap) == 0:
            return None
        maximo = self.heap[0]
        ultimo = self.heap.pop()
        if len(self.heap) > 0:
            self.heap[0] = ultimo
            self._hundir(0)
        return maximo

    def construir(self, lista):
        self.heap = list(lista)
        ultimo_padre = len(self.heap) // 2 - 1
        for i in range(ultimo_padre, -1, -1):
            self._hundir(i)


def heap_sort(lista):
    monticulo = MaxHeap()
    monticulo.construir(lista)
    ordenada = []
    while len(monticulo.heap) > 0:
        ordenada.append(monticulo.extraer_maximo())
    return ordenada


def ranking_agentes(agentes):
    parejas = []
    for agente in agentes:
        parejas.append((agente.tickets_resueltos.count(), agente.username))
    ordenadas = heap_sort(parejas)
    ranking = []
    for puesto, pareja in enumerate(ordenadas, start=1):
        ranking.append(
            {
                "puesto": puesto,
                "agente": pareja[1],
                "resueltos": pareja[0],
            }
        )
    return ranking
