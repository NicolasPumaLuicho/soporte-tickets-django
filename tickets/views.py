from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView

from .asignacion import asignar_siguiente_ticket
from .estructuras.red import red_de_areas
from .historial import historial_de
from .models import Area, Ticket


@login_required
def lista_tickets(request):
    es_agente = (
        request.user.groups.filter(name="Agente").exists()
        or request.user.is_superuser
    )
    if es_agente:
        filtro = Q(estado="abierto") & (
            Q(impacto=3) | Q(categoria__peso__gte=3)
        )
        tickets = list(Ticket.objects.filter(filtro))
        tickets.sort(key=lambda t: t.prioridad(), reverse=True)
    else:
        tickets = Ticket.objects.filter(creado_por=request.user)
    return render(
        request,
        "tickets/lista.html",
        {"tickets": tickets, "es_agente": es_agente},
    )


@login_required
def asignar_siguiente(request):
    ticket = asignar_siguiente_ticket()
    if ticket is None:
        messages.info(request, "No hay tickets pendientes")
    else:
        messages.success(request, "Ticket asignado: " + ticket.titulo)
    return redirect("tickets:lista")


class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = "tickets/todos.html"
    context_object_name = "tickets"
    paginate_by = 5
    ordering = ["-creado"]


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


@login_required
def red_areas(request):
    areas = Area.objects.order_by("nombre")
    red = red_de_areas(areas)
    filas = []
    for i, nombre in enumerate(red.nombres):
        filas.append(
            {
                "nombre": nombre,
                "valores": red.matriz[i],
                "salen": red.grado(nombre),
                "llegan": red.grado_entrada(nombre),
            }
        )
    return render(
        request,
        "tickets/red_areas.html",
        {"nombres": red.nombres, "filas": filas},
    )
