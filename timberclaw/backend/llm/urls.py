from django.urls import path

from . import views

urlpatterns = [
    path("invoke/", views.LLMInvokeView.as_view()),
]
