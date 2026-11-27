from django.contrib import admin

from .models import Area, Articulo, Categoria, CodigoPrueba, Comentario, Ticket


class ComentarioInline(admin.TabularInline):
    model = Comentario
    extra = 1


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("titulo", "estado", "impacto", "categoria", "creado_por", "resuelto_por", "fecha")
    list_filter = ("estado", "impacto", "categoria", "resuelto_por")
    inlines = [ComentarioInline]


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ("ticket", "autor", "fecha")
    list_filter = ("autor",)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "peso", "padre")
    search_fields = ("nombre",)


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    filter_horizontal = ("deriva_a",)


@admin.register(CodigoPrueba)
class CodigoPruebaAdmin(admin.ModelAdmin):
    list_display = ("sin_indice", "con_indice")


@admin.register(Articulo)
class ArticuloAdmin(admin.ModelAdmin):
    list_display = ("titulo",)
    search_fields = ("titulo",)
