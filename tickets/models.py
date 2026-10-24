from django.conf import settings
from django.db import models
from django.utils import timezone

from .estructuras.arbol_expresion import construir_postfija, evaluar_con_variables

FORMULA_PRIORIDAD = "impacto peso * dias +"


class Ticket(models.Model):
    ESTADOS = [
        ("abierto", "Abierto"),
        ("en_proceso", "En proceso"),
        ("cerrado", "Cerrado"),
    ]
    IMPACTO = [(1, "Bajo"), (2, "Medio"), (3, "Alto")]

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="abierto")
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="fecha de creación")
    creado = models.DateTimeField(default=timezone.now)
    impacto = models.PositiveSmallIntegerField(choices=IMPACTO, default=1)
    categoria = models.ForeignKey(
        "Categoria", null=True, blank=True, on_delete=models.SET_NULL
    )
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="tickets",
    )

    class Meta:
        verbose_name = "ticket"
        verbose_name_plural = "tickets"
        ordering = ["-fecha"]

    def __str__(self):
        return self.titulo

    def prioridad(self):
        valores = {
            "impacto": self.impacto,
            "peso": self.categoria.peso if self.categoria else 1,
            "dias": (timezone.now() - self.creado).days,
        }
        arbol = construir_postfija(FORMULA_PRIORIDAD)
        return evaluar_con_variables(arbol, valores)



class Comentario(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="comentarios",
        verbose_name="ticket",
    )
    texto = models.TextField(verbose_name="texto")
    autor = models.CharField(max_length=120, verbose_name="autor")
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="fecha de creación")

    class Meta:
        verbose_name = "comentario"
        verbose_name_plural = "comentarios"
        ordering = ["fecha"]

    def __str__(self):
        return f"{self.autor}: {self.texto[:40]}"


class Categoria(models.Model):
    nombre = models.CharField(max_length=60)
    peso = models.PositiveIntegerField(default=1)
    padre = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="subcategorias",
    )

    def __str__(self):
        return self.nombre
