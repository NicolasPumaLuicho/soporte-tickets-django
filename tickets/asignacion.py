"""Asignación de tickets pendientes con la cola FIFO.

Los tickets abiertos se encolan en el orden en que se crearon y
asignar_siguiente_ticket() saca siempre el primero de la fila, para que se
atiendan en el mismo orden en que llegaron (Semana 5).
"""

from .estructuras.cola_tickets import ColaTickets
from .models import Ticket


def cola_de_pendientes():
    """Arma la cola con los tickets abiertos, del más antiguo al más nuevo."""
    cola = ColaTickets()
    for ticket in Ticket.objects.filter(estado="abierto").order_by("creado", "id"):
        cola.encolar(ticket)
    return cola


def asignar_siguiente_ticket():
    """Saca el primer ticket de la fila y lo deja en proceso. Devuelve None si no hay."""
    ticket = cola_de_pendientes().dequeue()
    if ticket is None:
        return None
    ticket.estado = "en_proceso"
    ticket.save(update_fields=["estado"])
    return ticket
