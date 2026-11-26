"""Cola circular de tamaño fijo para los turnos pendientes.

Recuperación de la Semana 6: los turnos se atienden en orden de llegada y las
posiciones que deja libres cada atención se reutilizan con el operador %.
"""


class ColaCircular:
    def __init__(self, capacidad=8):
        self._datos = [None] * capacidad
        self._frente = 0
        self._cantidad = 0

    def encolar(self, dato):
        if self.esta_llena():
            return False
        posicion = (self._frente + self._cantidad) % len(self._datos)
        self._datos[posicion] = dato
        self._cantidad += 1
        return True

    def atender(self):
        if self.esta_vacia():
            return None
        dato = self._datos[self._frente]
        self._datos[self._frente] = None
        self._frente = (self._frente + 1) % len(self._datos)
        self._cantidad -= 1
        return dato

    def frente(self):
        if self.esta_vacia():
            return None
        return self._datos[self._frente]

    def esta_llena(self):
        return self._cantidad == len(self._datos)

    def esta_vacia(self):
        return self._cantidad == 0

    def __len__(self):
        return self._cantidad
