# Sistema de Gestión de Tickets de Soporte

Proyecto de portafolio del curso **Estructura de Datos y Algoritmos** (semanas 8, 9 y 10).

## Semana 10 — Prioridad del ticket con un árbol de expresión e inicio de sesión

- `Categoria` tiene el campo `peso` (1 normal, 3 crítica) y `Ticket` tiene
  `creado`, `impacto`, `categoria` y `creado_por`. Migración `0003` aplicada.
- `tickets/estructuras/arbol_expresion.py` contiene `NodoExpresion`,
  `construir_postfija` y `evaluar_con_variables`. La fórmula se guarda en
  postfija (`"impacto peso * dias +"`) y el árbol la calcula con el diccionario
  de valores; no se usa `eval()`.
- `Ticket.prioridad()` arma el árbol con `FORMULA_PRIORIDAD` y lo evalúa con
  `evaluar_con_variables(arbol, valores)`.
- Inicio y cierre de sesión con `django.contrib.auth` en `/cuentas/` y la
  plantilla `registration/login.html`.
- Grupos `Cliente` y `Agente`. El agente ve los tickets abiertos urgentes
  (filtro `Q(estado="abierto") & (Q(impacto=3) | Q(categoria__peso__gte=3))`)
  ordenados por prioridad; el cliente solo ve los tickets que creó.
- `@login_required` manda al login a quien no inició sesión.

### Cómo ejecutar

```bash
pip install django
python manage.py migrate
python manage.py cargar_datos_s08        # ticket de prueba con 5 comentarios
python manage.py cargar_categorias_s09   # categorías de ejemplo (3 niveles)
python manage.py cargar_datos_s10        # categorías con peso, usuarios y tickets de prueba
python manage.py runserver
```

- Lista de tickets: http://127.0.0.1:8000/
- Detalle del ticket: http://127.0.0.1:8000/ticket/1/
- Login: http://127.0.0.1:8000/cuentas/login/
- Admin: http://127.0.0.1:8000/admin/ (usuario `admin` / contraseña `soporte2026`, solo para desarrollo local)
- Usuarios de prueba: `nicolas` (Cliente), `carla` (Cliente), `agente` (Agente).
  Contraseñas de desarrollo: `cliente2026` y `agente2026`.

### Evidencias de la Semana 10

En `evidencias/`:

- `01_login.png` — formulario de ingreso en `/cuentas/login/`.
- `03_lista_cliente.png` — el cliente `nicolas` ve solo sus tickets.
- `04_lista_agente.png` — el agente ve los tickets urgentes ordenados por prioridad.
- `05_shell_prioridades.png` — `prioridad()` ejecutado en `python manage.py shell`.
- `06_migracion.png` — migración `0003` aplicada y sin cambios pendientes.

### Preguntas de la guía de la Semana 10

**a) En el filtro con `Q()` del paso 2, ¿cuáles son las hojas y cuáles los nodos internos?**

R: Las hojas son cada condición: `Q(estado="abierto")`, `Q(impacto=3)` y
`Q(categoria__peso__gte=3)`. Los nodos internos son los conectores: el `OR`
une las dos últimas condiciones y el `AND` es la raíz que une `estado="abierto"`
con ese `OR`.

**b) ¿Por qué conviene guardar la fórmula de prioridad en postfija y no en infija?**

R: Porque en postfija no hacen falta paréntesis ni reglas de precedencia: el
árbol se arma con una pila leyendo los tokens en orden, y cada operador toma
los dos últimos operandos. Además, si cambia la regla de negocio solo se
modifica el texto de la fórmula, sin tocar el código que la evalúa.

### Commit de la Semana 10

Enlace del commit: COMMIT_S10_URL

Repositorio: https://github.com/NicolasPumaLuicho/soporte-tickets-django

---

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

Enlace del commit: https://github.com/NIckKIng6969/soporte-tickets-django/commit/53f38ec15d35c71909c65532af6b72c8cede5214

Repositorio: https://github.com/NIckKIng6969/soporte-tickets-django

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
