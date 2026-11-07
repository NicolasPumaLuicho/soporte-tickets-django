from django.test import SimpleTestCase, TestCase
from .estructuras.arbol_bst import construir_balanceado, a_lista, altura, contar_pasos


class ArbolBalanceadoTest(SimpleTestCase):
    def setUp(self):
        self.datos = []
        for i in range(1, 101):
            self.datos.append((i, "Ticket " + str(i)))
        self.raiz = construir_balanceado(self.datos)

    def test_altura_balanceada(self):
        self.assertLessEqual(altura(self.raiz), 7)

    def test_inorden_sale_ordenado(self):
        salida = []
        a_lista(self.raiz, salida)
        self.assertEqual(salida, self.datos)

    def test_lista_vacia(self):
        self.assertIsNone(construir_balanceado([]))


class ListaTicketsTest(TestCase):
    def test_pide_iniciar_sesion(self):
        respuesta = self.client.get("/tickets/todos/")
        self.assertEqual(respuesta.status_code, 302)


class BusquedaTest(SimpleTestCase):
    def test_busqueda_rapida(self):
        datos = []
        for i in range(1, 101):
            datos.append((i, "Ticket " + str(i)))
        raiz = construir_balanceado(datos)
        self.assertLessEqual(contar_pasos(raiz, 100), 7)
