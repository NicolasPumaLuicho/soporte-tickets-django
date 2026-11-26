from django.core.management.base import BaseCommand

from tickets.models import Articulo

ARTICULOS = [
    ("Cambiar contraseña", "Ingresa a Mi perfil y usa la opción Restablecer contraseña."),
    ("Conectar impresora", "Revisa que la impresora esté en la misma red y usa Agregar dispositivo."),
    ("No llega el correo", "Verifica la carpeta de spam y vuelve a enviar la notificación."),
    ("Reiniciar el router", "Desconecta el equipo 30 segundos y vuelve a encenderlo."),
    ("Restablecer VPN", "Cierra la sesión de VPN, borra el perfil y vuelve a conectarte."),
    ("Windows no arranca", "Ingresa en modo seguro y revisa las actualizaciones pendientes."),
]


class Command(BaseCommand):
    help = "Carga los artículos de ayuda de prueba de la Semana 6"

    def handle(self, *args, **options):
        for titulo, contenido in ARTICULOS:
            articulo, creado = Articulo.objects.get_or_create(
                titulo=titulo, defaults={"contenido": contenido}
            )
            estado = "creado" if creado else "ya existía"
            self.stdout.write(f"{articulo.titulo}: {estado}")
        self.stdout.write(
            self.style.SUCCESS(f"{Articulo.objects.count()} artículos en el catálogo")
        )
