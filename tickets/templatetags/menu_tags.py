from django import template

register = template.Library()


@register.inclusion_tag("tickets/_nodo_menu.html")
def nodo_menu(nodo):
    return {"nodo": nodo}
