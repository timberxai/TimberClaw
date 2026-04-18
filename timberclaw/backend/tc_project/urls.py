from django.contrib import admin
from django.urls import include, path

from gitlab_integration.views import HealthGitLabView
from llm.views import HealthLLMView

from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/health/", views.health),
    path("api/health/llm/", HealthLLMView.as_view()),
    path("api/health/gitlab/", HealthGitLabView.as_view()),
    path("api/", include("accounts.urls")),
    path("api/llm/", include("llm.urls")),
]
