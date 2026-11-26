"""Pila propia para el historial de estados de un ticket.

Recuperación de la Semana 4: antes de aplicar un cambio de estado se apila el
estado anterior, y "deshacer" saca el último que entró (política LIFO).
"""


class PilaEstados:
    def __init__(self):
        self._elementos = []

    def apilar(self, estado):
        self._elementos.append(estado)

    def desapilar(self):
        if not self._elementos:
            return None
        return self._elementos.pop()

    def cima(self):
        if not self._elementos:
            return None
        return self._elementos[-1]

    def esta_vacia(self):
        return not self._elementos

    def __len__(self):
        return len(self._elementos)
