from .models import Categoria
from .estructuras.arbol_categorias import construir_arbol


def menu_categorias(request):
    return {"menu_categorias": construir_arbol(Categoria.objects.all())}
