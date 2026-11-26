from django.urls import path

from . import views

app_name = "tickets"

urlpatterns = [
    path("", views.lista_tickets, name="lista"),
    path(
        "asignar-siguiente/",
        views.asignar_siguiente,
        name="asignar_siguiente",
    ),
    path("ticket/<int:ticket_id>/", views.detalle_ticket, name="detalle"),
    path(
        "tickets/todos/",
        views.TicketListView.as_view(),
        name="tickets_todos",
    ),
]
