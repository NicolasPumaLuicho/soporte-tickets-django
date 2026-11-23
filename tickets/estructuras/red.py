from .grafo import Grafo


def red_de_areas(areas):
    nombres = [area.nombre for area in areas]
    red = Grafo(nombres, es_dirigido=True)
    for area in areas:
        for destino in area.deriva_a.all():
            red.agregar_arista(area.nombre, destino.nombre)
    return red
