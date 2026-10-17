# Sistema de Gestión de Tickets de Soporte

Proyecto de portafolio del curso **Estructura de Datos y Algoritmos** (semanas 8 y 9).

## Semana 9 — Menú de categorías con un árbol genérico

- Modelo `Categoria` con un campo `padre` que apunta a la misma tabla (`"self"`).
  Una categoría sin padre es de primer nivel y sus hijas se consultan con
  `subcategorias`.
- Migración `0002_categoria` aplicada y `Categoria` registrada en el Django Admin.
- `tickets/estructuras/arbol_categorias.py` contiene `NodoGenerico`, `mostrar` y
  `construir_arbol`. Esta última arma el árbol con un diccionario `id → nodo`,
  sin librerías externas.
- `tickets/context_processors.py` entrega el árbol a todas las plantillas como
  `menu_categorias`.
- `tickets/templatetags/menu_tags.py` define la etiqueta recursiva `nodo_menu`,
  que usa `tickets/_nodo_menu.html`. El menú completo se incluye en `base.html`
  con `{% include "tickets/_menu_categorias.html" %}`.
- El menú se muestra en la lista de tickets y en el detalle de cada ticket.
  Al agregar una categoría desde el admin, aparece al recargar sin modificar
  ninguna plantilla.

### Cómo ejecutar

```bash
pip install django
python manage.py migrate
python manage.py cargar_datos_s08        # ticket de prueba con 5 comentarios
python manage.py cargar_categorias_s09   # categorías de ejemplo (3 niveles)
python manage.py runserver
```

- Lista de tickets: http://127.0.0.1:8000/
- Detalle del ticket: http://127.0.0.1:8000/ticket/1/
- Admin: http://127.0.0.1:8000/admin/ (usuario `admin` / contraseña `soporte2026`, solo para desarrollo local)

### Evidencias de la Semana 9

En `evidencias/`:

- `01_menu_inicio.png` — menú con las categorías de tres niveles antes de agregar la nueva.
- `02_admin_categorias.png` — admin con las 12 categorías y su categoría padre.
- `03_admin_nueva_categoria.png` — alta de «WiFi invitados» con padre «WiFi».
- `04_admin_categoria_guardada.png` — confirmación del alta y la nueva fila en el admin.
- `05_menu_con_nueva_categoria.png` — el menú recargado ya muestra «WiFi invitados».
- `06_menu_detalle_ticket.png` — el mismo menú en el detalle del ticket.
- `07_shell_arbol.png` — `construir_arbol` y `mostrar` ejecutados en `python manage.py shell`.

### Preguntas de la guía de la Semana 9

**a) ¿Qué recorrido del laboratorio sigue el template tag recursivo y por qué?**

R: Sigue un recorrido preorden: dibuja el nodo (el padre) y después se llama a
sí mismo por cada hijo, de izquierda a derecha. Es el mismo orden de `mostrar`
del laboratorio y así el `<ul>` anidado refleja la profundidad; el caso base es
un nodo sin hijos.

**b) ¿Qué pasaría con el menú si una categoría tuviera como padre a una de sus propias subcategorías?**

R: Se formaría un ciclo y esa rama nunca tendría un camino hasta la raíz
«Categorías», por lo que `construir_arbol` no la colgaría de la raíz y el menú
no la mostraría. Si se intentara dibujar el ciclo directamente, la etiqueta se
llamaría a sí misma sin parar; por eso hay que evitar que un padre sea
descendiente de la propia categoría.

### Commit de la Semana 9

Pendiente de subir al repositorio del equipo:

```bash
git add .
git commit -m "S09: menú de categorías con árbol genérico"
git push
```

Enlace del commit: _(pegar aquí después del push)_

---

## Semana 8 — Historial de comentarios con lista doblemente enlazada

- Modelo `Comentario` con `ForeignKey` a `Ticket` (`related_name="comentarios"`),
  texto, autor y fecha de creación.
- Migración aplicada y `Comentario` registrado en el Django Admin.
- Clase `HistorialComentarios` (lista doblemente enlazada propia, sin librerías
  externas) en `tickets/historial.py`, con `actual()`, `anterior()` y `siguiente()`.
- Vista de detalle del ticket que muestra **un comentario a la vez** con los
  botones «Anterior» y «Siguiente».

### Preguntas de la guía de la Semana 8

**a) ¿Qué equivale, en su lista doble, a `has_previous()` y a `has_next()` del Paginator?**

R: Equivalen a comprobar si el puntero actual tiene nodo anterior o siguiente.
En la lista, `has_previous()` es `historial.actual.anterior is not None` y
`has_next()` es `historial.actual.siguiente is not None`; es decir, devolver
`False` cuando el puntero ya está en la cabeza o en la cola. En la vista, esas
comprobaciones son las que deciden si el botón «Anterior» o «Siguiente» se
muestra habilitado o deshabilitado.

**b) Si llega un comentario nuevo mientras el agente lee el comentario 3, ¿qué método de su lista doble usarían para agregarlo al final sin perder la posición actual?**

R: El método que inserta al final de la lista (`agregar_al_final()`). Como
conserva los enlaces de todos los nodos y solo engancha el nodo nuevo después
de la cola, el puntero actual se queda donde estaba: el agente sigue leyendo
el comentario 3 y el comentario nuevo queda disponible al final del historial.

## Integrantes

- Nicolás Puma Luicho
- _(compañero/a de equipo — completar)_
