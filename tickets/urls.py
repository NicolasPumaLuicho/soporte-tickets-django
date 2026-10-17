from django.urls import path

from . import views

app_name = "tickets"

urlpatterns = [
    path("", views.lista_tickets, name="lista"),
    path("ticket/<int:ticket_id>/", views.detalle_ticket, name="detalle"),
]
