from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/health/", views.health),
    path("api/", include("accounts.urls")),
]
