from django.shortcuts import get_object_or_404, render

from .historial import historial_de
from .models import Ticket


def lista_tickets(request):
    tickets = Ticket.objects.all()
    return render(request, "tickets/lista_tickets.html", {"tickets": tickets})


def detalle_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    historial = historial_de(ticket)
    total = len(historial)

    posicion = 1
    try:
        posicion = int(request.GET.get("pos", 1))
    except ValueError:
        posicion = 1
    posicion = max(1, min(posicion, total))

    historial.posicionar(posicion)

    contexto = {
        "ticket": ticket,
        "comentario": historial.actual(),
        "posicion": posicion,
        "total": total,
        "hay_anterior": posicion > 1,  # equivalente a has_previous()
        "hay_siguiente": posicion < total,  # equivalente a has_next()
    }
    return render(request, "tickets/detalle_ticket.html", contexto)
