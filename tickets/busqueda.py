"""Búsqueda binaria propia sobre el catálogo de artículos de ayuda.

Recuperación de la Semana 6: no se usa filter() ni bisect. El catálogo se
ordena por título y la búsqueda parte el rango a la mitad en cada paso,
contando las comparaciones realizadas.
"""

from .models import Articulo


def buscar_articulo(titulo):
    """Devuelve (articulo, comparaciones). Si no existe, el artículo es None."""
    articulos = list(Articulo.objects.order_by("titulo"))
    titulos = [articulo.titulo for articulo in articulos]
    inicio = 0
    fin = len(titulos) - 1
    comparaciones = 0
    while inicio <= fin:
        medio = (inicio + fin) // 2
        comparaciones += 1
        if titulos[medio] == titulo:
            return articulos[medio], comparaciones
        if titulos[medio] < titulo:
            inicio = medio + 1
        else:
            fin = medio - 1
    return None, comparaciones
