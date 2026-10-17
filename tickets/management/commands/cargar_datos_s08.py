"""Carga 5 comentarios de un ticket (dos integrantes distintos) y reproduce
la comprobación del Paginator de Django, tal como en la guía de la Semana 8.

Uso:
    python manage.py cargar_datos_s08
"""

from django.core.management.base import BaseCommand
from django.core.paginator import Paginator

from tickets.models import Comentario, Ticket

COMENTARIOS = [
    ("Nicolás Puma", "El cliente reporta que el sistema no carga el historial de compras."),
    ("Compañero de equipo", "Confirmo el problema; lo reproduje con el usuario de prueba."),
    ("Nicolás Puma", "Revisé los registros del servidor: la consulta demora más de 8 segundos."),
    ("Compañero de equipo", "Agregué un índice a la tabla de compras; la consulta bajó a 1 segundo."),
    ("Nicolás Puma", "Probado en el ambiente de QA: el historial ya carga rápido. Cierro el ticket."),
]


class Command(BaseCommand):
    help = "Carga el ticket de prueba con 5 comentarios y reproduce la comprobación del Paginator."

    def handle(self, *args, **options):
        ticket, creado = Ticket.objects.get_or_create(
            titulo="El historial de compras no carga",
            defaults={
                "descripcion": "El cliente no puede ver el historial de compras en su cuenta.",
                "estado": "en_proceso",
            },
        )
        if creado:
            for autor, texto in COMENTARIOS:
                Comentario.objects.create(ticket=ticket, autor=autor, texto=texto)
            self.stdout.write(f"Ticket creado: {ticket}")
        else:
            self.stdout.write(f"Ticket ya existente: {ticket}")

        total = ticket.comentarios.count()
        self.stdout.write(f"Comentarios del ticket: {total}")

        # ---- Comprobación del Paginator (guía, paso 3 y 4) ----
        p = Paginator(ticket.comentarios.order_by("fecha"), 1)
        self.stdout.write("")
        self.stdout.write(f"p = Paginator(ticket.comentarios.order_by('fecha'), 1)  -> {p.count} páginas")

        for numero in (2, 1, p.num_pages):
            pagina = p.page(numero)
            etiqueta = {1: "primera", p.num_pages: "última"}.get(numero, str(numero))
            self.stdout.write("")
            self.stdout.write(
                f"pagina = p.page({numero})   # {etiqueta} página ({pagina.object_list[0].autor})"
            )
            self.stdout.write(f"pagina.has_previous()          -> {pagina.has_previous()}")
            self.stdout.write(f"pagina.has_next()              -> {pagina.has_next()}")
            try:
                valor = pagina.previous_page_number()
            except Exception as error:
                valor = f"{type(error).__name__} ({error})"
            self.stdout.write(f"pagina.previous_page_number()  -> {valor}")
            try:
                valor = pagina.next_page_number()
            except Exception as error:
                valor = f"{type(error).__name__} ({error})"
            self.stdout.write(f"pagina.next_page_number()      -> {valor}")
