from django.contrib import admin

from .models import Categoria, CodigoPrueba, Comentario, Ticket


class ComentarioInline(admin.TabularInline):
    model = Comentario
    extra = 1


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("titulo", "estado", "impacto", "categoria", "creado_por", "fecha")
    list_filter = ("estado", "impacto", "categoria")
    inlines = [ComentarioInline]


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ("ticket", "autor", "fecha")
    list_filter = ("autor",)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "peso", "padre")
    search_fields = ("nombre",)


@admin.register(CodigoPrueba)
class CodigoPruebaAdmin(admin.ModelAdmin):
    list_display = ("sin_indice", "con_indice")
