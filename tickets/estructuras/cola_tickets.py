"""Cola FIFO propia para los tickets pendientes.

Recuperación de la Semana 5: el ticket que llegó primero se atiende primero.
Se encola al final y dequeue() retira siempre el del frente.
"""


class ColaTickets:
    def __init__(self):
        self._elementos = []

    def encolar(self, ticket):
        self._elementos.append(ticket)

    def dequeue(self):
        if not self._elementos:
            return None
        return self._elementos.pop(0)

    def esta_vacia(self):
        return not self._elementos

    def __len__(self):
        return len(self._elementos)
