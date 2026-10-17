class NodoGenerico:
    def __init__(self, nombre):
        self.nombre = nombre
        self.hijos = []


def mostrar(nodo, nivel=0):
    print("    " * nivel + nodo.nombre)
    for hijo in nodo.hijos:
        mostrar(hijo, nivel + 1)


def construir_arbol(categorias):
    categorias = list(categorias)
    raiz = NodoGenerico("Categorías")
    nodos = {categoria.id: NodoGenerico(categoria.nombre) for categoria in categorias}

    for categoria in categorias:
        nodo = nodos[categoria.id]
        if categoria.padre_id is None:
            raiz.hijos.append(nodo)
        else:
            nodos[categoria.padre_id].hijos.append(nodo)

    return raiz
