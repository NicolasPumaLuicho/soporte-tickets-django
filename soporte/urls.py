from django.contrib import admin
from django.urls import include, path

from tickets import views
from tickets.api import UrgentesAPI

urlpatterns = [
    path("admin/", admin.site.urls),
    path("cuentas/", include("django.contrib.auth.urls")),
    path("areas/red/", views.red_areas, name="red_areas"),
    path("tablero/", views.tablero, name="tablero"),
    path("api/tickets/urgentes/", UrgentesAPI.as_view(), name="urgentes"),
    path("", include("tickets.urls")),
]
