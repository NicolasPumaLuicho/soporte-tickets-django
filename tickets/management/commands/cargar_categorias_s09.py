"""Carga las categorías del menú con al menos tres niveles (Semana 9).

Uso:
    python manage.py cargar_categorias_s09
"""

from django.core.management.base import BaseCommand

from tickets.estructuras.arbol_categorias import construir_arbol, mostrar
from tickets.models import Categoria

CATEGORIAS = [
    ("Hardware", None),
    ("Impresoras", "Hardware"),
    ("Atasco de papel", "Impresoras"),
    ("Sin tinta", "Impresoras"),
    ("Laptops", "Hardware"),
    ("Monitores", "Hardware"),
    ("Software", None),
    ("Office", "Software"),
    ("Correo", "Software"),
    ("Redes", None),
    ("WiFi", "Redes"),
    ("Cuentas y accesos", None),
]


class Command(BaseCommand):
    help = "Carga las categorías de ejemplo con al menos tres niveles."

    def handle(self, *args, **options):
        creadas = 0
        for nombre, nombre_padre in CATEGORIAS:
            padre = Categoria.objects.filter(nombre=nombre_padre).first() if nombre_padre else None
            _, creada = Categoria.objects.get_or_create(nombre=nombre, padre=padre)
            if creada:
                creadas += 1
                self.stdout.write(f"Categoría creada: {nombre}" + (f" (padre: {nombre_padre})" if padre else ""))

        self.stdout.write("")
        self.stdout.write(f"Categorías nuevas: {creadas}")
        self.stdout.write(f"Total de categorías: {Categoria.objects.count()}")
        self.stdout.write("")
        mostrar(construir_arbol(Categoria.objects.all()))
