from django.contrib import admin
from django.urls import include, path

from tickets.api import UrgentesAPI

urlpatterns = [
    path("admin/", admin.site.urls),
    path("cuentas/", include("django.contrib.auth.urls")),
    path("api/tickets/urgentes/", UrgentesAPI.as_view(), name="urgentes"),
    path("", include("tickets.urls")),
]
