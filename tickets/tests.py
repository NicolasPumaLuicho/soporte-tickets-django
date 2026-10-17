import io
from contextlib import redirect_stdout

from django.test import TestCase
from django.urls import reverse

from .estructuras.arbol_categorias import construir_arbol, mostrar
from .historial import historial_de
from .models import Categoria, Comentario, Ticket


class HistorialComentariosTests(TestCase):
    def setUp(self):
        self.ticket = Ticket.objects.create(titulo="Prueba")
        for i in range(1, 6):
            Comentario.objects.create(ticket=self.ticket, autor=f"Autor {i}", texto=f"Comentario {i}")

    def test_recorrido_completo_en_ambos_sentidos(self):
        historial = historial_de(self.ticket)

        self.assertEqual(historial.actual().texto, "Comentario 1")

        for numero in range(2, 6):
            self.assertTrue(historial.siguiente())
            self.assertEqual(historial.actual().texto, f"Comentario {numero}")

        self.assertFalse(historial.siguiente())

        for numero in range(4, 0, -1):
            self.assertTrue(historial.anterior())
            self.assertEqual(historial.actual().texto, f"Comentario {numero}")

        self.assertFalse(historial.anterior())

    def test_agregar_al_final_no_mueve_el_puntero(self):
        historial = historial_de(self.ticket)
        historial.posicionar(3)

        Comentario.objects.create(ticket=self.ticket, autor="Otro", texto="Comentario nuevo")
        historial.agregar_al_final(self.ticket.comentarios.order_by("fecha").last())

        self.assertEqual(historial.actual().texto, "Comentario 3")
        self.assertEqual(len(historial), 6)

    def test_posicionar_invalida_devuelve_false(self):
        historial = historial_de(self.ticket)
        self.assertFalse(historial.posicionar(0))
        self.assertFalse(historial.posicionar(99))


class DetalleTicketTests(TestCase):
    def setUp(self):
        self.ticket = Ticket.objects.create(titulo="Ticket de prueba")
        for i in range(1, 6):
            Comentario.objects.create(ticket=self.ticket, autor=f"Autor {i}", texto=f"Comentario {i}")

    def test_muestra_un_comentario_a_la_vez(self):
        respuesta = self.client.get(reverse("tickets:detalle", args=[self.ticket.id]))
        self.assertContains(respuesta, "Comentario 1")
        self.assertNotContains(respuesta, "Comentario 2")
        self.assertContains(respuesta, "Comentario 1 de 5")

    def test_recorrido_con_botones_en_ambos_sentidos(self):
        for numero in range(2, 6):
            respuesta = self.client.get(
                reverse("tickets:detalle", args=[self.ticket.id]), {"pos": numero}
            )
            self.assertContains(respuesta, f"Comentario {numero}")

        for numero in range(4, 0, -1):
            respuesta = self.client.get(
                reverse("tickets:detalle", args=[self.ticket.id]), {"pos": numero}
            )
            self.assertContains(respuesta, f"Comentario {numero}")

    def test_botones_deshabilitados_en_los_extremos(self):
        primera = self.client.get(reverse("tickets:detalle", args=[self.ticket.id]))
        self.assertContains(primera, "boton-deshabilitado")
        self.assertEqual(primera.context["hay_anterior"], False)
        self.assertEqual(primera.context["hay_siguiente"], True)

        ultima = self.client.get(
            reverse("tickets:detalle", args=[self.ticket.id]), {"pos": 5}
        )
        self.assertEqual(ultima.context["hay_anterior"], True)
        self.assertEqual(ultima.context["hay_siguiente"], False)


class ArbolCategoriasTests(TestCase):
    def setUp(self):
        hardware = Categoria.objects.create(nombre="Hardware")
        impresoras = Categoria.objects.create(nombre="Impresoras", padre=hardware)
        Categoria.objects.create(nombre="Atasco de papel", padre=impresoras)
        Categoria.objects.create(nombre="Cuentas y accesos")

    def test_construir_arbol_arma_jerarquia_de_tres_niveles(self):
        raiz = construir_arbol(Categoria.objects.all())

        self.assertEqual(raiz.nombre, "Categorías")
        self.assertEqual([nodo.nombre for nodo in raiz.hijos], ["Hardware", "Cuentas y accesos"])

        hardware = raiz.hijos[0]
        self.assertEqual([nodo.nombre for nodo in hardware.hijos], ["Impresoras"])
        self.assertEqual(
            [nodo.nombre for nodo in hardware.hijos[0].hijos],
            ["Atasco de papel"],
        )

    def test_mostrar_imprime_el_arbol_con_sangria(self):
        salida = io.StringIO()
        with redirect_stdout(salida):
            mostrar(construir_arbol(Categoria.objects.all()))

        self.assertIn("Categorías\n    Hardware\n        Impresoras\n            Atasco de papel", salida.getvalue())

    def test_menu_aparece_en_las_paginas_y_toma_los_cambios_de_la_base(self):
        ticket = Ticket.objects.create(titulo="Ticket con categorías")
        respuesta = self.client.get(reverse("tickets:lista"))
        self.assertContains(respuesta, "Hardware")
        self.assertContains(respuesta, "Atasco de papel")

        Categoria.objects.create(nombre="WiFi invitados", padre=Categoria.objects.get(nombre="Hardware"))
        respuesta = self.client.get(reverse("tickets:detalle", args=[ticket.id]))
        self.assertContains(respuesta, "WiFi invitados")

