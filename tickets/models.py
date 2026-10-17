from django.db import models


class Ticket(models.Model):
    ESTADOS = [
        ("abierto", "Abierto"),
        ("en_proceso", "En proceso"),
        ("cerrado", "Cerrado"),
    ]

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="abierto")
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="fecha de creación")

    class Meta:
        verbose_name = "ticket"
        verbose_name_plural = "tickets"
        ordering = ["-fecha"]

    def __str__(self):
        return self.titulo


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
    padre = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="subcategorias",
    )

    def __str__(self):
        return self.nombre
