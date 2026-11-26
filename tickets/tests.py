from django.test import SimpleTestCase, TestCase
from .estructuras.arbol_bst import construir_balanceado, a_lista, altura, contar_pasos
from .estructuras.cola_prioridad import MinHeap, primeros
from .estructuras.pila_historial import PilaEstados
from .estructuras.red import red_de_areas
from .estados import cambiar_estado, deshacer_ultimo_cambio
from .models import Area, Ticket


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


class ColaUrgentesTest(SimpleTestCase):
    def test_sale_el_mas_urgente(self):
        cola = MinHeap()
        cola.insertar((-3, 1, "Mouse"))
        cola.insertar((-10, 2, "Sin internet"))
        cola.insertar((-7, 3, "Impresora"))
        salida = primeros(cola, 1)
        self.assertEqual(salida[0]["titulo"], "Sin internet")
        self.assertEqual(salida[0]["prioridad"], 10)

    def test_empate_gana_el_mas_antiguo(self):
        cola = MinHeap()
        cola.insertar((-5, 8, "Teclado"))
        cola.insertar((-5, 2, "Correo"))
        self.assertEqual(primeros(cola, 1)[0]["id"], 2)

    def test_cola_vacia(self):
        self.assertEqual(primeros(MinHeap(), 3), [])

    def test_orden_completo(self):
        cola = MinHeap()
        datos = [(4, 1, "Teclado"), (9, 2, "Sin internet"),
                 (1, 3, "Mouse"), (7, 4, "Impresora"),
                 (9, 5, "Servidor"), (2, 6, "Correo")]
        for prioridad, id, titulo in datos:
            cola.insertar((-prioridad, id, titulo))
        salida = primeros(cola, 10)
        self.assertEqual([t["prioridad"] for t in salida], [9, 9, 7, 4, 2, 1])


class UrgentesAPITest(TestCase):
    def test_pide_login(self):
        respuesta = self.client.get("/api/tickets/urgentes/")
        self.assertEqual(respuesta.status_code, 403)


class RedAreasTest(TestCase):
    def test_red_es_dirigida(self):
        mesa = Area.objects.create(nombre="Mesa de ayuda")
        redes = Area.objects.create(nombre="Redes")
        mesa.deriva_a.add(redes)
        red = red_de_areas(Area.objects.order_by("nombre"))
        self.assertEqual(red.vecinos("Mesa de ayuda"), ["Redes"])
        self.assertEqual(red.vecinos("Redes"), [])

    def test_area_sin_derivaciones(self):
        Area.objects.create(nombre="Seguridad")
        red = red_de_areas(Area.objects.order_by("nombre"))
        self.assertEqual(red.grado("Seguridad"), 0)
        self.assertEqual(red.grado_entrada("Seguridad"), 0)


class PilaEstadosTest(SimpleTestCase):
    def test_desapila_en_orden_inverso(self):
        pila = PilaEstados()
        for estado in ["abierto", "en_proceso", "cerrado"]:
            pila.apilar(estado)
        self.assertEqual(pila.desapilar(), "cerrado")
        self.assertEqual(pila.desapilar(), "en_proceso")
        self.assertEqual(pila.cima(), "abierto")

    def test_pila_vacia(self):
        pila = PilaEstados()
        self.assertTrue(pila.esta_vacia())
        self.assertIsNone(pila.desapilar())


class DeshacerEstadoTest(TestCase):
    def test_deshace_el_ultimo_cambio(self):
        ticket = Ticket.objects.create(titulo="Impresora sin conexión")
        cambiar_estado(ticket, "en_proceso")
        cambiar_estado(ticket, "cerrado")
        self.assertTrue(deshacer_ultimo_cambio(ticket))
        self.assertEqual(ticket.estado, "en_proceso")
        ticket.refresh_from_db()
        self.assertEqual(ticket.estado, "en_proceso")

    def test_sin_cambios_no_deshace(self):
        ticket = Ticket.objects.create(titulo="Correo duplicado")
        self.assertFalse(deshacer_ultimo_cambio(ticket))
        self.assertEqual(ticket.estado, "abierto")
