from datetime import timedelta

from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand
from django.utils import timezone

from tickets.models import Categoria, Ticket


class Command(BaseCommand):
    help = "Carga categorias, grupos, usuarios y tickets de prueba de la Semana 10"

    def handle(self, *args, **options):
        hardware, _ = Categoria.objects.get_or_create(nombre="Hardware", defaults={"peso": 3})
        software, _ = Categoria.objects.get_or_create(nombre="Software", defaults={"peso": 1})
        red, _ = Categoria.objects.get_or_create(nombre="Red", defaults={"peso": 2})

        grupo_cliente, _ = Group.objects.get_or_create(name="Cliente")
        grupo_agente, _ = Group.objects.get_or_create(name="Agente")

        nicolas, _ = User.objects.get_or_create(username="nicolas")
        nicolas.set_password("cliente2026")
        nicolas.save()
        nicolas.groups.add(grupo_cliente)

        carla, _ = User.objects.get_or_create(username="carla")
        carla.set_password("cliente2026")
        carla.save()
        carla.groups.add(grupo_cliente)

        agente, _ = User.objects.get_or_create(username="agente")
        agente.set_password("agente2026")
        agente.save()
        agente.groups.add(grupo_agente)

        ahora = timezone.now()
        datos = [
            ("Impresora atascada", 2, hardware, 4, "abierto", nicolas),
            ("Excel no abre", 3, software, 1, "abierto", nicolas),
            ("Clave olvidada", 1, software, 0, "abierto", nicolas),
            ("WiFi no conecta", 3, red, 0, "abierto", nicolas),
            ("Monitor no enciende", 3, hardware, 2, "abierto", carla),
            ("Correo lento", 2, red, 5, "abierto", carla),
            ("Servidor caído", 3, hardware, 1, "abierto", carla),
            ("Ticket cerrado urgente", 3, hardware, 3, "cerrado", carla),
        ]
        for titulo, impacto, categoria, dias, estado, usuario in datos:
            Ticket.objects.get_or_create(
                titulo=titulo,
                defaults={
                    "impacto": impacto,
                    "categoria": categoria,
                    "creado": ahora - timedelta(days=dias),
                    "estado": estado,
                    "creado_por": usuario,
                },
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Datos cargados: {Categoria.objects.count()} categorias, "
                f"{Ticket.objects.count()} tickets, {User.objects.count()} usuarios"
            )
        )
