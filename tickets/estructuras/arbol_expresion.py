class NodoExpresion:
    def __init__(self, valor, izq=None, der=None):
        self.valor = valor
        self.izq = izq
        self.der = der

    def es_hoja(self):
        return self.izq is None and self.der is None


def construir_postfija(postfija):
    pila = []
    for token in postfija.split():
        if token.isalnum():
            pila.append(NodoExpresion(token))
        else:
            der = pila.pop()
            izq = pila.pop()
            pila.append(NodoExpresion(token, izq, der))
    return pila.pop()


def evaluar_con_variables(nodo, valores):
    if nodo.es_hoja():
        if nodo.valor.isdigit():
            return int(nodo.valor)
        return valores[nodo.valor]
    val_izq = evaluar_con_variables(nodo.izq, valores)
    val_der = evaluar_con_variables(nodo.der, valores)
    if nodo.valor == "+":
        return val_izq + val_der
    if nodo.valor == "-":
        return val_izq - val_der
    if nodo.valor == "*":
        return val_izq * val_der
    if nodo.valor == "/":
        if val_der == 0:
            return None
        return val_izq // val_der
    return None
