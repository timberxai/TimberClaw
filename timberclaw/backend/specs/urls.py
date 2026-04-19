from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SpecDocumentViewSet

router = DefaultRouter()
router.register("documents", SpecDocumentViewSet, basename="spec-document")

urlpatterns = [
    path("", include(router.urls)),
]
