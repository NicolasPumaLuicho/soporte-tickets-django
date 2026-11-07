import random


class NodoBST:
    def __init__(self, codigo, nombre):
        self.codigo = codigo
        self.nombre = nombre
        self.izq = None
        self.der = None


def insertar(raiz, codigo, nombre):
    if raiz is None:
        return NodoBST(codigo, nombre)
    if codigo < raiz.codigo:
        raiz.izq = insertar(raiz.izq, codigo, nombre)
    else:
        raiz.der = insertar(raiz.der, codigo, nombre)
    return raiz


def buscar_con_pasos(raiz, codigo):
    actual = raiz
    pasos = 0
    while actual is not None:
        pasos = pasos + 1
        print("  revisa", actual.codigo)
        if codigo == actual.codigo:
            return pasos
        elif codigo < actual.codigo:
            actual = actual.izq
        else:
            actual = actual.der
    return pasos


def altura(nodo):
    if nodo is None:
        return 0
    return 1 + max(altura(nodo.izq), altura(nodo.der))


def construir_indice(tickets, mezclar=True):
    datos = [(t.id, t.titulo) for t in tickets]
    if mezclar:
        random.shuffle(datos)

    raiz = None
    for codigo, titulo in datos:
        raiz = insertar(raiz, codigo, titulo)
    return raiz


def a_lista(nodo, datos):
    if nodo is not None:
        a_lista(nodo.izq, datos)
        datos.append((nodo.codigo, nodo.nombre))
        a_lista(nodo.der, datos)


def construir_balanceado(datos):
    if len(datos) == 0:
        return None

    medio = len(datos) // 2
    codigo, nombre = datos[medio]
    nodo = NodoBST(codigo, nombre)
    nodo.izq = construir_balanceado(datos[:medio])
    nodo.der = construir_balanceado(datos[medio + 1:])
    return nodo


def construir_indice_balanceado(tickets):
    datos = [(t.id, t.titulo) for t in tickets]
    datos.sort()
    return construir_balanceado(datos)


def contar_pasos(raiz, codigo):
    actual = raiz
    pasos = 0
    while actual is not None:
        pasos = pasos + 1
        if codigo == actual.codigo:
            return pasos
        elif codigo < actual.codigo:
            actual = actual.izq
        else:
            actual = actual.der
    return pasos
