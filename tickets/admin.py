from django.contrib import admin

from .models import Categoria, Comentario, Ticket


class ComentarioInline(admin.TabularInline):
    model = Comentario
    extra = 1


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("titulo", "estado", "fecha")
    list_filter = ("estado",)
    inlines = [ComentarioInline]


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ("ticket", "autor", "fecha")
    list_filter = ("autor",)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "padre")
    search_fields = ("nombre",)
