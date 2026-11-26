"""Historial de estados del ticket con una pila propia.

Cada ticket guarda su pila de estados anteriores: cambiar_estado() apila el
estado anterior antes de aplicar el nuevo y deshacer_ultimo_cambio() devuelve
el último estado apilado. Es la misma política LIFO de la Semana 4.
"""

from .estructuras.pila_historial import PilaEstados


def pila_de(ticket):
    """Devuelve la pila de estados del ticket, creándola si aún no existe."""
    pila = getattr(ticket, "_pila_estados", None)
    if pila is None:
        pila = PilaEstados()
        ticket._pila_estados = pila
    return pila


def cambiar_estado(ticket, nuevo_estado):
    """Aplica el estado nuevo guardando el anterior en la pila."""
    if nuevo_estado == ticket.estado:
        return False
    pila_de(ticket).apilar(ticket.estado)
    ticket.estado = nuevo_estado
    if ticket.pk:
        ticket.save(update_fields=["estado"])
    return True


def deshacer_ultimo_cambio(ticket):
    """Revierte el último cambio de estado. Devuelve False si no hay nada que deshacer."""
    anterior = pila_de(ticket).desapilar()
    if anterior is None:
        return False
    ticket.estado = anterior
    if ticket.pk:
        ticket.save(update_fields=["estado"])
    return True
