"""Historial de comentarios con una lista doblemente enlazada.

Estructura de datos de la Semana 8: cada nodo guarda un comentario y sus
dos enlaces (anterior y siguiente). El historial además guarda un puntero
al nodo actual; anterior() y siguiente() solo mueven ese puntero y
devuelven False cuando no hay a dónde ir.
"""

from .models import Comentario


class NodoDoble:
    """Nodo para una lista doblemente enlazada."""

    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None
        self.anterior = None


class HistorialComentarios:
    """Lista doblemente enlazada para recorrer los comentarios de un ticket."""

    def __init__(self, comentarios=None):
        self.cabeza = None
        self.cola = None
        self._actual = None
        self.longitud = 0
        if comentarios is not None:
            for comentario in comentarios:
                self.agregar_al_final(comentario)

    def agregar_al_final(self, comentario):
        """Inserta un comentario al final y devuelve su nodo.

        Si el historial está vacío, deja el puntero actual en el nodo nuevo.
        """
        nuevo = NodoDoble(comentario)
        if self.cabeza is None:
            self.cabeza = nuevo
            self.cola = nuevo
            self._actual = nuevo
        else:
            nuevo.anterior = self.cola
            self.cola.siguiente = nuevo
            self.cola = nuevo
        self.longitud += 1
        return nuevo

    def posicionar(self, numero):
        """Coloca el puntero actual en el comentario número `numero` (1..longitud)."""
        if numero < 1:
            return False
        nodo = self.cabeza
        for _ in range(numero - 1):
            if nodo is None:
                return False
            nodo = nodo.siguiente
        if nodo is None:
            return False
        self._actual = nodo
        return True

    def actual(self):
        """Devuelve el comentario señalado por el puntero actual."""
        if self._actual is None:
            return None
        return self._actual.dato

    def anterior(self):
        """Mueve el puntero al nodo anterior. Devuelve False si no hay a dónde ir."""
        if self._actual is None or self._actual.anterior is None:
            return False
        self._actual = self._actual.anterior
        return True

    def siguiente(self):
        """Mueve el puntero al nodo siguiente. Devuelve False si no hay a dónde ir."""
        if self._actual is None or self._actual.siguiente is None:
            return False
        self._actual = self._actual.siguiente
        return True

    def __len__(self):
        return self.longitud


def historial_de(ticket):
    """Construye el historial de un ticket en orden cronológico."""
    return HistorialComentarios(ticket.comentarios.order_by("fecha"))
